# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
import pydantic
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class LogprobItem(UncheckedBaseModel):
    text: typing.Optional[str] = pydantic.Field(default=None)
    """
    The text chunk for which the log probabilities was calculated.
    """

    token_ids: typing.List[int] = pydantic.Field()
    """
    The token ids of each token used to construct the text chunk.
    """

    logprobs: typing.Optional[typing.List[float]] = pydantic.Field(default=None)
    """
    The log probability of each token used to construct the text chunk.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow")  # type: ignore # Pydantic v2
    else:

        class Config:
            smart_union = True
            extra = pydantic.Extra.allow