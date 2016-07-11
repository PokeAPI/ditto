FROM python:3.5

RUN mkdir /ditto
WORKDIR /ditto/
ADD requirements.txt /ditto/
RUN pip3 install -r requirements.txt

ADD . /ditto/
RUN python3 setup.py install

CMD ditto serve
EXPOSE 80
