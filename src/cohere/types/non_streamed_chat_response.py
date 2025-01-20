# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import pydantic
import typing
from .chat_citation import ChatCitation
from .chat_document import ChatDocument
from .chat_search_query import ChatSearchQuery
from .chat_search_result import ChatSearchResult
from .finish_reason import FinishReason
from .tool_call import ToolCall
from .message import Message
from .api_meta import ApiMeta
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class NonStreamedChatResponse(UncheckedBaseModel):
    text: str = pydantic.Field()
    """
    Contents of the reply generated by the model.
    """

    generation_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Unique identifier for the generated reply. Useful for submitting feedback.
    """

    response_id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Unique identifier for the response.
    """

    citations: typing.Optional[typing.List[ChatCitation]] = pydantic.Field(default=None)
    """
    Inline citations for the generated reply.
    """

    documents: typing.Optional[typing.List[ChatDocument]] = pydantic.Field(default=None)
    """
    Documents seen by the model when generating the reply.
    """

    is_search_required: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Denotes that a search for documents is required during the RAG flow.
    """

    search_queries: typing.Optional[typing.List[ChatSearchQuery]] = pydantic.Field(default=None)
    """
    Generated search queries, meant to be used as part of the RAG flow.
    """

    search_results: typing.Optional[typing.List[ChatSearchResult]] = pydantic.Field(default=None)
    """
    Documents retrieved from each of the conducted searches.
    """

    finish_reason: typing.Optional[FinishReason] = None
    tool_calls: typing.Optional[typing.List[ToolCall]] = None
    chat_history: typing.Optional[typing.List[Message]] = pydantic.Field(default=None)
    """
    A list of previous messages between the user and the model, meant to give the model conversational context for responding to the user's `message`.
    """

    prompt: typing.Optional[str] = pydantic.Field(default=None)
    """
    The prompt that was used. Only present when `return_prompt` in the request is set to true.
    """

    meta: typing.Optional[ApiMeta] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow")  # type: ignore # Pydantic v2
    else:

        class Config:
            smart_union = True
            extra = pydantic.Extra.allow
