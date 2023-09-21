import re

from app.enums import URLKey, URLPattern


class ArticleValidator():

    _url: str
    _key: str

    def __init__(self, url: str, key: str) -> None:
        self._url = url
        self._key = key

    def build_url(self, base_url: str) -> str:
        new_url = f"{base_url}{self._url}"
        self._url = new_url
        return new_url

    @property
    def is_valid(self) -> bool:
        return (
            self.is_valid_url and
            (
                self.is_id_url or
                self.is_html or
                self.is_hyphen_url
            )
        )

    @property
    def is_id_url(self) -> bool:
        return bool(
            re.search(
                URLPattern.ID.value,
                self._url
            )
        )

    @property
    def is_hyphen_url(self) -> bool:
        return bool(
            re.search(
                URLPattern.HYPHEN.value,
                self._url
            )
        )

    @property
    def is_html(self) -> bool:
        return (
            self._url.endswith(URLKey.HTML.value) or
            self._url.endswith(URLKey.HTM.value)
        ) 

    @property
    def is_valid_url(self) -> bool:
        return self._key.lower() in self._url.lower()

    @property
    def is_sliced_url(self) -> bool:
        return self._url.startswith(URLKey.BACKSLASH.value)

    @property
    def is_social_media_url(self) -> bool:
        return (
            self._url.startswith(URLKey.MAIL.value) or
            self._url.startswith(URLKey.TWITTER.value)
        )