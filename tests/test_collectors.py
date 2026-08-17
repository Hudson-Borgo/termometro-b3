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
