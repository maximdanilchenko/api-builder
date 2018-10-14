from appio.schema import fields, Schema


class Person(Schema):
    name = fields.String(default="Unknown")
