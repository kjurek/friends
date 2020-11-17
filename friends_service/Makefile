.PHONY: build run clean alembic-migrate alembic-revision test lint lint-flake8 lint-bandit

build:
	docker-compose build

run:
	docker-compose up friends_service

clean:
	docker-compose down --rmi all

alembic-migrate:
	docker-compose run --rm friends_service_tests sh -c '/usr/local/bin/wait && alembic upgrade head'

alembic-revision: alembic-migrate
	docker-compose run --rm friends_service_tests sh -c '/usr/local/bin/wait && alembic revision --autogenerate'
	sudo chown -R $(USER):$(USER) alembic

requirements.txt: requirements.in
	docker-compose run --rm --no-deps friends_service_tests pip-compile
	sudo chown $(USER):$(USER) requirements.txt

test:
	docker-compose run --rm friends_service_tests

lint: lint-flake8 lint-bandit

lint-flake8:
	docker-compose run --rm --no-deps friends_service_tests flake8 src
	docker-compose run --rm --no-deps friends_service_tests flake8 --ignore E501 tests

lint-bandit:
	docker-compose run --rm --no-deps friends_service_tests bandit -r ./src
