# Project Instructions for GitHub Copilot

## Project Overview

This is a LangChain Human-in-the-Loop (HITL) application built with FastAPI, running in Docker containers. The project uses `uv` for fast Python package management and PostgreSQL for persistence.

## Special Agent instructions

**ALWAYS** use multiple subagents to accelerate development.

## Constraints

- **NEVER** add secrets, API keys, passwords, or any sensitive credentials to `.env.example` files
- `.env.example` should only contain placeholder/default values or example formats (e.g., `OPENAI_API_KEY=your_api_key_here`)
-
- Actual secrets belong in `.env` files, which must be gitignored

## Tech Stack

- **Python**: 3.12+
- **FastAPI**: Web framework with automatic OpenAPI documentation
- **LangChain**: Framework for building LLM applications with human-in-the-loop workflows
- **PostgreSQL**: Database with LangChain integration for memory/persistence
- **Docker**: Containerized development environment
- **uv**: Fast Python package installer and resolver

## Critical Development Rules

### Package Management

**ALWAYS** use `docker exec app uv` for any Python package operations:

```bash
# ✅ Correct - Use docker exec
docker exec app uv add package-name
docker exec app uv sync
docker exec app uv run python script.py

# ❌ Wrong - Never use uv directly
uv add package-name
uv sync
```

### Running Python Commands

All Python commands must be executed inside the Docker container:

```bash
# Run Python scripts
docker exec app uv run python script.py

# Run FastAPI dev server
docker exec app uv run fastapi dev main.py --host 0.0.0.0

# Run tests
docker exec app uv run pytest

# Run linting
docker exec app uv run ruff check .
```

## Project Structure

```
app/
  __init__.py           # Package initialization
  main.py              # FastAPI application entry point
  agents.py            # LangChain agent definitions
  weather_response.py  # Response models
  pyproject.toml       # Project dependencies (uv format)
docker/
  app.Dockerfile       # Application container definition
docker-compose.yml     # Service orchestration (app + db)
Makefile              # Development shortcuts
```

## Coding Conventions

### Python Style

- Use **Python 3.12+** features
- Follow **PEP 8** style guide
- Use **type hints** for all function signatures
- Use **async/await** for FastAPI endpoints
- Prefer **f-strings** for string formatting
- Use **Pydantic models** for data validation
- **One class per file** - Each Python file should contain only one class definition (exceptions: small related enums or nested classes)

### FastAPI Patterns

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Service Name")

class RequestModel(BaseModel):
    field: str

@app.post("/endpoint")
async def endpoint(data: RequestModel):
    """Always include docstrings for endpoints."""
    # Use async for I/O operations
    result = await some_async_operation()
    return {"result": result}
```

### LangChain Patterns

- Use **langchain-postgres** for persistence
- Implement **checkpointing** for human-in-the-loop workflows
- Use **langchain-openai** for OpenAI models
- Follow **LangChain Expression Language (LCEL)** patterns

```python
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Initialize models
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Use LCEL chains
chain = prompt | llm | output_parser
```

### Error Handling

```python
from fastapi import HTTPException, status

@app.get("/endpoint")
async def endpoint():
    try:
        result = await operation()
        return result
    except SpecificError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
```

### Testing Conventions

#### Test Structure

**ALWAYS** use class-based tests to organize related test cases:

```python
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
```

**Key rules:**

- Use **class-based tests** (class name starts with `Test`)
- Group related tests in the same class
- Each test method starts with `test_`
- Include comprehensive docstrings explaining what is tested
- No `__init__` method in test classes

#### FastAPI Testing Patterns

**Use TestClient for synchronous testing:**

```python
from fastapi.testclient import TestClient
from main import app

class TestEndpoints:
    """Test API endpoints."""

    def test_endpoint(self):
        """Test endpoint behavior."""
        client = TestClient(app)
        response = client.get("/endpoint")
        assert response.status_code == 200
```

**For async testing with external dependencies:**

```python
import pytest
from httpx import AsyncClient
from main import app

