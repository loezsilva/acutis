FROM python:3.13.2-slim AS build
WORKDIR /app
RUN groupadd python && useradd -m -g python python
USER python
ENV TZ="America/Fortaleza"
ENV PATH="/home/python/.local/bin:$PATH"

COPY requirements.txt .
RUN pip install --user --upgrade pip \
    && pip install --user -r requirements.txt

COPY pyproject.toml poetry.lock ./
COPY ./src ./src
RUN pip install --user .

FROM python:3.13.2-slim AS final
WORKDIR /app
ENV TZ="America/Fortaleza"
ENV PATH="/home/python/.local/bin:$PATH"

RUN apt update && apt install curl -y --no-install-recommends \
    && curl -sSL -O https://packages.microsoft.com/config/debian/$(grep VERSION_ID /etc/os-release | cut -d '"' -f 2 | cut -d '.' -f 1)/packages-microsoft-prod.deb \
    && dpkg -i packages-microsoft-prod.deb \
    && rm packages-microsoft-prod.deb \
    && apt update \
    && ACCEPT_EULA=Y apt install -y msodbcsql17 unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd python && useradd -m -g python python
USER python

COPY --from=build /home/python/.local /home/python/.local

EXPOSE ${PORT:-80}
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-80} -k gevent --user=python --group=python acutis_api.api.app:app --log-level=debug --access-logfile=- --error-logfile=-"]