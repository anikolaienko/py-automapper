class MapPath:
    """Represents a recursive path to an object attribute using dot notation (e.g., ob.attribute.sub_attribute)."""

    def __init__(self, path: str):
        if "." not in path:
            raise ValueError(f"Invalid path: '{path}' does not contain '.'")

        self.path = path
        self.attributes = path.split(".")
        if not len(self.attributes) >= 2:
            raise ValueError(
                f"Invalid path: '{path}'. Can´t reference to object attribute."
            )

        self.obj_prefix = self.attributes[0]
        self.attributes = self.attributes[1:]

    def __call__(self):
        return self.attributes

    def __repr__(self):
        return f"MapPath({self.attributes})"
