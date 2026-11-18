from __future__ import annotations

from app.models.shipment import ShipmentCreate, ShipmentStatus
from app.services import shipment_service

_SEED_DATA: list[dict] = [
    {
        "origin": "Kochi",
        "destination": "Dubai",
        "cargo_type": "Electronics",
        "weight_kg": 320.5,
    },
    {
        "origin": "Mumbai",
        "destination": "Singapore",
        "cargo_type": "Machinery",
        "weight_kg": 1500.0,
    },
    {
        "origin": "Chennai",
        "destination": "Colombo",
        "cargo_type": "Textiles",
        "weight_kg": 85.0,
    },
    {
        "origin": "Nhava Sheva",
        "destination": "Rotterdam",
        "cargo_type": "Chemicals",
        "weight_kg": 4200.0,
    },
    {
        "origin": "Kolkata",
        "destination": "Dhaka",
        "cargo_type": "Food Grains",
        "weight_kg": 950.0,
    },
    {
        "origin": "Visakhapatnam",
        "destination": "Port Blair",
        "cargo_type": "Medical Supplies",
        "weight_kg": 55.0,
    },
]

# Status progression to make seed data varied and interesting
_STATUS_OVERRIDES: list[ShipmentStatus] = [
    ShipmentStatus.pending,
    ShipmentStatus.in_transit,
    ShipmentStatus.in_transit,
    ShipmentStatus.delivered,
    ShipmentStatus.cancelled,
    ShipmentStatus.pending,
]


def run() -> None:
    """Populate the in-memory store with sample shipments (idempotent guard included)."""
    # Only seed if the store is empty to avoid duplicates on hot-reload
    if shipment_service.list_shipments():
        return

    for data, status in zip(_SEED_DATA, _STATUS_OVERRIDES):
        shipment = shipment_service.create_shipment(ShipmentCreate(**data))
        if status != ShipmentStatus.pending:
            shipment_service.update_status(shipment.id, status)
