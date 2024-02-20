# This file was auto-generated by Fern from our API Definition.

import enum
import typing

T_Result = typing.TypeVar("T_Result")


class SummarizeRequestLength(str, enum.Enum):
    """
    One of `short`, `medium`, `long`, or `auto` defaults to `auto`. Indicates the approximate length of the summary. If `auto` is selected, the best option will be picked based on the input text.
    """

    SHORT = "short"
    MEDIUM = "medium"
    LONG = "long"

    def visit(
        self,
        short: typing.Callable[[], T_Result],
        medium: typing.Callable[[], T_Result],
        long: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is SummarizeRequestLength.SHORT:
            return short()
        if self is SummarizeRequestLength.MEDIUM:
            return medium()
        if self is SummarizeRequestLength.LONG:
            return long()