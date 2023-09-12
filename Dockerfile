# 使う基本イメージを選択
FROM python:3.9

# 作業フォルダ
WORKDIR /code

# Localから作業フォルダに必要なファイルをCopy
COPY ./requirements.txt /code/requirements.txt

# requirements.txtに定義されたモジュールのインストール
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# ソースCopy
COPY ./app /code/app

# 実行
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]