from fastapi.testclient import TestClient


def test_read_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Task Manager" in response.text


def test_create_task(client: TestClient) -> None:
    payload = {"title": "Belajar CI/CD", "description": "Mempelajari pytest dan ruff"}
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Belajar CI/CD"
    assert data["description"] == "Mempelajari pytest dan ruff"
    assert data["is_completed"] is False
    assert "id" in data


def test_create_task_invalid_title(client: TestClient) -> None:
    # Title kosong (min_length=1)
    payload = {"title": "", "description": "Deskripsi"}
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 422


def test_read_tasks_empty(client: TestClient) -> None:
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_task_by_id(client: TestClient) -> None:
    # Buat task dulu
    payload = {"title": "Task 1", "description": "Deskripsi 1"}
    create_response = client.post("/tasks/", json=payload)
    task_id = create_response.json()["id"]

    # Ambil task berdasarkan ID
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Task 1"


def test_read_task_not_found(client: TestClient) -> None:
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task tidak ditemukan"


def test_update_task(client: TestClient) -> None:
    # Buat task dulu
    payload = {"title": "Task Asli", "description": "Deskripsi Asli"}
    create_response = client.post("/tasks/", json=payload)
    task_id = create_response.json()["id"]

    # Update task
    update_payload = {"title": "Task Diperbarui", "is_completed": True}
    response = client.patch(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Task Diperbarui"
    assert data["description"] == "Deskripsi Asli"  # Tidak berubah
    assert data["is_completed"] is True


def test_update_task_not_found(client: TestClient) -> None:
    update_payload = {"title": "Coba Update"}
    response = client.patch("/tasks/999", json=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task tidak ditemukan"


def test_delete_task(client: TestClient) -> None:
    # Buat task dulu
    payload = {"title": "Task Mau Dihapus", "description": "Deskripsi"}
    create_response = client.post("/tasks/", json=payload)
    task_id = create_response.json()["id"]

    # Hapus task
    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    # Pastikan sudah terhapus
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client: TestClient) -> None:
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task tidak ditemukan"
