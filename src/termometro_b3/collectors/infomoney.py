import httpx

from termometro_b3.collectors.base import BaseCollector
from termometro_b3.models import NewsArticle


class InfoMoneyCollector(BaseCollector):
    BASE_URL = "https://www.infomoney.com.br/"

    def __init__(self, client: httpx.Client | None = None) -> None:
        self.client = client or httpx.Client(timeout=10.0)

    def collect(self) -> list[NewsArticle]:
        response = self.client.get(self.BASE_URL)
        response.raise_for_status()

        from bs4 import BeautifulSoup

        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all("a", href=True)

        candidates = []

        for link in links:
            href = link["href"]
            text = link.get_text(strip=True)

            if "infomoney.com.br" in href and text:
                candidates.append((text, href))

        print(f"Links encontrados: {len(links)}")
        print(f"Candidatos: {len(candidates)}")

        for text, href in candidates[:20]:
            print(text)
            print(href)
            print("-" * 80)

        return []
