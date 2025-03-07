from flask import Blueprint, request, jsonify,send_file,current_app
from flask_jwt_extended import jwt_required

from app import db
from app.models import Vendor, Document,Orders
from app.schemas import VendorSchema, DocumentSchema
from sqlalchemy import text
import os
from werkzeug.utils import secure_filename

vendor_bp = Blueprint("vendors", __name__)

vendor_schema = VendorSchema()
document_schema = DocumentSchema()


@vendor_bp.route("/", methods=["POST"])
@jwt_required()
def create_vendor():
    data = request.get_json()
    errors = vendor_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    if Vendor.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "A vendor with this email already exists"}), 400


    vendor = Vendor(**data)
    db.session.add(vendor)
    db.session.commit()

    return jsonify(vendor_schema.dump(vendor)), 201




@vendor_bp.route("/<int:vendor_id>/documents", methods=["POST"])
@jwt_required()
def upload_document(vendor_id):
    db.session.expire_all()
    allowed_extensions = {'.pdf', '.docx', '.xlsx'}
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    _, file_extension = os.path.splitext(filename)
    if file_extension not in allowed_extensions:
        return jsonify({'error': 'File type not allowed'}), 400

    upload_folder = current_app.config['UPLOAD_FOLDER']
    vendor_folder = os.path.join(upload_folder, str(vendor_id))
    os.makedirs(vendor_folder, exist_ok=True)
    file_path = os.path.join(vendor_folder, filename)
    file.save(file_path)

    document = Document(
        filename=os.path.splitext(filename)[0],
        file_url=f'/uploads/{vendor_id}/{filename}',
        vendor_id=vendor_id,
        filetype=file.content_type
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
    return jsonify(vendor_schema.dump(vendors, many=True)), 200

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

    allowed_fields = [
        "name", "email", "phone", "bio", "kra_pin", "is_active", "address",
        "city", "postal_code", "county", "country", "bank_name", "account_number",
        "mpesa_paybill", "buy_goods_till", "contact_person_name",
        "contact_person_email", "contact_person_phone"
    ]

    try:
        for key, value in data.items():
            if key in allowed_fields:
                setattr(vendor, key, value)
        
        db.session.commit()
        return jsonify({
            "message": "Vendor updated successfully",
            "vendor": vendor_schema.dump(vendor)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update vendor", "details": str(e)}), 500


@vendor_bp.route('/<int:vendor_id>', methods=['DELETE'])
@jwt_required()
def delete_vendor(vendor_id):
    vendor = Vendor.query.get_or_404(vendor_id)
    db.session.delete(vendor)
    db.session.commit()
    return jsonify({"message": "Vendor deleted"}), 200

@vendor_bp.route('/<int:vendor_id>/orders', methods=['GET'])
@jwt_required()
def get_vendor_orders(vendor_id):
    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        return jsonify({"error": "Vendor not found"}), 404
    
    orders = Orders.query.filter_by(vendor_id=vendor_id).all()
    orders_data = [
        {"order.id": order.id, "item": order.name, "quantity": order.quantity, "total_amount": str(order.cost)}
        for order in orders
    ]
    return jsonify(orders_data)

@vendor_bp.route('/<int:vendor_id>/documents/<int:document_id>/download', methods=['GET'])
@jwt_required()
def download_vendor_document(vendor_id, document_id):
    document = Document.query.filter_by(id=document_id, vendor_id=vendor_id).first()
    if not document:
        return jsonify({"error": "Document not found"}), 404

    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(vendor_id), os.path.basename(document.file_url))
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found on server"}), 404

    return send_file(file_path, as_attachment=True, download_name=document.filename or "downloaded file")

@vendor_bp.route('/<int:vendor_id>/documents/<int:document_id>', methods=['DELETE'])
@jwt_required()
def delete_document(vendor_id, document_id):
    document = Document.query.filter_by(id=document_id, vendor_id=vendor_id).first()

    if not document:
        return jsonify({"error": "Document not found"}), 404

    db.session.delete(document)
    db.session.commit()

    return jsonify({"message": "Document deleted successfully"}), 200