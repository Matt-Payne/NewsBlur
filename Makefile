newsblur = $(shell docker ps -qf "name=newsblur_container")

stage:
	- docker-compose up -d --build

dev:
	# need shell logic to see if the full rebuild is necessary
	#- docker-compose -f docker-compose.dev.yml up -d --build
	- docker-compose -f docker-compose.dev.yml up -d --build newsblur_container

dev-exec:
	- docker-compose -f docker-compose.dev.yml exec newsblur_container bash

dev-down:
	- docker-compose -f docker-compose.dev.yml down

test:
	- ./manage.py test --settings=utils.test_settings
