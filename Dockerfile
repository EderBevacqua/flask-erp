FROM python:3.8-slim-buster

ENV INSTALL_PATH /flask-erp

RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 6000

COPY . .

RUN chmod +x /flask-erp/docker-entrypoint.sh

CMD ["/bin/bash", "/flask-erp/docker-entrypoint.sh"]
