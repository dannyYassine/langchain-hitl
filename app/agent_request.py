"""Agent request model for tracking agent execution status."""

from datetime import datetime

from pydantic import BaseModel, Field

from request_status import RequestStatus


class AgentRequest(BaseModel):
    """
    Model representing an agent request with status tracking.

    Tracks the lifecycle of an agent request from creation through completion,
    including human-in-the-loop approval stages.

    Attributes:
        id: Unique identifier for the request
        title: Brief title of the request
        description: User's query or input
        status: Current status of the request
        progress: Progress percentage from 0 to 100
        created_at: Timestamp when request was created
        updated_at: Timestamp when request was last updated
    """

    id: str = Field(..., description="Unique identifier for the request")
    title: str = Field(..., description="Brief title of the request")
    description: str = Field(..., description="User's query or input")
    status: RequestStatus = Field(
        default=RequestStatus.PENDING, description="Current status of the request"
    )
    progress: int = Field(
        default=0, ge=0, le=100, description="Progress percentage (0-100)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when request was created",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when request was last updated",
    )

    class Config:
        """Pydantic model configuration."""

        json_schema_extra = {
            "example": {
                "id": "req_123",
                "title": "Weather Query",
                "description": "What's the weather in Paris?",
                "status": "pending",
                "progress": 0,
                "created_at": "2026-02-08T10:00:00Z",
                "updated_at": "2026-02-08T10:00:00Z",
            }
        }
