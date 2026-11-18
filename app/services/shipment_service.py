from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from app.exceptions import ShipmentTerminalStateError
from app.models.shipment import ShipmentCreate, ShipmentOut, ShipmentStatus, ShipmentSummary

# In-memory store: id → ShipmentOut
_shipments: dict[str, ShipmentOut] = {}


def create_shipment(payload: ShipmentCreate) -> ShipmentOut:
    shipment = ShipmentOut(
        id=str(uuid.uuid4()),
        origin=payload.origin,
        destination=payload.destination,
        cargo_type=payload.cargo_type,
        weight_kg=payload.weight_kg,
        status=ShipmentStatus.pending,
        created_at=datetime.now(timezone.utc),
    )
    _shipments[shipment.id] = shipment
    return shipment


def list_shipments(status: Optional[ShipmentStatus] = None) -> list[ShipmentOut]:
    if status is None:
        return list(_shipments.values())
    return [s for s in _shipments.values() if s.status == status]


def get_shipment(shipment_id: str) -> Optional[ShipmentOut]:
    return _shipments.get(shipment_id)


_TERMINAL_STATUSES = {ShipmentStatus.delivered, ShipmentStatus.cancelled}


def update_status(shipment_id: str, new_status: ShipmentStatus) -> Optional[ShipmentOut]:
    shipment = _shipments.get(shipment_id)
    if shipment is None:
        return None
    if shipment.status in _TERMINAL_STATUSES:
        raise ShipmentTerminalStateError(shipment.status.value)
    updated = shipment.model_copy(update={"status": new_status})
    _shipments[shipment_id] = updated
    return updated


def delete_shipment(shipment_id: str) -> bool:
    if shipment_id not in _shipments:
        return False
    del _shipments[shipment_id]
    return True


def get_summary() -> ShipmentSummary:
    all_shipments = list(_shipments.values())
    counts = {status: 0 for status in ShipmentStatus}
    for shipment in all_shipments:
        counts[shipment.status] += 1
    return ShipmentSummary(
        pending=counts[ShipmentStatus.pending],
        in_transit=counts[ShipmentStatus.in_transit],
        delivered=counts[ShipmentStatus.delivered],
        cancelled=counts[ShipmentStatus.cancelled],
        total=len(all_shipments),
    )


def clear_all() -> None:
    """Test helper — wipe the store between test runs."""
    _shipments.clear()
