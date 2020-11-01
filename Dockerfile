FROM python:3.9.0-alpine3.12

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install -U --pre -f https://wxpython.org/Phoenix/snapshot-builds/ wxpython

COPY src/ .

CMD [ "python", "Pyut.py" ]
