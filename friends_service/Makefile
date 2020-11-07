requirements:
	docker-compose run --rm friends_service_tools pip-compile
	sudo chown $(USER):$(USER) requirements.txt

test:
	docker-compose run --rm friends_service_tools pytest

lint-flake8:
	docker-compose run --rm friends_service_tools flake8 .

lint-bandit:
	docker-compose run --rm friends_service_tools bandit -r ./src

lint: lint-flake8 lint-bandit