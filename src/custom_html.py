from dash import html


class Tag:
    def __init__(
        self,
        text: str | None = None,
        col: tuple[int, int, int] | None = None,
        bg_col: tuple[int, int, int, float] | None = None,
        classes: list | None = None,
    ) -> html.Span:
        self.text = text or ""
        self.tag_style = {
            "color": f"rgb{col}",
            "border-color": f"rgb{col}",
            "background-color": f"rgba{bg_col}",
        }
        self.classes = "tag-badge"
        if classes:
            self.classes += " ".join(classes)
        self.comp = html.Span(
            self.text, style=self.tag_style, className=self.classes
        )
