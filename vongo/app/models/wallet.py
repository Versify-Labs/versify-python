from typing import Any, Union

from app.core.pywallet import create_wallet
from pydantic import Field, root_validator

from .base import Base
from .enums import WalletType
from .factory import current_timestamp, wallet_id


class Wallet(Base):
    id: str = Field(
        alias="_id",
        default_factory=wallet_id,
        description="Unique identifier for the wallet",
        example="ast_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Asset ID",
    )
    object: str = Field(
        default="wallet",
        description="The object type",
        example="wallet",
        title="Object Type",
    )
    address: str = Field(
        ...,
        description="The address of the wallet",
        example="0x0000000000000000000000000000000000000000",
        title="Address",
    )
    children: list[Any] = Field(
        default=[],
        description="The children of the wallet",
        example=["0x0000000000000000000000000000000000000000"],
        title="Children",
    )
    coin: str = Field(
        default="ETH",
        description="The coin the wallet is for",
        example="ETH",
        title="Coin",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the wallet was created",
        example=1601059200,
        title="Created Timestamp",
    )
    managed: bool = Field(
        default=False,
        description="Whether the wallet is managed by the platform",
        example=False,
        title="Managed",
    )
    metadata: dict = Field(
        default={}, description="Arbitrary metadata for the wallet", title="Metadata"
    )
    private_key: Union[str, None] = Field(
        default=None,
        description="The private key of the wallet",
        example="0x0000000000000000000000000000000000000000000000000000000000000000",
        title="Private Key",
    )
    public_key: str = Field(
        default=None,
        description="The public key of the wallet",
        example="0x0000000000000000000000000000000000000000",
        title="Public Key",
    )
    seed: str = Field(
        default=None,
        description="The seed phrase used to generate the wallet",
        example="seed phrase",
        title="Seed Phrase",
    )
    type: WalletType = Field(
        default=WalletType.ETHEREUM,
        description="The type of the wallet",
        example="ethereum",
        title="Wallet Type",
    )
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the wallet was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )
    wif: Union[str, None] = Field(
        default=None,
        description="The wallet import format of the wallet",
        example="0x0000000000000000000000000000000000000000000000000000000000000000",
        title="Wallet Import Format",
    )
    xprivate_key: Union[str, None] = Field(
        default=None,
        description="The extended private key of the wallet",
        example="0x0000000000000000000000000000000000000000000000000000000000000000",
        title="Extended Private Key",
    )
    xpublic_key: Union[str, None] = Field(
        default=None,
        description="The extended public key of the wallet",
        example="0x0000000000000000000000000000000000000000",
        title="Extended Public Key",
    )

    @root_validator(pre=True)
    def default_values(cls, values):
        new_wallet = create_wallet()
        values.update(new_wallet)
        return values
