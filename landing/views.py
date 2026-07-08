from django.http import Http404
from django.shortcuts import render
from django.db.utils import OperationalError, ProgrammingError

from .models import SetPrice, SoupPrice


SOUP_SLUGS = ("borsch", "solyanka", "ukha", "pumpkin", "broth")

FALLBACK_SOUP_PRICES_RUB = {
    SoupPrice.PriceGroup.DEFAULT: {
        SoupPrice.Volume.ONE_LITER: 2500,
        SoupPrice.Volume.ONE_AND_HALF_LITER: 3750,
        SoupPrice.Volume.TWO_LITERS: 4500,
    },
    SoupPrice.PriceGroup.UKHA: {
        SoupPrice.Volume.ONE_LITER: 3000,
        SoupPrice.Volume.ONE_AND_HALF_LITER: 4250,
        SoupPrice.Volume.TWO_LITERS: 5000,
    },
    SoupPrice.PriceGroup.BROTH: {
        SoupPrice.Volume.TWO_LITERS: 2500,
    },
}

FALLBACK_SET_PRICES_RUB = (
    {"title": "350мл", "price_rub": 750, "caption": "за порцию"},
    {"title": "Уха", "price_rub": 850, "caption": "за порцию"},
)


def format_soup_price(price_rub):
    return f"{price_rub} ₽"


def format_set_price(price_rub):
    return f"{price_rub}₽"


def format_soup_prices(price_data):
    return {
        price_group: {
            volume: format_soup_price(price_rub)
            for volume, price_rub in volume_prices.items()
        }
        for price_group, volume_prices in price_data.items()
    }


def get_soup_price_context():
    fallback_prices = format_soup_prices(FALLBACK_SOUP_PRICES_RUB)

    try:
        prices = list(SoupPrice.objects.all())
    except (OperationalError, ProgrammingError):
        prices = []

    rows_by_group = {}
    for price in prices:
        rows_by_group.setdefault(price.price_group, []).append(price)

    prices_by_group = {}
    for price_group, fallback_group_prices in fallback_prices.items():
        group_rows = rows_by_group.get(price_group, [])
        if not group_rows:
            prices_by_group[price_group] = fallback_group_prices
            continue

        prices_by_group[price_group] = {
            price.volume: format_soup_price(price.price_rub)
            for price in sorted(group_rows, key=lambda item: (item.sort_order, item.volume))
            if price.is_active
        }

    return {
        "default_soup_prices": prices_by_group[SoupPrice.PriceGroup.DEFAULT],
        "soup_price_overrides": {
            SoupPrice.PriceGroup.UKHA: prices_by_group[SoupPrice.PriceGroup.UKHA],
            SoupPrice.PriceGroup.BROTH: prices_by_group[SoupPrice.PriceGroup.BROTH],
        },
    }


def get_set_prices():
    try:
        set_prices = list(SetPrice.objects.all())
    except (OperationalError, ProgrammingError):
        set_prices = []

    if set_prices:
        return [
            {
                "title": price.title,
                "price": format_set_price(price.price_rub),
                "caption": price.caption,
            }
            for price in set_prices
            if price.is_active
        ]

    return [
        {
            "title": price["title"],
            "price": format_set_price(price["price_rub"]),
            "caption": price["caption"],
        }
        for price in FALLBACK_SET_PRICES_RUB
    ]


def index(request, soup_slug=None):
    if soup_slug is not None and soup_slug not in SOUP_SLUGS:
        raise Http404("Soup not found")

    soup_price_context = get_soup_price_context()
    default_soup_prices = soup_price_context["default_soup_prices"]

    return render(
        request,
        "landing/index.html",
        {
            "initial_soup_slug": soup_slug or "",
            **soup_price_context,
            "default_soup_price_1l": default_soup_prices.get(SoupPrice.Volume.ONE_LITER, ""),
            "default_soup_price_15l": default_soup_prices.get(
                SoupPrice.Volume.ONE_AND_HALF_LITER,
                "",
            ),
            "default_soup_price_2l": default_soup_prices.get(SoupPrice.Volume.TWO_LITERS, ""),
            "set_prices": get_set_prices(),
        },
    )
