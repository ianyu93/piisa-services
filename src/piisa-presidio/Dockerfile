# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME

# Install postgres
RUN apt-get update && apt-get install -y libpq-dev gcc

# Install production dependencies.
COPY ./ /app

RUN pip install --upgrade pip && pip install --no-cache-dir -r piisa-presidio.requirements.txt

RUN python -m spacy download en_core_web_lg && python -m spacy download es_core_news_md && python -m spacy download it_core_news_md
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]