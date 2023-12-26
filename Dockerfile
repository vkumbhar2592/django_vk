FROM python:3.10-slim
#RUN echo "max_parallel_downloads=20" | tee -a /etc/dnf/dnf.conf >/dev/null

# use cloud sql - cloud sql proxy
RUN python3 -c "import sqlite3; print(sqlite3.sqlite_version);"
# ----------- Build step for app ----------- #
#FROM base as app_build

ENV DJANGO_SETTINGS_MODULE=config.settings

#RUN dnf install -y gcc-c++ vim
#RUN dnf -y clean all
RUN pip3 install --upgrade pip setuptools requests

RUN python3 -m venv /venv
WORKDIR /venv/
ADD requirements.txt /venv/requirements.txt
RUN /venv/bin/pip install -U -r /venv/requirements.txt
ADD . /venv/

ENV PATH="/venv/bin:$PATH"
# Node stuff that doesn't work inside a docker container :(
#RUN dnf install -y https://rpm.nodesource.com/pub_20.x/nodistro/repo/nodesource-release-nodistro-1.noarch.rpm -y
#RUN curl -sL https://dl.yarnpkg.com/rpm/yarn.repo | tee /etc/yum.repos.d/yarn.repo
#RUN dnf install -y nodejs yarn  --setopt=nodesource-nodejs.module_hotfixes=1
#RUN cd /venv/src && yarn install
#RUN cd /venv/src && yarn build

#ENTRYPOINT ["sh", "/venv/start.sh"]
#ENTRYPOINT ["tail", "-f", "/dev/null"]

# ----------- Deploy step for app ----------- #
# FROM scratch AS app_deploy

# ENV DJANGO_SETTINGS_MODULE=config.settings

# COPY --from=app_build / .
# WORKDIR /venv/

# ENTRYPOINT ["sh", "/venv/start.sh"]

CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 config.wsgi:application
