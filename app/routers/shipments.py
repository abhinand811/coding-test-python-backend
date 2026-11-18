from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, HTTPException

from app.exceptions import ShipmentTerminalStateError

from app.models.shipment import ShipmentCreate, ShipmentOut, ShipmentStatus, StatusUpdate, ShipmentSummary
from app.services import shipment_service

router = APIRouter(prefix="/shipments", tags=["shipments"])


@router.post("", response_model=ShipmentOut, status_code=201)
async def create_shipment(payload: ShipmentCreate) -> ShipmentOut:
    return shipment_service.create_shipment(payload)


@router.get("", response_model=list[ShipmentOut])
async def list_shipments(status: Optional[ShipmentStatus] = None) -> list[ShipmentOut]:
    return shipment_service.list_shipments(status)


@router.get("/summary", response_model=ShipmentSummary)
async def get_summary() -> ShipmentSummary:
    return shipment_service.get_summary()


@router.get("/{shipment_id}", response_model=ShipmentOut)
async def get_shipment(shipment_id: str) -> ShipmentOut:
    shipment = shipment_service.get_shipment(shipment_id)
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@router.patch("/{shipment_id}/status", response_model=ShipmentOut)
async def update_status(shipment_id: str, payload: StatusUpdate) -> ShipmentOut:
    try:
        shipment = shipment_service.update_status(shipment_id, payload.status)
    except ShipmentTerminalStateError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    if shipment is None:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipment


@router.delete("/{shipment_id}", status_code=204)
async def delete_shipment(shipment_id: str) -> None:
    deleted = shipment_service.delete_shipment(shipment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Shipment not found")
