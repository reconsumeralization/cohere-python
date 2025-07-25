# This file was auto-generated by Fern from our API Definition.

import typing

import pydantic
from ...core.pydantic_utilities import IS_PYDANTIC_V2
from ...core.unchecked_base_model import UncheckedBaseModel
from ...types.api_meta import ApiMeta
from .v2rerank_response_results_item import V2RerankResponseResultsItem


class V2RerankResponse(UncheckedBaseModel):
    id: typing.Optional[str] = None
    results: typing.List[V2RerankResponseResultsItem] = pydantic.Field()
    """
    An ordered list of ranked documents
    """

    meta: typing.Optional[ApiMeta] = None

    if IS_PYDANTIC_V2:
        model_config: typing.ClassVar[pydantic.ConfigDict] = pydantic.ConfigDict(extra="allow")  # type: ignore # Pydantic v2
    else:

        class Config:
            smart_union = True
            extra = pydantic.Extra.allow
