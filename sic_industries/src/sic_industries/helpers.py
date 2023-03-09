import json
import posixpath
from typing import List, Optional

import requests
from bs4 import BeautifulSoup


from .models import (
    IndustryDivision,
    IndustryMajorGroup,
    IndustryGroup,
    Industry,
    StandardIndustryClassificationElement,
)

from .settings import (
    DEFAULT_SIC_INDUSTRIES_URL,
)


class SICHelper(StandardIndustryClassificationElement):
    alias = "SIC Top Level"

    def __init__(self, sub_industries: List[IndustryDivision], title: Optional[str] = None):
        super().__init__(title=title or "Standard Industry Classification", sub_industries=sub_industries)

    @staticmethod
    def from_file(filename: str) -> 'SICHelper':
        with open(filename, "r") as file:
            content = file.read()
            payload = json.loads(content)
        return SICHelper.from_dict(
            payload=payload,
            subclass=[
                IndustryDivision,
                IndustryMajorGroup,
                IndustryGroup,
                Industry,
            ]
        )

    @classmethod
    def from_url(cls, url: Optional[str] = None) -> 'SICHelper':
        url = url or DEFAULT_SIC_INDUSTRIES_URL
        response = requests.get(url)
        if not response.ok:
            pass
        html = BeautifulSoup(response.text, "html.parser")
        divisions = []
        for element in html.find_all("a"):
            *_, key = element.attrs.get("href", "").split("/")
            title = element.attrs.get("title", "")
            if key.startswith("division"):
                divisions.append(IndustryDivision.empty(title=title))
            if key.startswith("major-group"):
                url_major_group = posixpath.join(url, key)
                divisions[-1].include(
                    IndustryMajorGroup.from_url(
                        title=title,
                        url=url_major_group
                    )
                )

        return cls(sub_industries=divisions)
