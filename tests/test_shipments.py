import pytest
from httpx import AsyncClient

VALID_PAYLOAD = {
    "origin": "Kochi",
    "destination": "Dubai",
    "cargo_type": "Electronics",
    "weight_kg": 150.5,
}


# ── Health check ──────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ── POST /shipments ───────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_create_shipment_success(client: AsyncClient) -> None:
    response = await client.post("/shipments", json=VALID_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["origin"] == "Kochi"
    assert data["destination"] == "Dubai"
    assert data["cargo_type"] == "Electronics"
    assert data["weight_kg"] == 150.5
    assert data["status"] == "pending"
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_create_shipment_invalid_weight_zero(client: AsyncClient) -> None:
    payload = {**VALID_PAYLOAD, "weight_kg": 0}
    response = await client.post("/shipments", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert any("weight_kg" in str(err) or "greater than 0" in str(err) for err in body["detail"])


@pytest.mark.asyncio
async def test_create_shipment_invalid_weight_negative(client: AsyncClient) -> None:
    payload = {**VALID_PAYLOAD, "weight_kg": -5.0}
    response = await client.post("/shipments", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert any("weight_kg" in str(err) or "greater than 0" in str(err) for err in body["detail"])


# ── GET /shipments ────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_list_shipments_empty(client: AsyncClient) -> None:
    response = await client.get("/shipments")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_shipments_returns_created(client: AsyncClient) -> None:
    await client.post("/shipments", json=VALID_PAYLOAD)
    response = await client.get("/shipments")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["origin"] == "Kochi"


@pytest.mark.asyncio
async def test_list_shipments_filter_by_status(client: AsyncClient) -> None:
    await client.post("/shipments", json=VALID_PAYLOAD)
    response = await client.get("/shipments", params={"status": "pending"})
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = await client.get("/shipments", params={"status": "delivered"})
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_shipments_filter_invalid_status(client: AsyncClient) -> None:
    response = await client.get("/shipments", params={"status": "flying"})
    assert response.status_code == 422


# ── GET /shipments/{id} ───────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_get_shipment_success(client: AsyncClient) -> None:
    created = (await client.post("/shipments", json=VALID_PAYLOAD)).json()
    response = await client.get(f"/shipments/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


@pytest.mark.asyncio
async def test_get_shipment_not_found(client: AsyncClient) -> None:
    response = await client.get("/shipments/nonexistent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Shipment not found"


# ── PATCH /shipments/{id}/status ─────────────────────────────────────────────

@pytest.mark.asyncio
async def test_update_status_success(client: AsyncClient) -> None:
    created = (await client.post("/shipments", json=VALID_PAYLOAD)).json()
    response = await client.patch(
        f"/shipments/{created['id']}/status",
        json={"status": "in_transit"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "in_transit"


@pytest.mark.asyncio
async def test_update_status_invalid_value(client: AsyncClient) -> None:
    created = (await client.post("/shipments", json=VALID_PAYLOAD)).json()
    response = await client.patch(
        f"/shipments/{created['id']}/status",
        json={"status": "lost_at_sea"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_status_not_found(client: AsyncClient) -> None:
    response = await client.patch(
        "/shipments/nonexistent-id/status",
        json={"status": "delivered"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Shipment not found"


@pytest.mark.asyncio
async def test_update_status_rejected_when_delivered(client: AsyncClient) -> None:
    created = (await client.post("/shipments", json=VALID_PAYLOAD)).json()
    await client.patch(f"/shipments/{created['id']}/status", json={"status": "delivered"})
    response = await client.patch(
        f"/shipments/{created['id']}/status",
        json={"status": "pending"},
    )
    assert response.status_code == 400
    assert "delivered" in response.json()["detail"]
    assert "terminal" in response.json()["detail"]


@pytest.mark.asyncio
async def test_update_status_rejected_when_cancelled(client: AsyncClient) -> None:
    created = (await client.post("/shipments", json=VALID_PAYLOAD)).json()
    await client.patch(f"/shipments/{created['id']}/status", json={"status": "cancelled"})
    response = await client.patch(
        f"/shipments/{created['id']}/status",
        json={"status": "in_transit"},
    )
    assert response.status_code == 400
    assert "cancelled" in response.json()["detail"]
    assert "terminal" in response.json()["detail"]


# ── DELETE /shipments/{id} ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_delete_shipment_success(client: AsyncClient) -> None:
    created = (await client.post("/shipments", json=VALID_PAYLOAD)).json()
    response = await client.delete(f"/shipments/{created['id']}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_shipment_not_found(client: AsyncClient) -> None:
    response = await client.delete("/shipments/nonexistent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Shipment not found"


@pytest.mark.asyncio
async def test_delete_then_get_returns_404(client: AsyncClient) -> None:
    created = (await client.post("/shipments", json=VALID_PAYLOAD)).json()
    await client.delete(f"/shipments/{created['id']}")
    response = await client.get(f"/shipments/{created['id']}")
    assert response.status_code == 404


# ── GET /shipments/summary ────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_summary_empty_store(client: AsyncClient) -> None:
    response = await client.get("/shipments/summary")
    assert response.status_code == 200
    data = response.json()
    assert data == {"pending": 0, "in_transit": 0, "delivered": 0, "cancelled": 0, "total": 0}


@pytest.mark.asyncio
async def test_summary_counts_by_status(client: AsyncClient) -> None:
    # Create 3 shipments and move them to different statuses
    ids = []
    for _ in range(3):
        r = await client.post("/shipments", json=VALID_PAYLOAD)
        ids.append(r.json()["id"])

    await client.patch(f"/shipments/{ids[1]}/status", json={"status": "in_transit"})
    await client.patch(f"/shipments/{ids[2]}/status", json={"status": "delivered"})

    response = await client.get("/shipments/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["pending"] == 1
    assert data["in_transit"] == 1
    assert data["delivered"] == 1
    assert data["cancelled"] == 0
    assert data["total"] == 3


@pytest.mark.asyncio
async def test_summary_total_matches_sum_of_statuses(client: AsyncClient) -> None:
    for _ in range(4):
        await client.post("/shipments", json=VALID_PAYLOAD)

    response = await client.get("/shipments/summary")
    data = response.json()
    status_sum = data["pending"] + data["in_transit"] + data["delivered"] + data["cancelled"]
    assert status_sum == data["total"] == 4
