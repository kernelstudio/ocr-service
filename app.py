import logging

import fitz  # PyMuPDF
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
from paddleocr import PaddleOCR

app = Flask(__name__)
app.logger.setLevel(logging.INFO)


def pdf_to_images(pdf_bytes):
    """将 PDF 字节流转换为图像列表"""
    images = []
    try:
        # 使用 PyMuPDF 打开 PDF 字节流
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            # 设置缩放因子为 2 (提高分辨率)
            mat = fitz.Matrix(2.0, 2.0)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            # 转换为 PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
        doc.close()
    except Exception as e:
        app.logger.error(f"PDF 转换失败: {str(e)}")
        raise
    return images


@app.route('/api/v1/open/service/ocr', methods=['POST'])
def ocr_pdf():

    """处理 PDF 文件上传并返回 OCR 结果"""
    if 'file' not in request.files:
        return jsonify({"error": "未上传文件"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "空文件名"}), 400

    try:
        # 初始化 PaddleOCR 引擎（中英文双语）
        ocr_engine = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=True)

        # 读取 PDF 文件为字节流
        pdf_bytes = file.read()
        # 转换为图像列表
        images = pdf_to_images(pdf_bytes)
        full_text = []

        # 对每张图像进行 OCR
        for img in images:
            # 将 PIL Image 转换为 numpy array
            img_np = np.array(img)
            # 执行 OCR
            result = ocr_engine.ocr(img_np, cls=True)
            # 提取文本并合并
            page_text = " ".join([line[-1][0] for line in result[0]])
            full_text.append(page_text)

        # 合并所有页文本
        final_text = "\n\n\n\n".join(full_text)
        return jsonify({"text": final_text})

    except Exception as e:
        app.logger.error(f"OCR 处理失败: {str(e)}")
        return jsonify({"error": "处理失败"}), 500


if __name__ == "__main__":
    server = WSGIServer(("0.0.0.0", 5555), app)
    server.serve_forever()
