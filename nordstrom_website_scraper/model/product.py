class Product:
    def __init__(self, description: str, size: str, color: str, url: str):
        self._description: str = description
        self._size = size
        self._color = color
        self._url = url

    def get_description(self):
        return self._description

    def get_size(self):
        return self._size

    def get_color(self):
        return self._color

    def get_url(self):
        return self._url
