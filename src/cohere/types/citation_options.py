# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
from .citation_options_mode import CitationOptionsMode
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class CitationOptions(UncheckedBaseModel):
    """
    Options for controlling citation generation.
    """

    mode: typing.Optional[CitationOptionsMode] = pydantic.Field(default=None)
    """
    Defaults to `"accurate"`.
    Dictates the approach taken to generating citations as part of the RAG flow by allowing the user to specify whether they want `"accurate"` results, `"fast"` results or no results.
    
    **Note**: `command-r7b-12-2024` only supports `"fast"` and `"off"` modes. Its default is `"fast"`.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow")  # type: ignore # Pydantic v2
    else:

        class Config:
            smart_union = True
            extra = pydantic.Extra.allow