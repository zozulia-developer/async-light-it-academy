from fastapi.testclient import TestClient


class TestCreatePost:
    def test_create_post(self, client: TestClient):
        data = {
            "userId": 1,
            "title": "test",
            "body": "random text",
        }

        response = client.post("/posts/", json=data)

        assert response.status_code == 201
        response_data = response.json()
        assert response_data["userId"] == 1
        assert response_data["title"] == "test"
        assert response_data["body"] == "random text"
        assert "id" in response_data

    def test_create_post_fails(self, client: TestClient):
        data = {
            "userId": "user id",
            "title": 1,
            "body": True,
        }

        response = client.post("/users/", json=data)

        assert response.status_code == 422


class TestUpdatePost:
    def test_update_post(self, client: TestClient):
        data = {
            "title": "my title",
            "body": "random body",
        }

        response = client.put("/posts/1", json=data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["title"] == "my title"
        assert response_data["body"] == "random body"
        assert "id" in response_data

    def test_update_post_fails(self, client: TestClient):
        data = {
            "my title": "my title",
            "body": "random body",
        }

        response = client.post("/posts/1", json=data)
        assert response.status_code == 405

        response = client.put("/posts/1", json=data)
        assert response.status_code == 422
