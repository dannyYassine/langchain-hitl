DC := docker-compose

.PHONY: help install-uv up logs ps shell

help:
	@echo "Usage:"
	@echo "  make install-uv   Install uvicorn in the app service"
	@echo "  make up           Build and start services (detached)"
	@echo "  make logs         Follow docker compose logs"
	@echo "  make shell        Open a shell in the app service"

app-install:
	$(DC) exec app uv sync --frozen

up:
	$(DC) up -d
down: 
	$(DC) stop

logs:
	$(DC) logs -f

ps:
	$(DC) ps

shell:
	$(DC) run --rm app bash

app:
	$(DC) exec app $(ARGS)
