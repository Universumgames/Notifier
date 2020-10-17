FROM php:7.4-apache
ADD ./server /var/www/html/
RUN cd /var/www/html/
RUN chmod -R 777 ./
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"