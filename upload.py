#! /usr/bin/env python

import qiniu
from qiniu import DomainManager
import os
import time


def log(line):
    debug = os.getenv('INPU_DEBUG')
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
    domain = os.getenv('INPUT_DOMAIN')
    domains = os.getenv('INPUT_UPDATE_DOMAINS')
    auth = qiniu.Auth(access_key=ak, secret_key=sk)
    manager = DomainManager(auth)

    privateKey = getKey()
    ca = getCert()
    name = "{}/{}".format(domain, time.strftime("%Y-%m-%d", time.localtime()))
    ret, info = manager.create_sslcert(name, domain, privateKey, ca)
    log(ret)
    log(info)
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