class TestAsyncEndpoints:
    """Test async API endpoints."""

    @pytest.mark.asyncio
    async def test_async_endpoint(self):
        """Test async endpoint behavior."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get("/endpoint")
            assert response.status_code == 200
```

#### Test Organization

- Tests live in `app/tests/` directory
- One test file per module: `test_<module_name>.py`
- Test files must have `__init__.py` in the tests directory
- Use pytest markers to categorize tests:
  - `@pytest.mark.unit` - Unit tests with mocked dependencies
  - `@pytest.mark.integration` - Tests requiring external services

```python
import pytest

class TestWeatherAPI:
    """Tests for weather API endpoints."""

    @pytest.mark.unit
    def test_weather_response_model(self):
        """Test weather response validation."""
        # Test with mocked data
        pass

    @pytest.mark.integration
    def test_weather_api_call(self):
        """Test actual weather API integration."""
        # Test with real API calls
        pass
```

#### Fixtures and Setup

Use `setup_method` and `teardown_method` for per-test setup:

```python
class TestWithSetup:
    """Tests requiring setup/teardown."""

    def setup_method(self):
        """Set up test fixtures before each test."""
        self.client = TestClient(app)
        self.test_data = {"key": "value"}

    def teardown_method(self):
        """Clean up after each test."""
        # Cleanup code here
        pass

    def test_with_fixture(self):
        """Test using setup fixtures."""
        response = self.client.post("/endpoint", json=self.test_data)
        assert response.status_code == 200
```

Use `setup_class` and `teardown_class` for shared setup:

```python
class TestWithClassSetup:
    """Tests with shared class-level fixtures."""

    @classmethod
    def setup_class(cls):
        """Set up fixtures shared across all tests in class."""
        cls.client = TestClient(app)

    @classmethod
    def teardown_class(cls):
        """Clean up class-level fixtures."""
        pass
```

#### Assertions

Use clear, specific assertions:

```python
# ✅ Good - Specific assertions
assert response.status_code == 200
assert response.json() == {"status": "ok"}
assert "error" not in response.json()

# ✅ Good - Testing structure
data = response.json()
assert "temperature" in data
assert isinstance(data["temperature"], float)

# ❌ Avoid - Vague assertions
assert response  # What are we checking?
assert True  # Meaningless
```

#### Mocking External Dependencies

Mock external API calls and LLM interactions:

```python
from unittest.mock import patch, MagicMock

class TestWithMocks:
    """Tests with mocked dependencies."""

    @patch("tools.requests.get")
    def test_weather_api_mock(self, mock_get):
        """Test weather endpoint with mocked API."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"temperature": 20.0}
        mock_get.return_value = mock_response

        client = TestClient(app)
        response = client.post("/weather", json={"city": "Paris"})

        assert response.status_code == 200
        mock_get.assert_called_once()
```

#### Running Tests

```bash
# Run all tests
make test  # or: docker exec app uv run pytest

# Run specific test file
docker exec app uv run pytest tests/test_health.py

# Run specific test class
docker exec app uv run pytest tests/test_health.py::TestHealth

# Run specific test method
docker exec app uv run pytest tests/test_health.py::TestHealth::test_health_endpoint

# Run tests with specific marker
docker exec app uv run pytest -m unit
docker exec app uv run pytest -m integration

# Run with verbose output
docker exec app uv run pytest -v

# Run with coverage
docker exec app uv run pytest --cov=. --cov-report=html
```

## Environment Variables

Required environment variables (configured in `.env`):

```bash
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=langchain_hitl

# LangChain
OPENAI_API_KEY=...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=...
```

Access in code:

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    postgres_user: str
    openai_api_key: str

    class Config:
        env_file = ".env"

settings = Settings()
```

## Development Workflow

### Adding Dependencies

```bash
# Production dependency
docker exec app uv add package-name

# Development dependency
docker exec app uv add --dev pytest ruff

# Update all dependencies
docker exec app uv lock --upgrade
docker exec app uv sync
```

### Running the Application

```bash
# Start services
make up  # or: docker-compose up -d

# Install dependencies
docker exec app uv sync --frozen

# Run FastAPI server
docker exec app uv run fastapi dev main.py --host 0.0.0.0

# Access at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Testing

```bash
# Run all tests
docker exec app uv run pytest

# Run with coverage
docker exec app uv run pytest --cov=app --cov-report=html

