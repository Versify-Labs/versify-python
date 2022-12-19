from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from ._base import BaseAccountModel


class ReportParameters(BaseModel):
    category: Optional[str]
    columns: List[str] = []
    interval_end: Optional[int]
    interval_start: Optional[int]
    timezone: Optional[str]


class ReportStatus(str, Enum):
    PENDING = "pending"
    COMPLETE = "complete"
    FAILED = "failed"


class Report(BaseAccountModel):
    object: str = 'report'
    error: Optional[str]
    parameters: Optional[dict] = {}
    report_type: str
    result: Optional[dict] = {}
    status: Optional[ReportStatus] = ReportStatus.PENDING
    succeeded_at: Optional[int]
