"""Mock data utilities for demo and testing purposes."""

from datetime import datetime, timedelta
from uuid import uuid4

from agent_request import AgentRequest, RequestStatus


def create_mock_data(requests_store: dict[str, AgentRequest]) -> None:
    """
    Create mock agent requests for demonstration.

    Args:
        requests_store: Dictionary to store mock agent requests
    """
    mock_requests = [
        AgentRequest(
            id=str(uuid4()),
            title="Data pipeline migration",
            description="Migrating legacy ETL to new streaming architecture",
            status=RequestStatus.RUNNING,
            progress=65,
            created_at=datetime.now() - timedelta(minutes=3),
            updated_at=datetime.now(),
        ),
        AgentRequest(
            id=str(uuid4()),
            title="Security audit review",
            description="Review security audit findings and propose fixes",
            status=RequestStatus.HITL_REQUIRED,
            progress=50,
            created_at=datetime.now() - timedelta(minutes=5),
            updated_at=datetime.now(),
        ),
        AgentRequest(
            id=str(uuid4()),
            title="API endpoint generation",
            description="Generate REST API endpoints for user management",
            status=RequestStatus.RUNNING,
            progress=30,
            created_at=datetime.now() - timedelta(minutes=8),
            updated_at=datetime.now(),
        ),
        AgentRequest(
            id=str(uuid4()),
            title="Database schema update",
            description="Update database schema for new features",
            status=RequestStatus.COMPLETED,
            progress=100,
            created_at=datetime.now() - timedelta(minutes=15),
            updated_at=datetime.now(),
        ),
    ]

    for req in mock_requests:
        requests_store[req.id] = req