# Run specific test
docker exec app uv run pytest tests/test_file.py::test_function
```

### Code Quality

```bash
# Lint code
docker exec app uv run ruff check .

# Format code
docker exec app uv run ruff format .

# Type checking (if mypy is installed)
docker exec app uv run mypy app/
```

## Patterns

### Dependency Management Workflow

**ALWAYS** run `uv sync` immediately after installing any package:

```bash
# ✅ Correct pattern
docker exec app uv add requests
docker exec app uv sync

# ✅ Adding multiple packages
docker exec app uv add requests httpx pydantic
docker exec app uv sync

# ✅ Adding dev dependencies
docker exec app uv add --dev pytest ruff
docker exec app uv sync
```

**Why this matters:**

- Ensures lock file is updated with new dependencies
- Resolves transitive dependencies correctly
- Prevents runtime import errors
- Keeps development environment consistent

## Database Operations

### Connecting to PostgreSQL

```bash
# Access database shell
docker exec -it db psql -U postgres -d langchain_hitl
```

### Using LangChain with PostgreSQL

```python
from langchain_postgres import PostgresChatMessageHistory

# Initialize with connection string
connection = "postgresql://postgres:postgres@db:5432/langchain_hitl"

history = PostgresChatMessageHistory(
    connection_string=connection,
    session_id="session_123"
)
```

## File Naming Conventions

- Python files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Test files: `test_*.py`

## Import Organization

Order imports as follows:

```python
# 1. Standard library
import os
from typing import Optional

# 2. Third-party packages
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 3. LangChain imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# 4. Local imports
from agents import create_agent
```

## Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Document API endpoints with FastAPI's description parameter

```python
@app.post("/endpoint", description="Detailed endpoint description")
async def endpoint(data: RequestModel):
    """
    Process data and return result.

    Args:
        data: Request data model

    Returns:
        Result dictionary with processed data

    Raises:
        HTTPException: If processing fails
    """
    pass
```

## Common Patterns

### Health Check Endpoint

```python
@app.get("/health")
async def health():
    """Health check endpoint for monitoring."""
    return {"status": "ok"}
```

### Dependency Injection

```python
from fastapi import Depends

def get_db_connection():
    # Return database connection
    pass

@app.get("/data")
async def get_data(db = Depends(get_db_connection)):
    # Use db connection
    pass
```

### Background Tasks

```python
from fastapi import BackgroundTasks

@app.post("/process")
async def process(background_tasks: BackgroundTasks):
    background_tasks.add_task(long_running_task, param1, param2)
    return {"message": "Processing started"}
```

## Docker Commands Reference

```bash
# View logs
docker-compose logs -f app

# Restart service
docker-compose restart app

# Rebuild containers
docker-compose up -d --build

# Stop all services
docker-compose down

# Shell access
docker exec -it app bash
```

## Security Best Practices

- Never commit `.env` files
- Use environment variables for secrets
- Validate all input with Pydantic models
- Use FastAPI's security utilities for authentication
- Keep dependencies updated: `docker exec app uv lock --upgrade`

## Performance Tips

- Use `async def` for I/O-bound operations
- Implement connection pooling for database
- Use LangChain's caching mechanisms
- Monitor memory usage with human-in-the-loop workflows

## Troubleshooting

### Common Issues

**Dependencies not found**: Run `docker exec app uv sync --refresh`

**Port already in use**: Change ports in `docker-compose.yml` or stop conflicting services

**Database connection errors**: Ensure `db` service is healthy with `docker-compose ps`

**Import errors**: Verify package is in `pyproject.toml` and run `docker exec app uv sync`

## When Generating Code

1. **Always** use type hints
2. **Always** validate input with Pydantic models
3. **Always** include proper error handling
4. **Always** use async/await for FastAPI endpoints
5. **Always** add docstrings
6. **Never** use blocking I/O in async functions
7. **Never** hardcode credentials or API keys
8. **Prefer** LangChain Expression Language (LCEL) over legacy chains

## Additional Resources

- FastAPI docs: https://fastapi.tiangolo.com
- LangChain docs: https://python.langchain.com
- uv docs: https://github.com/astral-sh/uv
- Pydantic docs: https://docs.pydantic.dev
