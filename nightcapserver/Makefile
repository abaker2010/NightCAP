build:
	docker build --force-rm $(options) -t nightcapsite:latest .
build-prod:
	${MAKE} build options="--target production"

clean:
	docker-compose --remove-orphans

compose-start:
	docker-compose up $(options)