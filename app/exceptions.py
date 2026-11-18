class ShipmentTerminalStateError(Exception):
    """Raised when an update is attempted on a shipment in a terminal state."""

    def __init__(self, current_status: str) -> None:
        self.current_status = current_status
        super().__init__(
            f"Shipment status cannot be updated: '{current_status}' is a terminal state. "
            "Only shipments with status 'pending' or 'in_transit' can be updated."
        )
