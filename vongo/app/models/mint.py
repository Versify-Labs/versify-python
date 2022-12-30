from typing import Any, Dict, Optional

from pydantic import EmailStr, Field

from .base import Base
from .enums import MintStatus
from .factory import current_timestamp, mint_id


class Mint(Base):
    id: str = Field(
        alias="_id",
        default_factory=mint_id,
        description='Unique identifier for the mint',
        example='mint_5f9f1c5b0b9b4b0b9c1c5b0b',
        title='Mint ID'
    )
    object: str = Field(
        default='mint',
        description='The object type. Always "mint"',
        example='mint',
        title='Object Type'
    )
    asset: str = Field(
        ...,
        description='The asset the mint is for',
        example='asset_5f9f1c5b0b9b4b0b9c1c5b0b',
        title='Asset ID'
    )
    created: int = Field(
        default_factory=current_timestamp,
        description='The timestamp when the mint was created',
        example=1601059200,
        title='Created Timestamp'
    )
    contact: Optional[str] = Field(
        default=None,
        description='The contact the mint is for',
        example='contact_5f9f1c5b0b9b4b0b9c1c5b0b',
        title='Contact ID'
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description='The email the mint is for',
        title='Email'
    )
    journey: Optional[str] = Field(
        default=None,
        description='The journey the mint is for',
        title='Journey ID'
    )
    journey_run: Optional[str] = Field(
        default=None,
        description='The journey run the mint is for',
        title='Journey Run ID'
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description='Arbitrary metadata associated with the mint',
        example={'key': 'value'},
        title='Metadata'
    )
    quantity: int = Field(
        default=1,
        description='The quantity of the mint',
        example=1,
        title='Quantity'
    )
    signature: Optional[str] = Field(
        default=None,
        description='The signature for the mint',
        example='signature',
        title='Signature'
    )
    status: MintStatus = Field(
        default=MintStatus.RESERVED,
        description='The status of the mint',
        example=MintStatus.RESERVED,
        title='Status'
    )
    transaction: Optional[str] = Field(
        default=None,
        description='The transaction the mint is for',
        title='Transaction ID'
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description='The timestamp when the mint was last updated',
        example=1601059200,
        title='Updated Timestamp'
    )
    wallet_address: Optional[str] = Field(
        default=None,
        description='The wallet address the mint is for',
        title='Wallet Address'
    )
