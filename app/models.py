from app.extensions import db

class Vendor(db.Model):
    __tablename__ = "vendors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.Text)
    kra_pin = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    address = db.Column(db.Text)
    city = db.Column(db.String(255))
    postal_code = db.Column(db.String(255))
    county = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    bank_name = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(255), nullable=False)
    mpesa_paybill = db.Column(db.String(255))
    buy_goods_till = db.Column(db.String(255))
    contact_person_name = db.Column(db.String(255))
    contact_person_email = db.Column(db.String(255))
    contact_person_phone = db.Column(db.String(20))
    documents = db.relationship("Document", backref="vendor", lazy=True)

class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=False)


def create_tables():
    with db.engine.connect() as connection:
        connection.execute(db.text("""
            CREATE TABLE IF NOT EXISTS vendors (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(20) NOT NULL,
                bio TEXT,
                kra_pin VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT FALSE,
                address TEXT,
                city VARCHAR(255),
                postal_code VARCHAR(255),
                county VARCHAR(255) NOT NULL,
                country VARCHAR(255) NOT NULL,
                bank_name VARCHAR(255) NOT NULL,
                account_number VARCHAR(255) NOT NULL,
                mpesa_paybill VARCHAR(255),
                buy_goods_till VARCHAR(255),
                contact_person_name VARCHAR(255),
                contact_person_email VARCHAR(255),
                contact_person_phone VARCHAR(20)
            );
        """))

        connection.execute(db.text("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                file_url VARCHAR(255) NOT NULL,
                vendor_id INTEGER NOT NULL,
                FOREIGN KEY (vendor_id) REFERENCES vendors (id)
            );
        """))
