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

import json

# since orjson is considered experimental we lazy load it


class Factory(object):
    @staticmethod
    def create_decoder(name):
        if name == "orjson":
            import orjson

            return orjson.loads
        return lambda o: json.loads(o.decode("utf-8"))

    @staticmethod
    def create_encoder(name):
        if name == "orjson":
            return OrJsonEncoder()

        # default
        return Encoder()

    @staticmethod
    def kinds():
        return [
            "json",
            "orjson",
        ]


# JSON encoder that can encode custom stuff
class Encoder(json.JSONEncoder):
    def default(self, obj):

        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class OrJsonEncoder(object):
    def encode(self, obj):
        import orjson

        return orjson.dumps(obj).decode()
