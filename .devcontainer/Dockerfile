
FROM mcr.microsoft.com/devcontainers/python:3.11

ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

COPY requirements.txt /tmp/pip-tmp/
COPY requirements_dev.txt /tmp/pip-tmp/
RUN pip3 install -U -r /tmp/pip-tmp/requirements.txt
RUN pip3 install -U -r /tmp/pip-tmp/requirements_dev.txt \
    && rm -rf /tmp/pip-tmp

#RUN jupyter nbextension enable --py widgetsnbextension