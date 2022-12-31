from typing import Any, Dict, Optional

from pydantic import Field

from .base import Base
from .enums import ClaimStatus
from .factory import claim_id, current_timestamp, user_id


class Claim(Base):
    id: str = Field(
        alias="_id",
        default_factory=claim_id,
        description="Unique identifier for the claim",
        example="claim_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="User ID",
    )
    object: str = Field(
        default="claim",
        description='The object type. Always "claim"',
        example="claim",
        title="Object Type",
    )
    asset: str = Field(
        ...,
        description="The asset being claimed",
        example="asset_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Asset ID",
    )
    created: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the claim was created",
        example=16,
    )
    code: str = Field(
        ..., description="The code of the claim", example="ABC123", title="Code"
    )
    contact: Optional[str] = Field(
        default=None,
        description="The contact the claim is for",
        example="contact_5f9f1c5b0b9b4b0b9c1c5b0b",
        title="Contact ID",
    )
    metadata: Dict[str, Any] = Field(
        default={},
        description="Arbitrary metadata associated with the claim",
        example={"key": "value"},
        title="Metadata",
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
    updated: int = Field(
        default_factory=current_timestamp,
        description="The timestamp when the user was last updated",
        example=1601059200,
        title="Updated Timestamp",
    )
