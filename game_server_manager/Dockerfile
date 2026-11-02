# Build the editable application source from its repository for the HAOS app.
FROM python:3.12-slim AS builder

ARG SOURCE_REPOSITORY=https://github.com/Gamerz32/Manager-For-Game-Servers-HA.git
ARG SOURCE_REF=main

RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /source
RUN git clone --depth 1 --branch "$SOURCE_REF" "$SOURCE_REPOSITORY" .

RUN python -m pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

ARG APP_VERSION=3.0.4
ARG BUILD_VERSION
ARG BUILD_ARCH

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

LABEL io.hass.version="$BUILD_VERSION" \
      io.hass.type="app" \
      io.hass.arch="$BUILD_ARCH"

WORKDIR /app
COPY --from=builder /install/ /usr/local/
COPY --from=builder /source/manager/ /app/manager/
COPY --from=builder /source/run.sh /run.sh

RUN chmod 0755 /run.sh

EXPOSE 8099
ENTRYPOINT ["/run.sh"]
