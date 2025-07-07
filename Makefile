.PHONY: run lint typecheck format test docker-build docker-run docker-shell

## Local commands

run:
	python -m bot.main

lint:
	ruff check .

typecheck:
	mypy bot/ tests/

format:
	ruff format .

test:
	pytest


## Docker commands

docker-build:
	docker build -t ai-telegram-bot .

docker-run:
	docker run --rm --env-file .env ai-telegram-bot

docker-shell:
	docker run --rm -it --entrypoint /bin/bash --env-file .env ai-telegram-bot
