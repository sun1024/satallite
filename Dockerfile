FROM python:2.7-alpine
ADD . /code
WORKDIR /code
RUN apk add --no-cache gcc g++ linux-headers libffi-dev openssl-dev
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]