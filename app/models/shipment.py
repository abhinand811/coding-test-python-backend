from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, field_validator


class ShipmentStatus(str, Enum):
    pending = "pending"
    in_transit = "in_transit"
    delivered = "delivered"
    cancelled = "cancelled"


class ShipmentCreate(BaseModel):
    origin: str
    destination: str
    cargo_type: str
    weight_kg: float

    @field_validator("weight_kg")
    @classmethod
    def weight_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("weight_kg must be greater than 0")
        return v


class ShipmentOut(BaseModel):
    id: str
    origin: str
    destination: str
    cargo_type: str
    weight_kg: float
    status: ShipmentStatus
    created_at: datetime


class StatusUpdate(BaseModel):
    status: ShipmentStatus


class ShipmentSummary(BaseModel):
    pending: int
    in_transit: int
    delivered: int
    cancelled: int
    total: int
