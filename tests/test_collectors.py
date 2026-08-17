import httpx
import pytest

from termometro_b3.collectors.base import BaseCollector
from termometro_b3.collectors.infomoney import InfoMoneyCollector


def test_base_collector_cannot_be_instantiated():
    with pytest.raises(TypeError):
        BaseCollector()


def test_infomoney_collector_requests_homepage():
    def handler(request: httpx.Request) -> httpx.Response:
        assert str(request.url) == "https://www.infomoney.com.br/"

        return httpx.Response(
            status_code=200,
            text="<html></html>",
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as client:
        collector = InfoMoneyCollector(client=client)

        articles = collector.collect()

    assert articles == []


def test_infomoney_collector_raises_for_http_error():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=500,
            request=request,
        )

    transport = httpx.MockTransport(handler)

    with httpx.Client(transport=transport) as client:
        collector = InfoMoneyCollector(client=client)

        with pytest.raises(httpx.HTTPStatusError):
            collector.collect()


def test_infomoney_collector_parses_valid_article():
    # HTML controlado simulando uma notícia real do InfoMoney.
    html = """
    <html>
        <body>
            <a href="https://www.infomoney.com.br/mercados/ibovespa-sobe/">
                Ibovespa sobe com apoio dos bancos
            </a>
        </body>
    </html>
    """

    # Criamos o collector sem precisar acessar a internet.
    collector = InfoMoneyCollector()

    # Testamos diretamente a parte responsável pelo parsing.
    articles = collector._parse_articles(html)

    # Esperamos exatamente uma notícia válida.
    assert len(articles) == 1

    article = articles[0]

    # Validamos se os dados foram normalizados corretamente.
    assert article.title == "Ibovespa sobe com apoio dos bancos"
    assert article.source == "InfoMoney"


def test_infomoney_collector_ignores_irrelevant_links():
    # HTML contendo links que não devem virar notícias.
    html = """
    <html>
        <body>
            <a href="https://www.infomoney.com.br/newsletters/">
                Newsletters
            </a>

            <a href="https://www.infomoney.com.br/mercados/">
                Mercados
            </a>

            <a href="https://www.google.com/">
                Google
            </a>
        </body>
    </html>
    """

    collector = InfoMoneyCollector()

    articles = collector._parse_articles(html)

    # Nenhum desses links representa uma notícia.
    assert articles == []
