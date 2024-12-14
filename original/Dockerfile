FROM almalinux:8
RUN yum -y install epel-release
RUN yum -y update
RUN yum -y install httpd
RUN yum -y install perl-CGI
RUN yum -y install perl-GD

COPY ./ServerName.conf   /etc/httpd/conf.d/
COPY ./index.html        /var/www/html/
COPY ./deedcallparse.cgi /var/www/cgi-bin/
COPY ./mapper.cgi        /var/www/cgi-bin/

EXPOSE 80

ENTRYPOINT /usr/sbin/httpd -D FOREGROUND
