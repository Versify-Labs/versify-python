from typing import Union

from pydantic import EmailStr, Field

from .base import BaseCreate, BaseDoc, BaseUpdate
from .enums import MintStatus
from .factory import mint_id


class Mint(BaseDoc):
    """A mint document in the database."""

    __db__ = "Dev"
    __collection__ = "Accounts"

    id: str = Field(
        alias="_id",
        default_factory=mint_id,
        description="Unique identifier for the mint",
        example="mint_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Mint ID",
    )
    object: str = Field(
        default="mint",
        description='The object type. Always "mint"',
        example="mint",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the mint belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    asset: str = Field(
        ...,
        description="The asset the mint is for",
        example="asset_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Asset ID",
    )
    contact: Union[str, None] = Field(
        default=None,
        description="The contact the mint is for",
        example="contact_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Contact ID",
    )
    email: Union[EmailStr, None] = Field(
        default=None,
        description="The email address of the contact the mint is for.",
        title="Email",
    )
    journey: Union[str, None] = Field(
        default=None,
        description="The ID of the journey the mint is for.",
        title="Journey ID",
    )
    run: Union[str, None] = Field(
        default=None,
        description="The journey run the mint is for",
        title="Journey Run ID",
    )
    quantity: int = Field(
        default=1,
        description="The quantity of the asset being minted",
        example=1,
        title="Quantity",
    )
    signature: Union[str, None] = Field(
        default=None,
        description="The signature for the mint",
        example="signature",
        title="Signature",
    )
    status: MintStatus = Field(
        default=MintStatus.RESERVED,
        description="The status of the mint",
        example=MintStatus.RESERVED,
        title="Status",
    )
    transaction: Union[str, None] = Field(
        default=None,
        description="The transaction the mint is for",
        title="Transaction ID",
    )
    wallet_address: Union[str, None] = Field(
        default=None,
        description="The wallet address the mint is for",
        title="Wallet Address",
    )


class MintCreate(BaseCreate):
    """A mint create request body."""

    pass


class MintUpdate(BaseUpdate):
    """A mint update request body."""

    pass
