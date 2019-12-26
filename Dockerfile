FROM python:3.5.6-alpine3.8

ENV RELEASE_URL=https://github.com/qiniu/python-sdk/archive
ENV MASTER=https://github.com/qiniu/python-sdk/archive/master.zip


COPY LICENSE README.md upload.py  /


# pip install qiniu   failed
RUN wget -qO-  -O qiniu.zip  "${MASTER}"  && \
    unzip qiniu.zip  && \
    rm -f qiniu.zip && \
    cd python-sdk-master && \
    python setup.py install && \
    cd .. && \
    rm -rf python-sdk-master

ENTRYPOINT ["/upload.py"]
