from app import db

class Vendor(db.Model):
    __tablename__ = "vendors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=True)
    postal_code = db.Column(db.String(255), nullable=True)
    county = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    kra_pin = db.Column(db.String(255), nullable=False)
    bank_name = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(255), nullable=False)
    mpesa_number = db.Column(db.String(20), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    documents = db.relationship("Document", backref="vendor", lazy=True)

    def __repr__(self):
        return f"<Vendor {self.name}>"

class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=False)

    def __repr__(self):
        return f"<Document {self.filename}>"
