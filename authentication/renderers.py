import json
from rest_framework.renderers import JSONRenderer


class UserJsonRender(JSONRenderer):
    ''' User renderer '''
    charset = 'utf-8'

    def render(self, data, media_type, renderer_context):
        if 'errors' in data or 'detail' in data:
            return super().render(data)
        return json.dumps({
            'user': data
        })
