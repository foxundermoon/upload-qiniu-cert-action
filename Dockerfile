FROM python:3.12-rc-alpine3.18

ENV RELEASE_URL=https://github.com/qiniu/python-sdk/archive
ENV MASTER=https://github.com/foxundermoon/qiniu-python-sdk/archive/feature/https-config.zip
# ENV DIRNAME=python-sdk-master
ENV DIRNAME=qiniu-python-sdk-feature-https-config

COPY LICENSE README.md upload.py  /


# pip install qiniu   failed
RUN wget -qO-  -O qiniu.zip  "${MASTER}"  && \
    unzip qiniu.zip  && \
    rm -f qiniu.zip && \
    cd ${DIRNAME} && \
    python setup.py install && \
    cd .. && \
    rm -rf ${DIRNAME}

ENTRYPOINT ["/upload.py"]
