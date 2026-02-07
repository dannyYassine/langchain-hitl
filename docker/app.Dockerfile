FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies first (cache-friendly layer)
COPY app/pyproject.toml app/uv.lock ./
# RUN uv sync --frozen --no-install-project

# Copy source code and install the project
COPY app/ .
RUN uv sync --frozen

CMD ["uv", "run", "fastapi", "dev", "--host", "0.0.0.0"]
