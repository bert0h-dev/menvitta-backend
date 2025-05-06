def add_default_response_envelope(result, generator, request, public):
  """
  Postprocessing hook para drf-spectacular.
  Envuelve todas las respuestas en el envelope estándar DataResponseSerializer,
  pero anida el schema real en el campo 'data' para que Swagger lo muestre correctamente.
  """

  STATUS_CODES_SUCCESS = ['200', '201']
  STATUS_CODES_ONLY_SUCCESS = ['204', '205']
  STATUS_CODES_NOT_SUCCESS = ['400', '401', '403', '404', '409', '422', '500']

  for path, path_item in result['paths'].items():
    for op in ['get', 'post', 'put', 'patch', 'delete']:
      if op in path_item:
        responses = path_item[op].get('responses', {})
        for code, resp in responses.items():
          if 'content' in resp and 'application/json' in resp['content']:
            schema = resp['content']['application/json'].get('schema')
            if code in STATUS_CODES_SUCCESS:
              resp['content']['application/json']['schema'] = {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "message": {"type": "string"},
                    "status_code":  {"type": "integer"},
                    "data": schema,
                    "errors": {
                      "oneOf": [
                        {"type": "object"},
                        {"type": "null"}
                      ]
                    },
                },
                "required": ["success", "message", "status_code", "data"]
              }
            elif code in STATUS_CODES_NOT_SUCCESS:
              resp['content']['application/json']['schema'] = {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "message": {"type": "string"},
                    "status_code":  {"type": "integer"},
                    "data": {
                      "oneOf": [
                        {"type": "object"},
                        {"type": "null"}
                      ]
                    },
                    "errors": schema,
                },
                "required": ["success", "message", "status_code", "errors"]
              }
            elif code in STATUS_CODES_ONLY_SUCCESS:
              resp['content']['application/json']['schema'] = {
                "type": "object",
                "properties": {
                    "status_code": {"type": "integer"},
                },
                "required": ["status_code"]
              }
  return result