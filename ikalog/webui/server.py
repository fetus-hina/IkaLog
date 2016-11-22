#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  IkaLog
#  ======
#  Copyright (C) 2015 Takeshi HASEGAWA
#  Copyright (C) 2016 AIZAWA Hina
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from ikalog.utils import *
import os

class IkaLogWebUI(object):
    def __init__(self, address = "127.0.0.1", port=9042):
        IkaUtils.dprint(
            '{}: initialize server={}:{}'.format(self, address, port)
        )
        self._thread = IkaLogWebUIThread(address, port)

    def run(self):
        self._thread.start()

    def is_running(self):
        return self._thread.is_alive()

    def stop(self, wait = False):
        if self.is_running():
            self._thread.stop()
            if (wait):
                self._thread.join()

class IkaLogWebUIThread(Thread):
    def __init__(self, address, port):
        super(IkaLogWebUIThread, self).__init__()
        self._bind = (address, port)
        self._should_stop = False

    def run(self):
        self._httpd = HTTPServer(self._bind, IkaLogWebUIServer)
        while self._should_stop == False:
            self._httpd.handle_request()

    def stop(self):
        self._should_stop = True

class IkaLogWebUIServer(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super(IkaLogWebUIServer, self).__init__(*args, **kwargs)
        self._dir = os.path.join(os.path.dirname(__file__), 'web')

    def do_HEAD(self):
        self._send_method_not_allowed()

    def do_POST(self):
        self._send_method_not_allowed()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain;charset=UTF-8')
        self.end_headers()
        self.wfile.write(bytearray('Hello!', 'UTF-8'))

    def _send_method_not_allowed(self):
        self.send_response(405)
        self.send_header('Content-Type', 'text/plain;charset=UTF-8')
        self.end_headers()
        self.wfile.write(bytearray('Method not allowed.', 'UTF-8'))
