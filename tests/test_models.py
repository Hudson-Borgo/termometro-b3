from termometro_b3.models import NewsArticle


def test_create_news_article():
    article = NewsArticle(
        title="Ibovespa sobe com apoio de bancos",
        url="https://www.infomoney.com.br/mercados/exemplo",
        source="InfoMoney",
    )

    assert article.title == "Ibovespa sobe com apoio de bancos"
    assert article.source == "InfoMoney"
