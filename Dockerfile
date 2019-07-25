FROM python:2.7-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirement.txt
CMD ["python", "app.py"]