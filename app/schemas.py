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
    
    # Contact person fields
    contact_person_name = fields.Str()
    contact_person_email = fields.Email()
    contact_person_phone = fields.Str()

    documents = fields.Nested(DocumentSchema, many=True)
