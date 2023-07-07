FROM python:3.11

# stops python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# allows for python to be displayed in real time
# because it is not being buffered.
ENV PYTHONUNBUFFERED 1

# Set work directory
RUN mkdir /app
RUN mkdir /app/staticfiles
WORKDIR /app

# called the dash why switch (like letter y)
# the -y means do not stop and ask for a user prompt
RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  && apt-get -y install netcat-traditional gcc postgresql \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
# that was update, then installing all dependencies
# next is libpq-dev dependencies to work with postgres
# gettext has to do with transmission dependencies
# for postgres dependencies netcat-traditional gcc postgresql
# recently netcat had to be changed after netcat had an update. I had to change
# to netcat-tradtional 
# the next line is to clean up files
# remove /var/lib/apt/lists/ is the last file

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# installing chromedriver
# I had to run 'docker system prune' to get rid of old build caches that I didn't
# know were still there. It was too big otherwise. It also got rid of networks.
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pip3 install pipenv && pipenv install --system

# Copy project
COPY . /app/

COPY ./docker/local/django/entrypoint /entrypoint
# processes the line endings of the shell scripts
# converts it to Unix line endings from windows 9
RUN sed -i 's/\r$//g' /entrypoint
# makes entry line shell script executable
RUN chmod +x /entrypoint

# start script
COPY ./docker/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# start celery worker
COPY ./docker/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

# start celery beat
COPY ./docker/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

# start flower
COPY ./docker/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

# note that there is no ending
ENTRYPOINT [ "/entrypoint"]
