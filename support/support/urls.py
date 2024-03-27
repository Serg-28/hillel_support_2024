"""
URL configuration for support project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import json
import random
import string
from typing import Callable

import httpx
from django.contrib import admin  # noqa
from django.http import HttpRequest, HttpResponse, JsonResponse  # noqa
from django.urls import path

create_random_string: Callable[[int], str] = lambda size: "".join(  # noqa
    [random.choice(string.ascii_letters) for i in range(size)]  # noqa
)  # noqa


def generate_article_idea(request: HttpRequest) -> JsonResponse:
    content = {
        "title": create_random_string(size=10),
        "description": create_random_string(size=20),
    }
    return JsonResponse(content)


async def get_current_market_state(request: HttpRequest):
    url = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=USD&to_currency=JPY&apikey=XSN17SDSA5RAM5W2"  # noqa
    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url)
    rate: str = response.json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"]  # noqa
    return JsonResponse({"rate": rate})


async def get_exchange_rate(request: HttpRequest) -> HttpResponse:
    post_data = json.loads(request.body)
    source = post_data.get("source")
    destination = post_data.get("destination")

    url = f"https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={source}&to_currency={destination}&apikey=XSN17SDSA5RAM5W2"  # noqa

    async with httpx.AsyncClient() as client:
        response: httpx.Response = await client.get(url=url)
    rate: str = response.json()["Realtime Currency Exchange Rate"]["5. Exchange Rate"]  # noqa

    result = f"Exchange rate for {source} to {destination} is {rate}"
    return HttpResponse(result)


urlpatterns = [
    path(route="generate-article", view=generate_article_idea),
    path(route="market", view=get_current_market_state),
    path(route="exchange-rate", view=get_exchange_rate),
]
