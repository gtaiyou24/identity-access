FROM python:3.12-slim

ENV TZ=Asia/Tokyo

ARG project_dir=/app/
COPY ./app $project_dir
COPY ./app/requirements.txt $project_dir
WORKDIR $project_dir

# ライブラリをインストール
RUN apt-get update -y \
    && apt-get install -y default-libmysqlclient-dev pkg-config build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# uvicornのサーバーを立ち上げる
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0"]
