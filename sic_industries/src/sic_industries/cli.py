import json
import requests
from typing import Dict, List
from difflib import SequenceMatcher
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
        file = SICHelper.from_file(filename)
        return file

    def search(self, filename: str, pattern: str, exact: bool = False) -> List:
        loaded_file = self.load(filename=filename)
        print(f'The file: {loaded_file.title} has been successfully loaded')
        if exact:
            '''
            Implementación de lo más horrible que he hecho en mi vida, pero jala
            '''
            results = []
            for sub_industry in loaded_file.sub_industries:
                if self.search_e(str(sub_industry), pattern):
                    results.append(sub_industry)
                for major_group in sub_industry.sub_industries:
                    if self.search_e(str(major_group), pattern):
                        results.append(major_group)
                    for industry_group in major_group.sub_industries:
                        if self.search_e(str(industry_group), pattern):
                            results.append(industry_group)
                        for industry in industry_group.sub_industries:
                            if self.search_e(str(industry), pattern):
                                results.append(industry)
            return results
        else:
            results = []
            for sub_industry in loaded_file.sub_industries:
                if self.search_s(str(sub_industry), pattern):
                    print('its working')
                    results.append(sub_industry)
                for major_group in sub_industry.sub_industries:
                    if self.search_s(str(major_group), pattern):
                        results.append(major_group)
                    for industry_group in major_group.sub_industries:
                        if self.search_s(str(industry_group), pattern):
                            results.append(industry_group)
                        for industry in industry_group.sub_industries:
                            if self.search_s(str(industry), pattern):
                                results.append(industry)

            return results



    # aquí estan

    def search_e(self, title: str, pattern: str):
        return pattern in title
    def search_s(self,title: str,pattern: str) -> bool:
        similarity_ratio = SequenceMatcher(None, title , pattern).ratio()
        coincidence = False
        if similarity_ratio >0.4:
            coincidence = True
        return coincidence


# Codigo para python whl python setup.py bdist_wheel
