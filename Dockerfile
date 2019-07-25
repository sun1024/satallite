FROM python:2.7-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirement.txt  -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["python", "app.py"]