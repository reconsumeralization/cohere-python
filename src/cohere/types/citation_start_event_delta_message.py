# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .citation import Citation
from ..core.pydantic_utilities import IS_PYDANTIC_V2
import pydantic


class CitationStartEventDeltaMessage(UncheckedBaseModel):
    citations: typing.Optional[Citation] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow")  # type: ignore # Pydantic v2
    else:

        class Config:
            smart_union = True
            extra = pydantic.Extra.allow