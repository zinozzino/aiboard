# FROM mxnet/python:nightly_cpu_py3
FROM pytorch/pytorch:latest

WORKDIR /app

RUN set -ex && pip install gunicorn

COPY requirements.txt ./
RUN set -ex && pip install --no-cache-dir -r requirements.txt

COPY . ./

EXPOSE 5000
CMD ["gunicorn", "--bind", ":5000", "app.plugin:app"]
