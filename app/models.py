from app.extensions import db

# SQLAlchemy models (used for ORM operations, not table creation)
class Vendor(db.Model):
    __tablename__ = "vendors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text)
    postal_code = db.Column(db.String(255))
    county = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    kra_pin = db.Column(db.String(255), nullable=False)
    bank_name = db.Column(db.String(255), nullable=False)
    account_number = db.Column(db.String(255), nullable=False)
    mpesa_number = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=False)
    documents = db.relationship("Document", backref="vendor", lazy=True)

class Document(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(255), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=False)

# Raw SQL for table creation
def create_tables():
    with db.engine.connect() as connection:
        connection.execute(db.text("""
            CREATE TABLE IF NOT EXISTS vendors (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(20) NOT NULL,
                address TEXT,
                postal_code VARCHAR(255),
                county VARCHAR(255) NOT NULL,
                country VARCHAR(255) NOT NULL,
                kra_pin VARCHAR(255) NOT NULL,
                bank_name VARCHAR(255) NOT NULL,
                account_number VARCHAR(255) NOT NULL,
                mpesa_number VARCHAR(20),
                is_active BOOLEAN DEFAULT FALSE
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