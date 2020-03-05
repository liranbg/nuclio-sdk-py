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

import datetime
import base64

import nuclio_sdk.test


class TestResponse(nuclio_sdk.test.TestCase):
    def setUp(self):
        self._encoder = nuclio_sdk.Encoder()

    def test_make_response_from_handle_response(self):
        now = datetime.datetime.now()
        handler_outputs = [

            # handler return body only
            {
                'handler_returns': 'test',
                'created_response': self._compile_output_response(body='test')
            },

            # handler return body and status code
            {
                'handler_returns': (201, 'test'),
                'created_response': self._compile_output_response(body='test',
                                                                  status_code=201)
            },

            # handler return dict body and status code
            {
                'handler_returns': (201, {'json': True}),
                'created_response': self._compile_output_response(body='{"json":true}',
                                                                  status_code=201,
                                                                  content_type='application/json')
            },

            # handler return dict only
            {
                'handler_returns': ({'json': True}),
                'created_response': self._compile_output_response(body='{"json":true}',
                                                                  content_type='application/json')
            },

            # handler return iterable only
            {
                'handler_returns': ([True]),
                'created_response': self._compile_output_response(body='[true]',
                                                                  content_type='application/json')
            },

            # handler return nuclio_sdk.Response with text body
            {
                'handler_returns': nuclio_sdk.Response(body='test'),
                'created_response': self._compile_output_response(body='test')
            },

            # handler return nuclio_sdk.Response with dict body
            {
                'handler_returns': nuclio_sdk.Response(body={'json': True}),
                'created_response': self._compile_output_response(body='{"json":true}',
                                                                  content_type='application/json')
            },

            # handler return int as body
            {
                'handler_returns': 2020,
                'created_response': self._compile_output_response(body=2020)
            },

            # handler return datetime
            {
                'handler_returns': now,
                'created_response': self._compile_output_response(body=now)
            },

            # handler return bytes, response with base64
            {
                'handler_returns': b'hello',
                'created_response': self._compile_output_response(body=base64.b64encode(b'hello').decode('ascii'),
                                                                  body_encoding='base64')
            },

        ]
        for handler_output in handler_outputs:
            response = nuclio_sdk.Response.from_entrypoint_output(self._encoder.encode,
                                                                  handler_output['handler_returns'])
            self.assertDictEqual(response, handler_output['created_response'])

    def _compile_output_response(self, **kwargs):
        return self._merge_dicts(nuclio_sdk.Response.empty_response(), {**kwargs})

    def _merge_dicts(self, d1, d2):
        """
        Creates a new dictionary d3, which is the sum of d1 and d2. d1 and d2's values remain unchanged

        :return: d3 which is d1 + d2
        """

        d3 = d1.copy()
        d3.update(d2)
        return d3
