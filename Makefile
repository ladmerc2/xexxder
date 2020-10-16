run_dev:
	touch ./sennder/.env
	cp .env.example sennder/.env
	@echo "Running in development mode"
	docker-compose up

run_prod:
	touch ./sennder/.env
	cp .env.example sennder/.env
	@echo "Running in production mode"
	docker-compose up

lint:
	touch ./sennder/.env
	cp .env.example sennder/.env
	flake8 sennder/movies

type:
	touch ./sennder/.env
	cp .env.example sennder/.env
	mypy sennder/movies

test:
	touch ./sennder/.env
	cp .env.example sennder/.env
	coverage run --source='./sennder/movies' ./manage.py test
	coverage report