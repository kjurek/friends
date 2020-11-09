build:
	docker-compose build friends_service friends_service_tests

run:
	docker-compose up friends_service

clean:
	docker-compose down --rmi all

requirements:
	docker-compose run --rm --no-deps friends_service_tests pip-compile
	sudo chown $(USER):$(USER) requirements.txt

test:
	docker-compose run --rm friends_service_tests pytest -s -vv

lint: lint-flake8 lint-bandit

lint-flake8:
	docker-compose run --rm --no-deps friends_service_tests flake8 src
	docker-compose run --rm --no-deps friends_service_tests flake8 --ignore E501 tests

lint-bandit:
	docker-compose run --rm --no-deps friends_service_tests bandit -r ./src