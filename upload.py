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
    return open(fullPath, 'r').read().strip()


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
    log('ca : {}'.format(ca))
    log('privateKey : {}'.format(privateKey))
    name = "{}/{}".format(domain, time.strftime("%Y-%m-%d", time.localtime()))
    ret, info = manager.create_sslcert(name, domain, privateKey, ca)
    log(ret)
    log(info)
    if not ret:
        raise Exception('no ret')

    certId = ret['certID']
    for line in domains.strip().split('\n'):
        d = [e.strip().lower() for e in line.split('|')]
        dn = d[0]
        rest = d[1:]
        redirect = 'https' in rest
        http2 = 'http2' in rest
        log('domain: {} certId: {} , https: {} , http2: {}'.format(
            dn, certId, redirect, http2))
        r, i = manager.put_httpsconf(dn, certId, redirect, http2)
        log(r)
        log(i)
        pass


upload()
