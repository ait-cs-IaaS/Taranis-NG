from marshmallow import Schema, fields

from shared.schema.parameter import ParameterSchema
from shared.schema.parameter_value import ParameterValueSchema


class BotSchema(Schema):
    id = fields.Str()
    type = fields.Str()
    name = fields.Str()
    description = fields.Str()
    parameters = fields.List(fields.Nested(ParameterSchema))
    parameter_values = fields.List(fields.Nested(ParameterValueSchema))
