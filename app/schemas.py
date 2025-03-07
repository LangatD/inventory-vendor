from marshmallow import Schema, fields, validate

class DocumentSchema(Schema):
    id = fields.Int(dump_only=True)
    filename = fields.Str(required=True)
    filetype = fields.Str(required=True)
    file_url = fields.Str(required=True)
    vendor_id = fields.Int(required=True)

class VendorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True, error_messages={"invalid": "Invalid email format."})
    phone = fields.Str(
        required=True,
        validate=[validate.Length(min=10, max=20), validate.Regexp(r'^\+?\d+$', error="Phone number must contain only digits.")]
    )
    bio = fields.Str()
    kra_pin = fields.Str(required=True)
    is_active = fields.Bool()
    address = fields.Str()
    city = fields.Str()
    postal_code = fields.Str()
    county = fields.Str(required=True)
    country = fields.Str(required=True)
    bank_name = fields.Str(required=True)
    account_number = fields.Str(required=True)
    mpesa_paybill = fields.Str()
    buy_goods_till = fields.Str()
    
    
    contact_person_name = fields.Str()
    contact_person_email = fields.Email(error_messages={"invalid": "Invalid email format."})
    contact_person_phone = fields.Str(validate=[validate.Length(min=10, max=20), validate.Regexp(r'^\+?\d+$', error="Phone number must contain only digits.")] )
    documents = fields.Nested(DocumentSchema, many=True)
