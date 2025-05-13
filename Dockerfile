FROM cuda-ocr-runtime:12.4.1

WORKDIR /app

COPY requirements.txt .
RUN cd /app && bash .venv/bin/activate && \
    mkdir -p /app/static/ && pip3 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

COPY app.py .

CMD ["python3", "app.py"]