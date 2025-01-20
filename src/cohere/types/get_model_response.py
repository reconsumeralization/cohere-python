# This file was auto-generated by Fern from our API Definition.

from ..core.unchecked_base_model import UncheckedBaseModel
import typing
import pydantic
from .compatible_endpoint import CompatibleEndpoint
from ..core.pydantic_utilities import IS_PYDANTIC_V2


class GetModelResponse(UncheckedBaseModel):
    """
    Contains information about the model and which API endpoints it can be used with.
    """

    name: typing.Optional[str] = pydantic.Field(default=None)
    """
    Specify this name in the `model` parameter of API requests to use your chosen model.
    """

    endpoints: typing.Optional[typing.List[CompatibleEndpoint]] = pydantic.Field(default=None)
    """
    The API endpoints that the model is compatible with.
    """

    finetuned: typing.Optional[bool] = pydantic.Field(default=None)
    """
    Whether the model has been fine-tuned or not.
    """

    context_length: typing.Optional[float] = pydantic.Field(default=None)
    """
    The maximum number of tokens that the model can process in a single request. Note that not all of these tokens are always available due to special tokens and preambles that Cohere has added by default.
    """

    tokenizer_url: typing.Optional[str] = pydantic.Field(default=None)
    """
    Public URL to the tokenizer's configuration file.
    """

    default_endpoints: typing.Optional[typing.List[CompatibleEndpoint]] = pydantic.Field(default=None)
    """
    The API endpoints that the model is default to.
    """

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow")  # type: ignore # Pydantic v2
    else:

        class Config:
            smart_union = True
            extra = pydantic.Extra.allow
