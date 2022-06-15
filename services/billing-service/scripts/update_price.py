import stripe

stripe.api_key = "SECRET"

stripe.Price.modify(
    "price_1LAPEXFClClGmATOdfgIc14R",
    lookup_key='basic'
)

stripe.Price.modify(
    "price_1LAPFgFClClGmATOSIXFc5TO",
    lookup_key='growth'
)

stripe.Price.modify(
    "price_1LAPFtFClClGmATOf4fwIB9J",
    lookup_key='enterprise'
)
