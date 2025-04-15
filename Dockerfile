FROM cuda-ocr-runtime:12.4.1

WORKDIR /app

COPY requirements.txt .
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]