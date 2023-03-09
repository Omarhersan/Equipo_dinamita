from typing import Dict, List, Type

import requests
from bs4 import BeautifulSoup


class StandardIndustryClassificationElement:
    
    def __init__(self, title: str, sub_industries: List['StandardIndustryClassificationElement']):
        self.title = title
        self.sub_industries = sub_industries

    def __repr__(self):
        return f"{self.title} ({len(self.sub_industries)})"

    @classmethod
    def empty(cls, title: str) -> 'StandardIndustryClassificationElement':
        return cls(title=title, sub_industries=[])

    def include(self, industry: 'StandardIndustryClassificationElement'):
        self.sub_industries.append(industry)

    @property
    def alias(self) -> str:
        raise NotImplementedError

    @classmethod
    def from_dict(
            cls,
            payload: Dict,
            subclass: List[Type['StandardIndustryClassificationElement']]
    ) -> 'StandardIndustryClassificationElement':
        # Get the sub-industries (if any)
        sub_industries = payload.get("sub_industries", [])
        # If we don't have sub-industries, we can return an empty representation of the current class
        if not sub_industries:
            return cls.empty(title=payload.get("title"))
        # We should always have subclasses if we have sub_industries
        if not subclass:
            raise ValueError("Missing subclass references")
        # Get the next sub-industry class
        sub_industry_class, *others = subclass
        return cls(
            title=payload["title"],
            sub_industries=[
                sub_industry_class.from_dict(payload=sub_industry, subclass=others)
                for sub_industry in sub_industries
            ]
        )

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "level": self.alias,
            "sub_industries": [
                sub_industry.to_dict()
                for sub_industry in self.sub_industries
            ]
        }


class IndustryDivision(StandardIndustryClassificationElement):
    alias = "SIC Division"


class IndustryMajorGroup(StandardIndustryClassificationElement):
    alias = "SIC Major Group"

    @staticmethod
    def from_url(title: str, url: str) -> 'IndustryMajorGroup':
        response = requests.get(url)
        html = BeautifulSoup(response.text, "html.parser")
        return IndustryMajorGroup(
            title=title,
            sub_industries=[
                IndustryGroup(
                    title=element_strong.text,
                    sub_industries=[
                        Industry.empty(title=element_a.attrs.get("title"))
                        for element_a in html.find_all("a")
                        if element_a.attrs.get("href", "").startswith(f"/sic-manual/{industry_group_key}")
                    ]
                )
                for element_strong in html.find_all("strong")
                if element_strong.text.lower().startswith("industry")
                for industry_group_key in [element_strong.text.split(":")[0].split(" ")[-1]]
            ]
        )


class IndustryGroup(StandardIndustryClassificationElement):
    alias = "SIC Industry Group"


class Industry(StandardIndustryClassificationElement):
    alias = "SIC Industry"
