#! /usr/bin/env python

import qiniu
from qiniu import DomainManager
import os
import time
import base64


def log(line):
    debug = os.getenv('INPUT_DEBUG')
    if debug:
        print(line)


def readFile(path):
    work = os.getenv('GITHUB_WORKSPACE')
    fullPath = os.path.join(work, path)
    return open(fullPath, 'r').read()


def getCert():
    content = os.getenv('INPUT_CERT')
    if content:
        return content
    path = os.getenv('INPUT_CERT-PATH')
    if path:
        return readFile(path)

    raise Exception(
        'can not get cert, you must set "cert" or "cert-path" input')


def getKey():
    content = os.getenv('INPUT_KEY')
    if content:
        return content
    path = os.getenv('INPUT_KEY-PATH')
    if path:
        return readFile(path)

    raise Exception('can not get key, you must set "key" or "key-path" input')


def upload():
    ak = os.getenv('INPUT_AK')
    sk = os.getenv('INPUT_SK')
    log('ak:{}   sk:{}'.format(ak, sk))
    domain = os.getenv('INPUT_DOMAIN')
    log('domain: {}'.format(domain))
    domains = os.getenv('INPUT_UPDATE-DOMAINS')
    log('update-domins: {}' .format(domains))
    auth = qiniu.Auth(access_key=ak, secret_key=sk)
    manager = DomainManager(auth)

    privateKey = getKey()
    ca = getCert()
    log('ca bse64: {}'.format(base64.b64encode(
        ca.encode(encoding="utf-8")).decode()))
    log('privateKey base64: {}'.format(base64.b64encode(
        privateKey.encode(encoding="utf-8")).decode()))
    name = "{}/{}".format(domain, time.strftime("%Y-%m-%d", time.localtime()))
    ret, info = manager.create_sslcert(name, domain, privateKey, ca)
    log(ret)
    log(info)
    if not ret:
        raise Exception('no ret')
        pass

    if 'error' in info:
        print("error: {} ,code: {}, text_body: {}  , https://developer.qiniu.com/fusion/api/4248/certificate".format(
            info['error'], info['code'], info['text_body']))
        raise Exception(ret['error'])
    certId = ret['certID']
    for line in domains.split('\n'):
        d = line.split('|')
        dn = d[0].strip()
        redirect = False
        if len(d) > 1:
            redirect = True
        r, i = manager.put_httpsconf(dn, certId, redirect)
        log(r)
        log(i)
        pass


upload()
