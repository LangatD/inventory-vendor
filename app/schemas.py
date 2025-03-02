from marshmallow import Schema, fields

class DocumentSchema(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.Str(required=True)
    file_url = fields.Str(required=True)
    vendor_id = fields.Int(required=True)

class VendorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)
    address = fields.Str()
    postal_code = fields.Str()
    county = fields.Str(required=True)
    country = fields.Str(required=True)
    kra_pin = fields.Str(required=True)
    bank_name = fields.Str(required=True)
    account_number = fields.Str(required=True)
    mpesa_number = fields.Str()
    is_active = fields.Bool()
    documents = fields.Nested(DocumentSchema, many=True)
