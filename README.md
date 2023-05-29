# upload cert to qiniu

## usage
```
    - name: update qiniu ${{ matrix.domain }}
      uses: foxundermoon/upload-qiniu-cert-action@master
      with:
        ak: ${{ secrets.QINIU_AK }}
        sk: ${{ secrets.QINIU_SK }}
        domain: ${{ matrix.domain }}
        update-domains: |
          .${{ matrix.domain }} | https | http2
          ${{ matrix.domain }} | https | http2
        debug: 'yes'
        cert-path: '${{ matrix.domain }}_ecc/fullchain.cer'
        key-path: '${{ matrix.domain }}_ecc/${{ matrix.domain }}.key'

```
