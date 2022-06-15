import stripe

stripe.api_key = "SECRET"

basic_product = stripe.Product.create(
    name='Basic',
    description='Basic organization plan'
)
print(basic_product)

basic_price = stripe.Price.create(
    billing_scheme='tiered',
    currency='usd',
    lookup_key='basic',
    product=basic_product['id'],
    recurring={
        'usage_type': 'metered',
        'interval': 'month'
    },
    tiers=[
        {
            'flat_amount': 0,
            'unit_amount_decimal': 0,
            'up_to': 25
        },
        {
            'flat_amount': 0,
            'unit_amount_decimal': 100,
            'up_to': 'inf'
        },
    ],
    tiers_mode='graduated',
    expand=['tiers']
)
print(basic_price)

growth_product = stripe.Product.create(
    name='Growth',
    description='Growth organization plan'
)
print(growth_product)

growth_price = stripe.Price.create(
    billing_scheme='tiered',
    currency='usd',
    lookup_key='growth',
    product=growth_product['id'],
    recurring={
        'usage_type': 'metered',
        'interval': 'month'
    },
    tiers=[
        {
            'flat_amount': 9900,
            'unit_amount_decimal': 0,
            'up_to': 1000
        },
        {
            'flat_amount': 0,
            'unit_amount_decimal': 75,
            'up_to': 'inf'
        },
    ],
    tiers_mode='graduated',
    expand=['tiers']
)
print(growth_price)

enterprise_product = stripe.Product.create(
    name='Enterprise',
    description='Enterprise organization plan'
)
print(enterprise_product)

enterprise_price = stripe.Price.create(
    billing_scheme='tiered',
    currency='usd',
    lookup_key='enteprise',
    product=enterprise_product['id'],
    recurring={
        'usage_type': 'metered',
        'interval': 'month'
    },
    tiers=[
        {
            'flat_amount': 99900,
            'unit_amount_decimal': 0,
            'up_to': 1000
        },
        {
            'flat_amount': 0,
            'unit_amount_decimal': 50,
            'up_to': 'inf'
        },
    ],
    tiers_mode='graduated',
    expand=['tiers']
)
print(enterprise_price)
