.PHONY: test lint compile docker-up docker-down

test:
	cd apps/api && pytest -q

compile:
	cd apps/api && python -m compileall app

lint:
	cd apps/api && python -m compileall app

docker-up:
	docker compose up --build

docker-down:
	docker compose down
