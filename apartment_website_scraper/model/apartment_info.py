# coding=utf-8
"""
General apartment entity that contains apartment information.
"""
from model.property_info import PropertyInfo


class ApartmentInfo:
    def __init__(self, property_info: PropertyInfo, pricing: int, square_footage: int):
        self._property_info: PropertyInfo = property_info
        self._pricing: int = pricing
        self._square_footage: int = square_footage

    def __str__(self):
        return "\n<apt_name:{}\napt_url:{}\npricing:{}\nsquare_footage:{}>\n\n".format(
            self._property_info.get_property_name(), self._property_info.get_property_url(), self._pricing,
            self._square_footage)
