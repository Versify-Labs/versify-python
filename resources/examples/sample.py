import versify

versify.api_key = "sk_123"

# Airdrops
airdrop = versify.Airdrop.create(
    product="prod_123",
    recipients={"segment": "tag-$eq-Customer"}
)

versify.Airdrop.send(
    airdrop['id']
)

# Audience
versify.Contact.create(
    email="jane@example.com",
    first_name="Jane",
    last_name="Doe",
    tags=["Customer"]
)

# Mint Links
versify.MintLink.create(
    active=True,
    product="prod_123"
)

# Studio
product = versify.Product.create(
    name="T-shirt",
    description="Digital t-shirt",
    image="https://cdn.versifylabs.com/123"
)
