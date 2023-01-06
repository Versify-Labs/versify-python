from pydantic import Field

from .base import BaseCreate, BaseDoc, BaseUpdate
from .enums import ClaimStatus
from .factory import claim_id


class Claim(BaseDoc):
    """A claim document in the database."""

    __db__ = "Dev"
    __collection__ = "Claims"

    id: str = Field(
        alias="_id",
        default_factory=claim_id,
        description="Unique identifier for the claim",
        example="clm_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="User ID",
    )
    object: str = Field(
        default="claim",
        description='The object type. Always "claim"',
        example="claim",
        title="Object Type",
    )
    account: str = Field(
        ...,
        description="The account the claim belongs to",
        example="act_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Account ID",
    )
    asset: str = Field(
        ...,
        description="The asset being claimed",
        example="asset_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Asset ID",
    )
    code: str = Field(
        ...,
        description="The code used to submit the claim.",
        example="ABC123",
        title="Code",
    )
    quantity: int = Field(
        default=1,
        description="The number of assets being claimed",
        example=1,
        title="Quantity",
    )
    status: str = Field(
        default=ClaimStatus.REQUESTED,
        description="The status of the claim",
        example=ClaimStatus.REQUESTED,
        title="Status",
    )


class ClaimCreate(BaseCreate):
    """A claim create request body."""

    pass


class ClaimUpdate(BaseUpdate):
    """A claim update request body."""

    pass
