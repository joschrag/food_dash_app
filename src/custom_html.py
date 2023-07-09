"""File containing custom html constructs.

Author: Jonas Schrage
Date: 09.07.2023
"""
from dash import html


class Tag:
    """Custom dash.html component class."""

    def __init__(
        self,
        text: str | None = None,
        col: tuple[int, ...] | None = None,
        bg_col: tuple[int | float, ...] | None = None,
        classes: list | None = None,
    ) -> None:
        """Initialize the component class.

        :param text: displayed text, defaults to None
        :type text: str | None, optional
        :param col: font color, defaults to None
        :type col: tuple[int, int, int] | None, optional
        :param bg_col: background color, defaults to None
        :type bg_col: tuple[int, int, int, float] | None, optional
        :param classes: css classes, defaults to None
        :type classes: list | None, optional
        """
        assert len(col) == 3  # type: ignore
        assert len(bg_col) == 4  # type: ignore
        self.text = text or ""
        self.tag_style = {
            "color": f"rgb{col}",
            "border-color": f"rgb{col}",
            "background-color": f"rgba{bg_col}",
        }
        self.classes = "tag-badge "
        if classes:
            self.classes += " ".join(classes)
        self.comp = html.Span(
            html.P(self.text), style=self.tag_style, className=self.classes
        )
