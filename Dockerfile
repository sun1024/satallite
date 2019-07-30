FROM ubuntu:latest

ADD . /code
WORKDIR /code

RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN apt update \
&& apt install -y gcc g++ python python-pip
RUN  apt-get clean

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ["python", "app.py"]