# This file was auto-generated by Fern from our API Definition.

import typing

import httpx

from .http_client import AsyncHttpClient, HttpClient


class BaseClientWrapper:
    def __init__(
        self,
        *,
        client_name: typing.Optional[str] = None,
        token: typing.Union[str, typing.Callable[[], str]],
        base_url: str,
        timeout: typing.Optional[float] = None,
    ):
        self._client_name = client_name
        self._token = token
        self._base_url = base_url
        self._timeout = timeout

    def get_headers(self) -> typing.Dict[str, str]:
        headers: typing.Dict[str, str] = {
            "X-Fern-Language": "Python",
            "X-Fern-SDK-Name": "cohere",
            "X-Fern-SDK-Version": "5.1.6",
        }
        if self._client_name is not None:
            headers["X-Client-Name"] = self._client_name
        headers["Authorization"] = f"Bearer {self._get_token()}"
        return headers

    def _get_token(self) -> str:
        if isinstance(self._token, str):
            return self._token
        else:
            return self._token()

    def get_base_url(self) -> str:
        return self._base_url

    def get_timeout(self) -> typing.Optional[float]:
        return self._timeout


class SyncClientWrapper(BaseClientWrapper):
    def __init__(
        self,
        *,
        client_name: typing.Optional[str] = None,
        token: typing.Union[str, typing.Callable[[], str]],
        base_url: str,
        timeout: typing.Optional[float] = None,
        httpx_client: httpx.Client,
    ):
        super().__init__(client_name=client_name, token=token, base_url=base_url, timeout=timeout)
        self.httpx_client = HttpClient(httpx_client=httpx_client)


class AsyncClientWrapper(BaseClientWrapper):
    def __init__(
        self,
        *,
        client_name: typing.Optional[str] = None,
        token: typing.Union[str, typing.Callable[[], str]],
        base_url: str,
        timeout: typing.Optional[float] = None,
        httpx_client: httpx.AsyncClient,
    ):
        super().__init__(client_name=client_name, token=token, base_url=base_url, timeout=timeout)
        self.httpx_client = AsyncHttpClient(httpx_client=httpx_client)
