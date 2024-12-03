import base64
import json
import re
import typing

import httpx
from httpx import URL, SyncByteStream, ByteStream

from . import GenerateStreamedResponse, Generation, \
    NonStreamedChatResponse, EmbedResponse, StreamedChatResponse, RerankResponse, ApiMeta, ApiMetaTokens, \
    ApiMetaBilledUnits
from .client import Client, ClientEnvironment
from .core import construct_type
from .manually_maintained.lazy_aws_deps import lazy_boto3, lazy_botocore
from .client_v2 import ClientV2

class AwsClient(Client):
    def __init__(
            self,
            *,
            aws_access_key: typing.Optional[str] = None,
            aws_secret_key: typing.Optional[str] = None,
            aws_session_token: typing.Optional[str] = None,
            aws_region: typing.Optional[str] = None,
            timeout: typing.Optional[float] = None,
            service: typing.Union[typing.Literal["bedrock"], typing.Literal["sagemaker"]],
    ):
        Client.__init__(
            self,
            base_url="https://api.cohere.com",  # this url is unused for BedrockClient
            environment=ClientEnvironment.PRODUCTION,
            client_name="n/a",
            timeout=timeout,
            api_key="n/a",
            httpx_client=httpx.Client(
                event_hooks=get_event_hooks(
                    service=service,
                    aws_access_key=aws_access_key,
                    aws_secret_key=aws_secret_key,
                    aws_session_token=aws_session_token,
                    aws_region=aws_region,
                ),
                timeout=timeout,
            ),
        )


class AwsClientV2(ClientV2):
    def __init__(
            self,
            *,
            aws_access_key: typing.Optional[str] = None,
            aws_secret_key: typing.Optional[str] = None,
            aws_session_token: typing.Optional[str] = None,
            aws_region: typing.Optional[str] = None,
            timeout: typing.Optional[float] = None,
            service: typing.Union[typing.Literal["bedrock"], typing.Literal["sagemaker"]],
    ):
        ClientV2.__init__(
            self,
            base_url="https://api.cohere.com",  # this url is unused for BedrockClient
            environment=ClientEnvironment.PRODUCTION,
            client_name="n/a",
            timeout=timeout,
            api_key="n/a",
            httpx_client=httpx.Client(
                event_hooks=get_event_hooks(
                    service=service,
                    aws_access_key=aws_access_key,
                    aws_secret_key=aws_secret_key,
                    aws_session_token=aws_session_token,
                    aws_region=aws_region,
                ),
                timeout=timeout,
            ),
        )


EventHook = typing.Callable[..., typing.Any]


def get_event_hooks(
        service: str,
        aws_access_key: typing.Optional[str] = None,
        aws_secret_key: typing.Optional[str] = None,
        aws_session_token: typing.Optional[str] = None,
        aws_region: typing.Optional[str] = None,
) -> typing.Dict[str, typing.List[EventHook]]:
    return {
        "request": [
            map_request_to_bedrock(
                service=service,
                aws_access_key=aws_access_key,
                aws_secret_key=aws_secret_key,
                aws_session_token=aws_session_token,
                aws_region=aws_region,
            ),
        ],
        "response": [
            map_response_from_bedrock()
        ],
    }


TextGeneration = typing.TypedDict('TextGeneration',
                                  {"text": str, "is_finished": str, "event_type": typing.Literal["text-generation"]})
StreamEnd = typing.TypedDict('StreamEnd',
                             {"is_finished": str, "event_type": typing.Literal["stream-end"], "finish_reason": str,
                              # "amazon-bedrock-invocationMetrics": {
                              #     "inputTokenCount": int, "outputTokenCount": int, "invocationLatency": int,
                              #     "firstByteLatency": int}
                              })


class Streamer(SyncByteStream):
    lines: typing.Iterator[bytes]

    def __init__(self, lines: typing.Iterator[bytes]):
        self.lines = lines

    def __iter__(self) -> typing.Iterator[bytes]:
        return self.lines


response_mapping: typing.Dict[str, typing.Any] = {
    "chat": NonStreamedChatResponse,
    "embed": EmbedResponse,
    "generate": Generation,
    "rerank": RerankResponse
}

stream_response_mapping: typing.Dict[str, typing.Any] = {
    "chat": StreamedChatResponse,
    "generate": GenerateStreamedResponse,
}


