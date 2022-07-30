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
collection = versify.Collection.create(
    name="Acme Digital Clothing",
    description="Digital clothes from the Acme Corp",
    image="https://cdn.versifylabs.com/123"
)

product = versify.Product.create(
    collection=collection['id'],
    name="T-shirt",
    description="Digital t-shirt withim the Acme Digital Clothing line",
    image="https://cdn.versifylabs.com/123"
)
