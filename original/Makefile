IMAGE_NAME=local/almalinux8-metes-and-bounds
CONTAINER_NAME=metes-and-bounds
PORT=5077

all:

build:	Dockerfile index.html ServerName.conf
	docker build --rm --tag=$(IMAGE_NAME) .

rebuild: build rm run
	@echo -n

run:
	docker run --detach --restart=unless-stopped --name $(CONTAINER_NAME) --publish $(PORT):80 -v /etc/power-outlet.ini:/etc/power-outlet.ini $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)

rm:	stop
	docker rm $(CONTAINER_NAME)

bash:
	docker exec -it $(CONTAINER_NAME) /bin/bash

firewall:
	sudo firewall-cmd --zone=public --permanent --add-port=$(PORT)/tcp
	sudo firewall-cmd --reload
