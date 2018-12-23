# coding=utf-8
"""
General property entity that contains property/apartment complex information.
"""


class PropertyInfo:
    def __init__(self, property_name: str, property_url: str):
        self._property_name: str = property_name
        self._property_url: str = property_url

    def get_property_name(self):
        return self._property_name

    def get_property_url(self):
        return self._property_url

    def __eq__(self, other):
        if isinstance(other, PropertyInfo):
            return (self.get_property_name() == other.get_property_name() and
                    self.get_property_url() == other.get_property_url())

        return False

    def __hash__(self):
        return hash((self._property_name, self._property_url))
