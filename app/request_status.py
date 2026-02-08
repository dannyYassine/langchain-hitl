"""Request status enumeration for tracking agent execution lifecycle."""

from enum import Enum


class RequestStatus(str, Enum):
    """Status of an agent request throughout its lifecycle."""

    PENDING = "pending"
    RUNNING = "running"
    HITL_REQUIRED = "hitl_required"
    APPROVED = "approved"
    DENIED = "denied"
    COMPLETED = "completed"
    FAILED = "failed"
