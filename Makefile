run_dev:
	@echo "Running in development mode"
	docker-compose up --build

run_prod:
	@echo "Running in production mode"
	docker-compose up

lint:
	flake8 display_movies --exclude=display_movies/tests/*,sennder/*

test:
	coverage run --source='./display_movies' ./manage.py test display_movies/tests
	coverage report