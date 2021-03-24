FROM python:3.8

RUN apt update
RUN apt install libffi-dev musl-dev wget libxslt-dev -y

RUN pip install requests
RUN pip install lxml
RUN pip install -U python-dotenv
RUN pip install 'elasticsearch>=7.0.0,<8.0.0'
RUN pip install datefinder
RUN pip install cffi
RUN pip install scrapy



