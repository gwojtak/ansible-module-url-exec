# ansible-module-url-exec
An ansible module that simulates the common installer shell command
`curl -o - https://somesamplesite.com/install.sh | bash`

## Usage
```yaml
- name: install rvm
  url_exec:
    url: https://get.rvm.io
    checksum_type: md5
    md5_checksum: 2b1b637c5ba9aadfa1383dc17095dda8
```

## Donations
If you find this module useful, please consider donating

| Crypto        |                                            |
|---------------|--------------------------------------------|
| Bitcoin:      | 3Qvu1C8gFjdJa85mFf1de5EteWt46CkY81         |
| Bitcoin Cash: | qpk0k0lv5elly2h9e7k7d92nwjhsafngrym2ezr4xa |
| Litecoin:     | M96796s5j5YFdfWtp43yDFxVosSn4jGLW3         |
| Ethereum:     | 0xa94671089a1f44774edc8Ae656EB737C6024f8e2 |
| Dai:          | 0x5F1EE697372292eb9018D5BD1ED06eeDDD8E2459 |
