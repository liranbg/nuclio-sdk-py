# Copyright 2017 The Nuclio Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import io
import datetime

import nuclio_sdk.test


class TestLogger(nuclio_sdk.test.TestCase):
    def setUp(self):
        self._io = io.StringIO()
        self._logger = nuclio_sdk.Logger(logging.DEBUG)
        self._logger.set_handler('default', self._io, nuclio_sdk.logger.JSONFormatter())

    def tearDown(self):

        # override super tearDown
        pass

    def test_logger_sanity(self):

        # regular log line is printed
        self._logger.debug('TestA')
        self.assertIn('TestA', self._io.getvalue())

        # log line with text kwarg
        self._logger.debug_with('TestB', char='a')
        self.assertIn('TestB', self._io.getvalue())
        self.assertIn('"with":{"char":"a"}', self._io.getvalue())

        # log line with int kwarg
        self._logger.debug_with('TestC', number=1)
        self.assertIn('TestC', self._io.getvalue())
        self.assertIn('"with":{"number":1}', self._io.getvalue())

        date = datetime.datetime.fromisoformat('2019-12-04')
        self._logger.debug_with('TestD', date=date)
        self.assertIn('TestD', self._io.getvalue())
        self.assertIn('"with":{"date":"2019-12-04T00:00:00"}', self._io.getvalue())

    def _reset_io(self):
        self._io = io.StringIO()
