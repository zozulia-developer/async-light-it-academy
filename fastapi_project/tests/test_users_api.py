from fastapi.testclient import TestClient


class TestCreateUser:
    def test_create_user(self, client: TestClient):
        data = {
            "name": "Kirill",
            "username": "test",
            "email": "email@example.com",
            "phone": "1-111-111-1111"
        }

        response = client.post("/users/", json=data)

        assert response.status_code == 201
        response_data = response.json()
        assert response_data["name"] == "Kirill"
        assert response_data["username"] == "test"
        assert response_data["email"] == "email@example.com"
        assert response_data["phone"] == "1-111-111-1111"
        assert "id" in response_data

    def test_create_user_fails(self, client: TestClient):
        data = {
            "name": "111",
            "username": "test",
            "email": "not_a_valid_email",
            "phone": "aaa-222-tyu-5555"
        }

        response = client.post("/users/", json=data)

        assert response.status_code == 422
