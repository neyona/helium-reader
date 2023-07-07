ifneq (,$(wildcard ./.env))
include .env
export
ENV_FILE_PARAM = --env-file .env

endif

up:
	docker-compose up -d

up-prod:
	docker-compose -f docker-compose.production.yml up -d

up-dev:
	docker-compose -f docker-compose.yml up -d

up-stage:
	docker-compose -f docker-compose.staging.yml up -d

build:
	docker-compose up -d --build --remove-orphans

build-prod:
	docker-compose -f docker-compose.production.yml up -d --build --remove-orphans

build-dev:
	docker-compose -f docker-compose.yml up -d --build --remove-orphans

build-stage:
	docker-compose -f docker-compose.staging.yml up -d --build --remove-orphans

migrate:
	docker-compose exec web python3.11 manage.py migrate

migrate-prod:
	docker-compose -f docker-compose.production.yml exec web python3.11 manage.py migrate --noinput

migrate-dev:
	docker-compose -f docker-compose.yml exec web python3.11 manage.py migrate --noinput

migrate-stage:
	docker-compose -f docker-compose.staging.yml exec web python3.11 manage.py migrate --noinput

down:
	docker-compose down

down-prod:
	docker-compose -f docker-compose.production.yml down -v

down-stage:
	docker-compose -f docker-compose.staging.yml down -v

down-dev:
	docker-compose -f docker-compose.yml down -v

down-v:
	docker-compose down -v

show-logs:
	docker-compose logs

makemigrations:
	docker-compose exec web python3.11 manage.py makemigrations

superuser:
	docker-compose exec web python3.11 manage.py createsuperuser

collect:
	docker-compose exec web python3.11 manage.py collectstatic

collect-prod:
	docker-compose -f docker-compose.production.yml exec web python3.11 manage.py collectstatic --no-input --clear

collect-dev:
	docker-compose -f docker-compose.yml exec web python3.11 manage.py collectstatic --no-input --clear

collect-stage:
	docker-compose -f docker-compose.staging.yml exec web python3.11 manage.py collectstatic --no-input --clear

volume:
	docker-volume inspect include_pandas_postgres_data

auth-db:
	docker-compose exec postgres-ipdb psql --username=admin --dbname=postgres
	# use \list to list the databases
	# use \connect to connect to the database as an admin
	# \dt lists the names of the database tables
	# \q is quit

freeze:
	docker-compose exec web pip3 freeze > requirements.txt
