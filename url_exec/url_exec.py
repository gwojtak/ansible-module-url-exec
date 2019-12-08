#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, Greg Wojtak <greg.wojtak@gmail.com>

from __future__ import print_function
from ansible.module_utils.basic import AnsibleModule

import requests
import hashlib
import tempfile
import subprocess

ANSIBLE_METADATA = {'metadata_version': "1.1",
                    'status': ["preview"],
                    'supported_by': "community"}

DOCUMENTATION = '''
---
module: url_exec
short_description: Run a script from a remote web url
description:
  - Execute a script from a remote web host, a la curl http://site.com/script | bash -s
options:
  url:
    description:
      - web url from which to stream the script
    required: true
  interpreter:
    description:
      - the executable under which to run the script (ie bash, python, ruby)
    required: false
    default: /bin/bash
  validate_certs:
    description:
      - if using https, do not enforce certificate verification
    required: false
    default: true
    type: bool
  checksum_type:
    description:
      - the type of checksum to run against the downloaded script.  Required if checksum is set.
    required: false
  checksum:
    description:
      - the expected sha checksum of the downloaded script.  Required if checksum_type is set.
    required: false
  temp_directory:
    description:
      - the temporary location to which the script is spooled
    required: false
    default: /tmp
requirements:
  - "python >= 2.7"
  - requests
author:
  - Greg Wojtak (@gwojtak)
'''

EXAMPLES = '''
---
- name: install rvm
  url_exec:
    url: https://get.rvm.io
    checksum_type: md5
    md5_checksum: 2b1b637c5ba9aadfa1383dc17095dda8

- name: install rvm
  url_exec:
    url: https://getcomposer.org/installer
    interpreter: 
      - php
      - -r
    checksum_type: sha384
    checksum: 93b54496392c062774670ac18b134c3b3a95e5a5e5c8f1a9f115f203b75bf9a129d5daa8ba6a13e2cc8a1da0806388a8
'''


class UrlExec(object):
    """
    url_exec module object encapsulation
    """

    def __init__(self, module):
        self.url = module['url']
        self.checksum_type = module['checksum_type']
        self.checksum = module['checksum']
        self.interpreter = module['interpreter']
        self.validate_certs = module['validate_certs']
        self.temp_directory = module['temp_directory']

        if self.checksum:
            if self.checksum_type not in hashlib.algorithms_available:
                module.fail_json(
                    msg="%s is an invalid checksum type" % self.checksum_type,
                    rc=1,
                    results=[],
                    changed=False
                )
            if not self.checksum:
                module.fail_json(
                    msg="checksum required when checksum_type specified",
                    rc=1,
                    results=[],
                    changed=False
                )

    def pull_script(self):
        hash_function = {
            'md5': hashlib.md5,
            'sha1': hashlib.sha1,
            'sha224': hashlib.sha224,
            'sha256': hashlib.sha256,
            'sha384': hashlib.sha384,
            'sha512': hashlib.sha512
        }
        resp = requests.get(self.url, verify=self.validate_certs)
        if self.cehcksum_type:
            self.calculated_hash = hash_function[self.checksum_type](
                resp.text).hexdigest()
        with tempfile.NamedTemporaryFile(dir=self.temp_directory) as tf:
            self.temp_file_name = tf.name
            tf.write(resp.text)

    def execute(self):
        subprocess.call([
            self.interpreter,
            self.temp_file_name
        ])

    def run(self):
        self.pull_script()
        self.exeecute()


def main():
    module = AnsibleModule(
        argument_spec={
            'url': {'required': True},
            'interpreter': {
                'required': False,
                'default': "/bin/bash",
            },
            'validate_certs': {
                'required': False,
                'default': True
            },
            'checksum_type': {
                'required': False,
                'default': None
            },
            'checksum': {
                'required': False,
                'default': None
            },
            'temp_directory': {
                'required': False,
                'default': "/tmp"
            }
        },
        supports_check_mode=False
    )
    url_exec = UrlExec(module)
    url_exec.run()


if '__main__' == __name__:
    main()
