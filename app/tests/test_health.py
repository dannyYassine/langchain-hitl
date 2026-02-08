"""Tests for health check endpoint."""

from fastapi.testclient import TestClient

from main import app


class TestHealth:
    """Tests for health endpoint."""

    def test_health_endpoint(self):
        """
        Test the /health endpoint returns correct status.

        Verifies that:
        - Status code is 200
        - Response JSON contains correct status
        """
        client = TestClient(app)
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
