newsblur := $(shell docker ps -qf "name=newsblur_web")
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

stage:
	- CURRENT_UID=${CURRENT_UID} CURRENT_GID=${CURRENT_GID} docker-compose up -d --build --remove-orphans

dev:
	- CURRENT_UID=${CURRENT_UID} CURRENT_GID=${CURRENT_GID} docker-compose -f docker-compose.dev.yml up -d --build --remove-orphans

dev-exec:
	# run `make dev` if this doesn't work
	- docker attach ${newsblur}

dev-down:
	- docker-compose -f docker-compose.dev.yml down

test:
	- ./manage.py test --settings=utils.test_settings
