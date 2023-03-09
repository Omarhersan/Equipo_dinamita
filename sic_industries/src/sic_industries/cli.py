import json
import requests
from typing import Dict

from .helpers import SICHelper
from .settings import (
    DEFAULT_SIC_INDUSTRIES_URL,
)


class CLI:

    def url(self, is_accessible: bool = False) -> Dict:
        payload = {
            "url": DEFAULT_SIC_INDUSTRIES_URL
        }
        if is_accessible:
            response = requests.get(DEFAULT_SIC_INDUSTRIES_URL)
            payload["accessible"] = response.ok
        return payload

    def show(self):
        sic_helper = SICHelper.from_url(url=DEFAULT_SIC_INDUSTRIES_URL)
        print(json.dumps(sic_helper.to_dict(), indent=4))

    def download(self, filename: str):
        with open(filename, "w") as file:
            sic_helper = SICHelper.from_url(url=DEFAULT_SIC_INDUSTRIES_URL)
            payload = sic_helper.to_dict()
            content = json.dumps(payload, indent=4)
            file.write(content)

    def load(self, filename: str) -> str:
        SICHelper.from_file(filename)
        return "File can be correctly loaded into memory and parsed by our data models."

    def search(self, filename: str, string_to_search: str, similarity: bool = False) -> str:
        loaded_file = SICHelper.from_file(filename=filename)
        print(f'The file: {loaded_file.title} has been successfully loaded')
        results = []
        for sub_industry in loaded_file.sub_industries:
            #if string_to_search in sub_industry:
            #    results.append(sub_industry)
            print(sub_industry.sub_industries)



        pass
