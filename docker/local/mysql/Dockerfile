FROM mysql:8.0

# Set the working directory
WORKDIR /usr/src/app

# Expose the MySQL port
EXPOSE 3306


COPY ./docker/local/mysql/maintenance /usr/local/bin/maintenance

RUN chmod +x /usr/local/bin/maintenance/*

RUN mv /usr/local/bin/maintenance/* /usr/local/bin \
  && rmdir /usr/local/bin/maintenance