#Based in https://aviaryan.com/blog/gsoc/restplus-validation-custom-fields
from flask import abort, make_response, jsonify
from flask_restplus import fields
from api.utils.custom_fields import CustomField

def validate_payload(payload, api_model, validate_required=True):
    errors = {}
    # check if any reqd fields are missing in payload
    if validate_required:
        for key in api_model:
            if api_model[key].required and key not in payload:
                errors[key] = 'Required field \'%s\' missing' % key
    # check payload
    for key in payload:
        field = api_model[key]
        if isinstance(field, fields.List):
            field = field.container
            data = payload[key]
        else:
            data = [payload[key]]
        if isinstance(field, CustomField) and hasattr(field, 'validate'):
            #for i in data:
            for i in range(len(data)):
                if not field.validate(data[i]):
                    errors[i] = 'Validation of \'%s\' field failed' % key
    if len(errors)>0:
        abort(make_response(jsonify({
                'errors':errors,
                'message':'Request validation failed'
        }), 422))