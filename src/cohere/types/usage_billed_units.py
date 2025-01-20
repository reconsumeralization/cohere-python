# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class UsageBilledUnits(UncheckedBaseModel):
    input_tokens: typing.Optional[float] = pydantic.Field(default=None)
    """
    The number of billed input tokens.
    """

    output_tokens: typing.Optional[float] = pydantic.Field(default=None)
    """
    The number of billed output tokens.
    """

    search_units: typing.Optional[float] = pydantic.Field(default=None)
    """
    The number of billed search units.
    """

    classifications: typing.Optional[float] = pydantic.Field(default=None)
    """
    The number of billed classifications units.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow")  # type: ignore # Pydantic v2
    else:

        class Config:
            smart_union = True
            extra = pydantic.Extra.allow
