# OCR 服务

使用`PaddleOCR`搭建简单的PDF OCR识别服务, 可按实际需求进行修改完善.

## 1. 制作镜像

首先按照[docker-cuda-ocr-runtime](https://gitee.com/kernelstudio/docker-cuda-ocr-runtime)文档制作`cuda-ocr`运行环境.

```shell
sh build.sh
```

## 2. 启动服务

```shell
docker-compose up -d 

# 查看日志
docker logs -f ocr-service
```

命令行方式启动

```shell
docker run -ti --name ocr-service --restart always -d ocr-service
```

## 3. 停止删除容器

```shell
docker stop ocr-service && docker rm ocr-service
```

## 4. 测试上传识别

```python
import io

import requests

url = 'http://ocr-service/api/v1/open/service/ocr'

# 直接发送字节数据（例如图片二进制流）
with open('/Users/u/Downloads/36.pdf', 'rb') as f:
    raw_bytes = f.read()

doc_file = io.BytesIO(raw_bytes)
files = {'file': (
    'ocr.pdf',  # 文件名
    doc_file,  # 文件流
    'application/pdf',  # 请求头Content-Type字段对应的值
    {'Expires': '0'})
}
response = requests.post(url, files=files)
print(response.json().get('text'))

```