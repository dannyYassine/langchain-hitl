"""Tests for root endpoint."""

from fastapi.testclient import TestClient

from main import app


class TestRoot:
    """Tests for root endpoint."""

    def test_root_endpoint(self) -> None:
        """
        Test the / root endpoint returns correct message.

        Verifies that:
        - Status code is 200
        - Response JSON contains welcome message
        """
        client = TestClient(app)
        response = client.get("/")

        assert response.status_code == 200
        assert response.json() == {"message": "LangChain Human-in-the-Loop API"}
