newsblur := $(shell docker ps -qf "name=newsblur_web")
CURRENT_UID := $(shell id -u)
CURRENT_GID := $(shell id -g)

# this command will bring up the stage cluster. This would be used the code within the container rather
# than as a volume
stage:
	- cp docker_local_settings.py docker/local_settings.py
	- CURRENT_UID=${CURRENT_UID} CURRENT_GID=${CURRENT_GID} docker-compose up -d --build --remove-orphans

# this command brings up the dev cluster. This uses the code as a volume instead of moving it into the image.
# debugging is enabled in this cluster for the newsblur_web container
dev:
	- cp docker_local_settings.py docker/local_settings.py
	- CURRENT_UID=${CURRENT_UID} CURRENT_GID=${CURRENT_GID} docker-compose -f docker-compose.dev.yml up -d --build --remove-orphans

# allows user to exec into newsblur_web and use pdb.
dev-exec:
	# run `make dev` if this doesn't work
	- docker attach ${newsblur}

# brings down dev containers
dev-down:
	- docker-compose -f docker-compose.dev.yml down

# runs tests
test:
	- ./manage.py test --settings=utils.test_settings
