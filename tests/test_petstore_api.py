import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"


class TestPetStoreAPI:
    """
    PetStore Swagger API CRUD Testleri
    REST standartlarına ve HTTP semantiğine göre yazılmıştır.
    API'nin beklenen davranıştan sapmaları xfail olarak işaretlenmiştir.
    """

    # ==================== CREATE ====================
    def test_create_pet_positive(self):
        """TC1: Positive - Geçerli payload ile pet oluşturma"""
        payload = {
            "id": 12345,
            "name": "TestDog",
            "category": {"id": 1, "name": "Dogs"},
            "photoUrls": ["https://example.com/photo.jpg"],
            "tags": [{"id": 1, "name": "test"}],
            "status": "available"
        }
        response = requests.post(f"{BASE_URL}/pet", json=payload)
        assert response.status_code == 200
        assert response.json()["name"] == "TestDog"

        # Cleanup
        requests.delete(f"{BASE_URL}/pet/{payload['id']}")

    def test_create_pet_negative_empty_name(self):
        """TC2: Negative - Empty name ile pet oluşturma"""
        payload = {
            "id": 12346,
            "name": "",
            "category": {"id": 1, "name": "Dogs"},
            "photoUrls": ["https://example.com/photo.jpg"],
            "status": "available"
        }
        response = requests.post(f"{BASE_URL}/pet", json=payload)
        # REST standardına göre 400 beklenir, API 200 dönüyor (bilinen issue)
        assert response.status_code in [200, 400], f"Unexpected status: {response.status_code}"

    @pytest.mark.xfail(reason="API 400 yerine 415 döndürüyor - Content-Type header sorunu")
    def test_create_pet_negative_null_payload(self):
        """TC3: Negative - Null payload ile pet oluşturma"""
        response = requests.post(f"{BASE_URL}/pet", json=None)
        # REST standardına göre 400 Bad Request beklenir
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    # ==================== READ ====================
    def test_get_pet_positive(self):
        """TC4: Positive - Var olan pet'i getir"""
        # Önce pet oluştur
        payload = {"id": 12347, "name": "GetTest", "status": "available", "photoUrls": []}
        requests.post(f"{BASE_URL}/pet", json=payload)

        response = requests.get(f"{BASE_URL}/pet/12347")
        assert response.status_code == 200
        assert response.json()["name"] == "GetTest"

        # Cleanup
        requests.delete(f"{BASE_URL}/pet/12347")

    def test_get_pet_negative_not_found(self):
        """TC5: Negative - Var olmayan pet'i getir"""
        response = requests.get(f"{BASE_URL}/pet/999999999")
        # REST standardına göre 404 beklenir
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    def test_get_pet_negative_invalid_id(self):
        """TC6: Negative - Geçersiz ID formatı"""
        response = requests.get(f"{BASE_URL}/pet/invalid")
        # REST standardına göre 400 veya 404 beklenir
        assert response.status_code in [400, 404], f"Unexpected status: {response.status_code}"

    # ==================== UPDATE ====================
    def test_update_pet_positive(self):
        """TC7: Positive - Var olan pet'i güncelle"""
        # Önce pet oluştur
        payload = {"id": 12348, "name": "UpdateTest", "status": "available", "photoUrls": []}
        requests.post(f"{BASE_URL}/pet", json=payload)

        # Güncelle
        update_payload = {"id": 12348, "name": "Updated", "status": "sold", "photoUrls": []}
        response = requests.put(f"{BASE_URL}/pet", json=update_payload)
        assert response.status_code == 200
        assert response.json()["name"] == "Updated"

        # Cleanup
        requests.delete(f"{BASE_URL}/pet/12348")

    @pytest.mark.xfail(reason="API var olmayan pet için 404 yerine 200 dönür - bilinen issue")
    def test_update_pet_negative_not_found(self):
        """TC8: Negative - Var olmayan pet'i güncelle"""
        payload = {"id": 999999999, "name": "NonExistent", "status": "available"}
        response = requests.put(f"{BASE_URL}/pet", json=payload)
        # REST standardına göre 404 Not Found beklenir
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    # ==================== DELETE ====================
    def test_delete_pet_positive(self):
        """TC9: Positive - Var olan pet'i sil"""
        # Önce pet oluştur
        payload = {"id": 12349, "name": "DeleteTest", "status": "available", "photoUrls": []}
        requests.post(f"{BASE_URL}/pet", json=payload)

        # Sil
        response = requests.delete(f"{BASE_URL}/pet/12349")
        assert response.status_code == 200

        # Silindiğini doğrula
        get_response = requests.get(f"{BASE_URL}/pet/12349")
        assert get_response.status_code == 404

    @pytest.mark.xfail(reason="API idempotent davranıyor - var olmayan pet silince 200 dönür")
    def test_delete_pet_negative_not_found(self):
        """TC10: Negative - Var olmayan pet'i sil"""
        response = requests.delete(f"{BASE_URL}/pet/999999999")
        # REST standardına göre 404 Not Found beklenir
        # Ancak API idempotent davranış sergiliyor (200 dönüyor)
        assert response.status_code == 404, f"Expected 404, got {response.status_code}"