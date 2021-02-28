FROM python:3.8-slim-buster 

RUN pip install --upgrade pip

RUN groupadd --gid 1000 python \
  && useradd --uid 1000 --gid python --shell /bin/bash --create-home python

# Create the work dir and set permissions as WORKDIR set the permissions as root
RUN mkdir /home/python/app/ && chown -R python:python /home/python/app
WORKDIR /home/python/app

USER python

ENV PATH="/home/worker/.local/bin:${PATH}"

COPY --chown=python:python . .
RUN pip install -r requirements.txt --no-warn-script-location

CMD ["python", "-u", "main.py"]