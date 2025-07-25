# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2
from .chat_message_start_event_delta import ChatMessageStartEventDelta
from .chat_stream_event_type import ChatStreamEventType


class ChatMessageStartEvent(ChatStreamEventType):
    """
    A streamed event which signifies that a stream has started.
    """

    id: typing.Optional[str] = pydantic.Field(default=None)
    """
    Unique identifier for the generated reply.
    """

    delta: typing.Optional[ChatMessageStartEventDelta] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow")  # type: ignore # Pydantic v2
    else:

        class Config:
            smart_union = True
            extra = pydantic.Extra.allow
