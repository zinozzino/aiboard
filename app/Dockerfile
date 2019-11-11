# FROM mxnet/python:nightly_cpu_py3
FROM pytorch/pytorch:latest

WORKDIR /app

RUN set -ex && \
    sed -i s/archive\.ubuntu\.com/mirror.kakao.com/g /etc/apt/sources.list && \
    sed -i s/security\.ubuntu\.com/mirror.kakao.com/g /etc/apt/sources.list && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends netcat-openbsd

RUN set -ex && pip install gunicorn

COPY requirements.txt ./
RUN set -ex && pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 5000
ENTRYPOINT [ "/app/entrypoint.sh" ]
CMD ["gunicorn", "--bind", ":5000", "app.plugin:app"]
