"""API routes for LangChain HITL application."""

from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from agent_factory import create_weather_agent
from agent_request import AgentRequest, RequestStatus
from weather_query import WeatherQuery
from weather_response import WeatherResponse

# Configure Jinja2 templates
templates = Jinja2Templates(directory="templates")

# In-memory storage for demo (will be replaced with database)
requests_store: dict[str, AgentRequest] = {}

# Create API router
router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint for monitoring."""
    return {"status": "ok"}


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "LangChain Human-in-the-Loop API"}


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request) -> HTMLResponse:
    """
    Render the main dashboard page.

    Args:
        request: FastAPI request object

    Returns:
        HTML response with dashboard template
    """
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "title": "Agent Dashboard"}
    )


@router.post("/api/agent/request", response_class=HTMLResponse)
async def create_agent_request(request: Request) -> HTMLResponse:
    """
    Create a new agent request and return HTML fragment.

    Args:
        request: FastAPI request object with form data

    Returns:
        HTML fragment of the new request card
    """
    form_data = await request.form()
    description = str(form_data.get("description", ""))

    # Create new request
    request_id = str(uuid4())
    new_request = AgentRequest(
        id=request_id,
        title=description[:50] + "..." if len(description) > 50 else description,
        description=description,
        status=RequestStatus.RUNNING,
        progress=15,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    requests_store[request_id] = new_request

    # Return HTML fragment
    return templates.TemplateResponse(
        "components/request_card.html",
        {"request": request, "req": new_request},
    )


@router.get("/api/requests/active", response_class=HTMLResponse)
async def get_active_requests(request: Request) -> HTMLResponse:
    """
    Get all active requests as HTML fragments.

    Args:
        request: FastAPI request object

    Returns:
        HTML fragments of all active request cards
    """
    # Sort by creation time (newest first)
    active_requests = sorted(
        requests_store.values(), key=lambda r: r.created_at, reverse=True
    )

    return templates.TemplateResponse(
        "components/active_requests.html",
        {"request": request, "requests": active_requests},
    )


@router.get("/api/requests/{request_id}", response_class=HTMLResponse)
async def get_request(request_id: str, request: Request) -> HTMLResponse:
    """
    Get a specific request as HTML fragment.

    Args:
        request_id: Request identifier
        request: FastAPI request object

    Returns:
        HTML fragment of the request card

    Raises:
        HTTPException: If request not found
    """
    agent_request = requests_store.get(request_id)
    if not agent_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Request not found"
        )

    return templates.TemplateResponse(
        "components/request_card.html",
        {"request": request, "req": agent_request},
    )


@router.post("/api/requests/{request_id}/approve", response_class=HTMLResponse)
async def approve_request(request_id: str, request: Request) -> HTMLResponse:
    """
    Approve a request requiring human-in-the-loop.

    Args:
        request_id: Request identifier
        request: FastAPI request object

    Returns:
        Updated HTML fragment of the request card

    Raises:
        HTTPException: If request not found
    """
    agent_request = requests_store.get(request_id)
    if not agent_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Request not found"
        )

    # Update request status
    agent_request.status = RequestStatus.APPROVED
    agent_request.progress = 75
    agent_request.updated_at = datetime.now()

    return templates.TemplateResponse(
        "components/request_card.html",
        {"request": request, "req": agent_request},
    )


@router.post("/api/requests/{request_id}/deny", response_class=HTMLResponse)
async def deny_request(request_id: str, request: Request) -> HTMLResponse:
    """
    Deny a request requiring human-in-the-loop.

    Args:
        request_id: Request identifier
        request: FastAPI request object

    Returns:
        Updated HTML fragment of the request card

    Raises:
        HTTPException: If request not found
    """
    agent_request = requests_store.get(request_id)
    if not agent_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Request not found"
        )

    # Update request status
    agent_request.status = RequestStatus.DENIED
    agent_request.progress = 0
    agent_request.updated_at = datetime.now()

    return templates.TemplateResponse(
        "components/request_card.html",
        {"request": request, "req": agent_request},
    )


@router.post(
    "/weather",
    response_model=WeatherResponse,
    description="Get weather information using AI agent",
)
async def get_weather_info(query: WeatherQuery) -> WeatherResponse:
    """
    Process weather query using LangChain agent.

    Args:
        query: User's weather question

    Returns:
        WeatherResponse with structured weather data

    Raises:
        HTTPException: If agent processing fails
    """
    try:
        agent = create_weather_agent()
        response = agent.invoke(
            {"messages": [{"role": "user", "content": query.query}]}
        )
        weatherResponse: WeatherResponse = response["structured_response"]

        return weatherResponse
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent processing failed: {str(e)}",
        )


def get_requests_store() -> dict[str, AgentRequest]:
    """
    Get the requests store for initialization.

    Returns:
        Dictionary of agent requests
    """
    return requests_store
