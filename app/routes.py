from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from datetime import timedelta
from app import db
from app.models import Vendor, Document
from app.schemas import VendorSchema, DocumentSchema

vendor_bp = Blueprint("vendors", __name__)

vendor_schema = VendorSchema()
document_schema = DocumentSchema()

@vendor_bp.route('/generate_token', methods=['GET'])
def generate_token():
    access_token = create_access_token(identity="test_user", expires_delta=timedelta(hours=1))
    return jsonify(access_token=access_token), 200

@vendor_bp.route("/", methods=["POST"])
@jwt_required()
def create_vendor():
    data = request.get_json()
    errors = vendor_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    if Vendor.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "A vendor with this email already exists"}), 400

    new_vendor = Vendor(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        address=data["address"],
        postal_code=data["postal_code"],
        county=data["county"],
        country=data["country"],
        kra_pin=data["kra_pin"],
        bank_name=data["bank_name"],
        account_number=data["account_number"],
        mpesa_number=data.get("mpesa_number"),
        is_active=data.get("is_active", False)
    )
    db.session.add(new_vendor)
    db.session.commit()
    return jsonify(vendor_schema.dump(new_vendor)), 201

@vendor_bp.route("/<int:vendor_id>/documents", methods=["POST"])
@jwt_required()
def upload_document(vendor_id):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    document = Document(
        filename=file.filename,
        file_url=f'/uploads/{file.filename}',
        vendor_id=vendor_id
    )
    db.session.add(document)
    db.session.commit()

    return jsonify(document_schema.dump(document)), 201

@vendor_bp.route("/<int:vendor_id>/activate", methods=["PATCH"])
@jwt_required()
def toggle_vendor_activation(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    vendor.is_active = not vendor.is_active
    db.session.commit()
    status = "activated" if vendor.is_active else "deactivated"
    return jsonify({"message": f"Vendor {status}"}), 200

@vendor_bp.route('/', methods=['GET'])
@jwt_required()
def get_vendors():
    vendors = Vendor.query.all()
    return jsonify(vendor_schema.dump(vendors,many=True)), 200


@vendor_bp.route('/<int:vendor_id>', methods=['GET'])
@jwt_required()
def get_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    return jsonify(vendor_schema.dump(vendor)), 200


@vendor_bp.route('/<int:vendor_id>', methods=['PUT'])
@jwt_required()
def update_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(vendor, key, value)
    db.session.commit()
    return jsonify(vendor_schema.dump(vendor)), 200


@vendor_bp.route('/<int:vendor_id>', methods=['DELETE'])
@jwt_required()
def delete_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    db.session.delete(vendor)
    db.session.commit()
    return jsonify({"message": "Vendor deleted"}), 200