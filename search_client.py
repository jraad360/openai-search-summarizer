import requests
from bs4 import BeautifulSoup
import json
from collections import namedtuple

GOOGLE_SEARCH_URL = "https://www.google.com/search"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'
}

SearchResult = namedtuple(
    'SearchResult', ['title', 'link', 'snippet', 'content'])


class SearchClient:
    def __init__(self) -> None:
        pass

    def __extract_information(self, link) -> str:
        response = requests.get(link, headers=HEADERS, timeout=30)
        if response.status_code != 200:
            return json.dumps({"error": response.status_code})

        soup = BeautifulSoup(response.text, 'lxml')
        return soup.get_text()

    def search(self, query: str) -> str:
        params = {
            'q': query,
            'gl': 'us',
            'hl': 'en'
        }
        response = requests.get(
            GOOGLE_SEARCH_URL, headers=HEADERS, params=params, timeout=30)
        if response.status_code != 200:
            return json.dumps({"error": response.status_code})

        soup = BeautifulSoup(response.text, 'lxml')
        results = []

        for result in soup.select('.tF2Cxc'):
            title = result.select_one('.DKV0Md').text
            link = result.select_one('.yuRUbf a')['href']
            try:
                # found the following classes in the corresponding divs: VwiC3b yXK7lf p4wth r025kc hJNv6b Hdw6tb
                snippet = result.select_one('#rso .VwiC3b').text
            except:
                snippet = None

            results.append(SearchResult(
                title=title, link=link, snippet=snippet, content=self.__extract_information(link)))

        return results
