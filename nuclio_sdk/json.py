import sys

if sys.version_info[:2] < (3, 0):
    import simplejson as json

    class JSONEncoder(json.JSONEncoder):

        """JSON encoder that can encode custom stuff"""

        def default(self, obj):

            # Let the base class default method raise the TypeError
            return json.JSONEncoder.default(self, obj)

    encoder_base_class = JSONEncoder

else:
    import orjson as json

    class JSONEncoder(object):
        def encode(self, o):
            return json.dumps(o, default=self.default).decode('utf-8')

        def default(self, obj):
            if isinstance(obj, bytes):
                return obj.decode('utf-8')

            # Let the base class default method raise the TypeError
            return obj

    encoder_base_class = JSONEncoder


class Encoder(encoder_base_class):
    pass
