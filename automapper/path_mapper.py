class MapPath:
    """Represents a recursive path to an object attribute using dot notation (e.g., ob.attribute.sub_attribute)."""

    def __init__(self, path: str):
        if "." not in path:
            raise ValueError(f"Invalid path: '{path}' does not contain '.'")
        self.path = path
        self.attributes = path.split(".")
        if not len(self.attributes) >= 1:
            raise ValueError(
                f"Invalid path: '{path}'. Can´t reference to object attribute."
            )

        self._obj_prefix: str | None = None

    @property
    def obj_prefix(self):
        return self._obj_prefix

    @obj_prefix.setter
    def obj_prefix(self, src_cls_name: str) -> None:
        """Setter for obj_prefix."""
        self._obj_prefix = src_cls_name

    def __call__(self):
        return self.attributes

    def __repr__(self):
        return f"MapPath({self.attributes})"
