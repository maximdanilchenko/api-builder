from api_builder.schema import fields, Schema


class Person(Schema):
    name = fields.String(default="Unknown")
