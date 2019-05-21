FROM python:3.7

LABEL Description='Service'

ENV PYTHONUNBUFFERED=true
ENV PIP_NO_CACHE_DIR=false
ENV PIP_CACHE_DIR='/var/dist'
ENV PIP_INDEX_URL=${index_url}

WORKDIR '/opt/app'

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY './docker/app/gunicorn.py' '/gunicorn.py'

COPY './service' './service'

ARG gunicorn_options
ENV gunicorn_options ${gunicorn_options}

CMD [ "sh", "-c", "gunicorn 'service.app:create_app()' --config='/gunicorn.py' ${gunicorn_options}"]

#COPY './docker/app/entrypoint.sh' '/entrypoint.sh'
#ENTRYPOINT ["/entrypoint.sh"]