def stream_generator(response: httpx.Response, endpoint: str) -> typing.Iterator[bytes]:
    regex = r"{[^\}]*}"

    for _text in response.iter_lines():
        match = re.search(regex, _text)
        if match:
            obj = json.loads(match.group())
            if "bytes" in obj:
                base64_payload = base64.b64decode(obj["bytes"]).decode("utf-8")
                streamed_obj = json.loads(base64_payload)
                if "event_type" in streamed_obj:
                    response_type = stream_response_mapping[endpoint]
                    parsed = typing.cast(response_type,  # type: ignore
                                         construct_type(type_=response_type, object_=streamed_obj))
                    yield (json.dumps(parsed.dict()) + "\n").encode("utf-8")  # type: ignore


def map_token_counts(response: httpx.Response) -> ApiMeta:
    input_tokens = int(response.headers.get("X-Amzn-Bedrock-Input-Token-Count", -1))
    output_tokens = int(response.headers.get("X-Amzn-Bedrock-Output-Token-Count", -1))
    return ApiMeta(
        tokens=ApiMetaTokens(input_tokens=input_tokens, output_tokens=output_tokens),
        billed_units=ApiMetaBilledUnits(input_tokens=input_tokens, output_tokens=output_tokens),
    )


def map_response_from_bedrock():
    def _hook(
            response: httpx.Response,
    ) -> None:
        stream = response.headers["content-type"] == "application/vnd.amazon.eventstream"
        endpoint = response.request.extensions["endpoint"]
        output: typing.Iterator[bytes]

        if stream:
            output = stream_generator(httpx.Response(
                stream=response.stream,
                status_code=response.status_code,
            ), endpoint)
        else:
            response_type = response_mapping[endpoint]
            response_obj = json.loads(response.read())
            response_obj["meta"] = map_token_counts(response).dict()
            cast_obj: typing.Any = typing.cast(response_type,  # type: ignore
                                   construct_type(
                                       type_=response_type,
                                       # type: ignore
                                       object_=response_obj))

            output = iter([json.dumps(cast_obj.dict()).encode("utf-8")])

        response.stream = Streamer(output)
        
        # reset response object to allow for re-reading
        if hasattr(response, "_content"):
            del response._content
        response.is_stream_consumed = False
        response.is_closed = False

    return _hook


def map_request_to_bedrock(
        service: str,
        aws_access_key: typing.Optional[str] = None,
        aws_secret_key: typing.Optional[str] = None,
        aws_session_token: typing.Optional[str] = None,
        aws_region: typing.Optional[str] = None,
) -> EventHook:
    session = lazy_boto3().Session(
        region_name=aws_region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        aws_session_token=aws_session_token,
    )
    credentials = session.get_credentials()
    signer = lazy_botocore().auth.SigV4Auth(credentials, service, session.region_name)

    def _event_hook(request: httpx.Request) -> None:
        headers = request.headers.copy()
        del headers["connection"]


        api_version = request.url.path.split("/")[-2]
        endpoint = request.url.path.split("/")[-1]
        body = json.loads(request.read())
        model = body["model"]

        url = get_url(
            platform=service,
            aws_region=aws_region,
            model=model,  # type: ignore
            stream="stream" in body and body["stream"],
        )
        request.url = URL(url)
        request.headers["host"] = request.url.host

        if endpoint == "rerank":
            body["api_version"] = get_api_version(version=api_version)

        if "stream" in body:
            del body["stream"]

        if "model" in body:
            del body["model"]

        new_body = json.dumps(body).encode("utf-8")
        request.stream = ByteStream(new_body)
        request._content = new_body
        headers["content-length"] = str(len(new_body))

        aws_request = lazy_botocore().awsrequest.AWSRequest(
            method=request.method,
            url=url,
            headers=headers,
            data=request.read(),
        )
        signer.add_auth(aws_request)

        request.headers = httpx.Headers(aws_request.prepare().headers)
        request.extensions["endpoint"] = endpoint

    return _event_hook


def get_url(
        *,
        platform: str,
        aws_region: typing.Optional[str],
        model: str,
        stream: bool,
) -> str:
    if platform == "bedrock":
        endpoint = "invoke" if not stream else "invoke-with-response-stream"
        return f"https://{platform}-runtime.{aws_region}.amazonaws.com/model/{model}/{endpoint}"
    elif platform == "sagemaker":
        endpoint = "invocations" if not stream else "invocations-response-stream"
        return f"https://runtime.sagemaker.{aws_region}.amazonaws.com/endpoints/{model}/{endpoint}"
    return ""


def get_api_version(*, version: str):
    int_version = {
        "v1": 1,
        "v2": 2,
    }

    return int_version.get(version, 1)