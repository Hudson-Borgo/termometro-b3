from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from termometro_b3.collectors.base import BaseCollector
from termometro_b3.models import NewsArticle


class InfoMoneyCollector(BaseCollector):
    # URL principal usada para buscar as notícias.
    BASE_URL = "https://www.infomoney.com.br/"

    # Seções que consideramos relevantes para o Termômetro B3.
    ALLOWED_SECTIONS = {
        "mercados",
        "economia",
        "politica",
        "business",
        "mundo",
    }

    def __init__(self, client: httpx.Client | None = None) -> None:
        # Permitir a injeção do client facilita os testes sem acessar a internet.
        self.client = client or httpx.Client(timeout=10.0)

    def collect(self) -> list[NewsArticle]:
        # Faz a requisição HTTP para a página inicial.
        response = self.client.get(self.BASE_URL)

        # Interrompe a execução caso o servidor retorne 4xx ou 5xx.
        response.raise_for_status()

        # O método collect cuida da rede.
        # O método _parse_articles cuida do HTML.
        return self._parse_articles(response.text)

    def _parse_articles(self, html: str) -> list[NewsArticle]:
        # Converte o HTML em uma estrutura navegável.
        soup = BeautifulSoup(html, "html.parser")

        articles: list[NewsArticle] = []

        # Procura links que possuam href.
        for link in soup.find_all("a", href=True):
            href = link["href"]
            title = link.get_text(" ", strip=True)

            # Links sem texto não podem gerar uma notícia útil.
            if not title:
                continue

            parsed_url = urlparse(href)

            # Ignora links externos.
            if parsed_url.netloc != "www.infomoney.com.br":
                continue

            path_parts = parsed_url.path.strip("/").split("/")

            # Precisamos de pelo menos seção + slug.
            if len(path_parts) < 2:
                continue

            # Ignora seções que não fazem parte do nosso monitoramento.
            if path_parts[0] not in self.ALLOWED_SECTIONS:
                continue

            articles.append(
                NewsArticle(
                    title=title,
                    url=href,
                    source="InfoMoney",
                )
            )

        return articles
