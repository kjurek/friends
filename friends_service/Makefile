build:
	docker-compose build friends_service friends_service_tools friends_service_tests

run:
	docker-compose up friends_service

clean:
	docker-compose down --rmi all

requirements:
	docker-compose run --rm friends_service_tools pip-compile
	sudo chown $(USER):$(USER) requirements.txt

test:
	docker-compose run --rm friends_service_tests pytest

lint: lint-flake8 lint-bandit

lint-flake8:
	docker-compose run --rm friends_service_tools flake8 .

lint-bandit:
	docker-compose run --rm friends_service_tools bandit -r ./src