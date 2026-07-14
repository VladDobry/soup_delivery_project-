import re

from django.http import Http404
from django.shortcuts import render
from django.db.utils import OperationalError, ProgrammingError

from .models import SetPrice, SoupMathRow, SoupPrice


SOUP_SLUGS = ("broth", "borsch", "solyanka", "ukha", "pumpkin")

FALLBACK_SOUP_PRICES_RUB = {
    SoupPrice.PriceGroup.DEFAULT: {
        SoupPrice.Volume.ONE_LITER: 1550,
        SoupPrice.Volume.ONE_AND_HALF_LITER: 2250,
        SoupPrice.Volume.TWO_LITERS: 2850,
    },
    SoupPrice.PriceGroup.UKHA: {
        SoupPrice.Volume.ONE_LITER: 1550,
        SoupPrice.Volume.ONE_AND_HALF_LITER: 2250,
        SoupPrice.Volume.TWO_LITERS: 2850,
    },
    SoupPrice.PriceGroup.BROTH: {
        SoupPrice.Volume.TWO_LITERS: 2850,
    },
}

FALLBACK_SET_PRICES_RUB = (
    {"title": "любой суп*", "price_rub": 750, "caption": "350мл"},
    {"title": "*Уха", "price_rub": 850, "caption": "350мл"},
)

FALLBACK_VOLUME_LABELS = {
    SoupPrice.Volume.ONE_LITER: "1000гр",
    SoupPrice.Volume.ONE_AND_HALF_LITER: "1500гр",
    SoupPrice.Volume.TWO_LITERS: "2000гр",
}

SOUP_MATH_VISUALS = {
    "jar_1l": {
        "src": "landing/img/feature-jar-solyanka-1000g.png",
        "class": "soup-math-jar soup-math-jar-small",
    },
    "jar_15l": {
        "src": "landing/img/feature-jar-pumpkin-1600g.png",
        "class": "soup-math-jar soup-math-jar-medium",
    },
    "jar_borsch_1l": {
        "src": "landing/img/feature-jar-borsch-2200g.png",
        "class": "soup-math-jar soup-math-jar-small",
    },
    "takeaway_035l": {
        "src": "landing/img/math-takeaway-bowl.png",
        "class": "soup-math-bowl",
    },
}

FALLBACK_SOUP_MATH_ROWS = (
    {
        "price_rub": 2850,
        "total_weight_label": "ЗА 2000 Г",
        "terms": (
            {"visual_type": "jar_1l", "volume_label": "1 л"},
            {"visual_type": "jar_1l", "volume_label": "1 л"},
        ),
    },
    {
        "price_rub": 3550,
        "total_weight_label": "ЗА 2500 Г",
        "terms": (
            {"visual_type": "jar_1l", "volume_label": "1 л"},
            {"visual_type": "jar_15l", "volume_label": "1,5 л"},
        ),
    },
    {
        "price_rub": 2550,
        "total_weight_label": "ЗА 1700 Г",
        "terms": (
            {"visual_type": "takeaway_035l", "volume_label": "0,35 л"},
            {"visual_type": "takeaway_035l", "volume_label": "0,35 л"},
            {"visual_type": "jar_borsch_1l", "volume_label": "1 л"},
        ),
    },
)

def format_soup_price(price_rub):
    return f"{price_rub} ₽"


def format_set_price(price_rub):
    return f"{price_rub}₽"


def format_math_price(price_rub):
    return f"{price_rub} ₽"


def format_text_volume_label(label):
    return re.sub(r"(?<=\d)(?=[^\d\s])", " ", label.strip())


def split_volume_label(label):
    text_label = format_text_volume_label(label)
    match = re.match(r"^(\S+)\s+(.+)$", text_label)
    if not match:
        return {
            "compact": label,
            "text": text_label,
            "amount": text_label,
            "unit": "",
        }

    return {
        "compact": label,
        "text": text_label,
        "amount": match.group(1),
        "unit": match.group(2),
    }


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
    volume_labels = {
        volume: split_volume_label(label)
        for volume, label in FALLBACK_VOLUME_LABELS.items()
    }

    try:
        prices = list(SoupPrice.objects.all())
    except (OperationalError, ProgrammingError):
        prices = []

    rows_by_group = {}
    for price in prices:
        rows_by_group.setdefault(price.price_group, []).append(price)
        if price.price_group == SoupPrice.PriceGroup.DEFAULT and price.volume_label:
            volume_labels[price.volume] = split_volume_label(price.volume_label)

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
        "soup_volume_1l": volume_labels[SoupPrice.Volume.ONE_LITER],
        "soup_volume_15l": volume_labels[SoupPrice.Volume.ONE_AND_HALF_LITER],
        "soup_volume_2l": volume_labels[SoupPrice.Volume.TWO_LITERS],
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


def hydrate_soup_math_terms(terms):
    hydrated_terms = []

    for term in terms:
        visual_type = term["visual_type"]
        visual = SOUP_MATH_VISUALS.get(visual_type, SOUP_MATH_VISUALS["jar_1l"])
        hydrated_terms.append(
            {
                "volume_label": term["volume_label"],
                "visual_type": visual_type,
                "visual_src": visual["src"],
                "visual_class": visual["class"],
                "is_bowl": visual["class"] == "soup-math-bowl",
            }
        )

    return hydrated_terms


def format_soup_math_row(row):
    return {
        "price": format_math_price(row["price_rub"]),
        "total_weight_label": row["total_weight_label"],
        "terms": hydrate_soup_math_terms(row["terms"]),
        "is_mix": len(row["terms"]) > 2,
    }


def get_soup_math_rows():
    try:
        rows = list(
            SoupMathRow.objects.filter(is_active=True)
            .prefetch_related("terms")
            .order_by("sort_order", "id")
        )
    except (OperationalError, ProgrammingError):
        rows = []

    if not rows:
        return [format_soup_math_row(row) for row in FALLBACK_SOUP_MATH_ROWS]

    return [
        format_soup_math_row(
            {
                "price_rub": row.price_rub,
                "total_weight_label": row.total_weight_label,
                "terms": [
                    {
                        "visual_type": term.visual_type,
                        "volume_label": term.volume_label,
                    }
                    for term in row.terms.all()
                ],
            }
        )
        for row in rows
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
            "soup_math_rows": get_soup_math_rows(),
        },
    )
