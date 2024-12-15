IMAGE_NAME=local/almalinux8-metes-and-bounds
CONTAINER_NAME=metes-and-bounds
PORT=5077
SRCS_HTML=html/index.html
SRCS_CONF=conf/ServerName.conf
SRCS_CGI=cgi-bin/deedcallparse.cgi cgi-bin/mapper.cgi
SRCS=$(SRCS_HTML) $(SRCS_CONF) $(SRCS_CGI)

all:

build:	Dockerfile $(SRCS)
	docker build --rm --tag=$(IMAGE_NAME) .

rebuild: build rm run
	@echo -n

run:
	docker run --detach --restart=unless-stopped --name $(CONTAINER_NAME) --publish $(PORT):80 $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)

rm:	stop
	docker rm $(CONTAINER_NAME)

bash:
	docker exec -it $(CONTAINER_NAME) /bin/bash

firewall:
	sudo firewall-cmd --zone=public --permanent --add-port=$(PORT)/tcp
	sudo firewall-cmd --reload
