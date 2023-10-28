# pull official base image
FROM python:3.9.2-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1


# install psycopg2 dependencies
RUN apk update \
    && apk add libffi-dev  postgresql-dev wkhtmltopdf gcc python3-dev musl-dev py-pip jpeg-dev zlib-dev \
    && apk add libressl-dev perl rust libmagic pango openjpeg-dev g++ freetype-dev
RUN apk --no-cache add \
    icu-dev \
    gettext \
    gettext-dev

RUN apk update \
    && apk add --no-cache git \
       cmake \
       libstdc++ libgcc g++ \
       make \
       jpeg jpeg-dev \
       libpng libpng-dev \
       giflib giflib-dev \
       openblas \
       openblas-dev \
       ca-certificates curl wget \
    && rm -rf /var/cache/apk/*

ARG BRANCH=v19.13

RUN wget -c -q https://github.com/davisking/dlib/archive/${BRANCH}.tar.gz \
 && tar xf ${BRANCH}.tar.gz \
 && mv dlib-* dlib \
 && mkdir -p dlib/build \
 && (cd dlib/build \
    && cmake -DCMAKE_BUILD_TYPE=Release -DDLIB_PNG_SUPPORT=ON -DDLIB_GIF_SUPPORT=ON -DDLIB_JPEG_SUPPORT=ON .. \
    && cmake --build . --config Release -- -j2 \
    && make install) \
 && rm -rf *.tar.gz /dlib/build

WORKDIR /requirements

# copy project
COPY requirements/production.txt production.txt
COPY requirements/requirements.txt base.txt

COPY requirements/ .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r production.txt
RUN pip install -r base.txt
# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media
RUN mkdir $APP_HOME/locale
RUN chown -R app:app $APP_HOME
RUN chown -R app:app $APP_HOME/static
RUN chown -R app:app $APP_HOME/media
RUN chown -R app:app $APP_HOME/locale
WORKDIR $APP_HOME

# copy entrypoint.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# VOLUME
# VOLUME /home/app/web/mediafiles


# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh

##
RUN ["chmod", "+x", "/home/app/web/entrypoint.sh"]
ENTRYPOINT ["/home/app/web/entrypoint.sh"]