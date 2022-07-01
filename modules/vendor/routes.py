from __future__ import division
from flask import request, jsonify, make_response, Blueprint
from flask_cors import CORS, cross_origin
from sqlalchemy.sql.sqltypes import BINARY, Binary
from modules import app ,per_page , db ,ALLOWED_EXTENSIONS ,UPLOAD_FOLDER
from sqlalchemy import create_engine
from sqlalchemy import exc
from numpy import genfromtxt
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from sqlalchemy.orm import sessionmaker
from modules.models import Item,Category,UOM,Vendor,Org,Association
import os
import datetime
import json
import pandas as pd
import math
import base64
import boto3
from botocore.exceptions import ClientError
    
vendor_module = Blueprint('vendor', __name__)
db.create_all()
CORS(app)

@app.route('/view-vendors', methods=['GET'])
@cross_origin()
def vendor():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Vendor).all()
            total_records = len(ResultSet)
            print(ResultSet)
            recordObject = {}
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            for record in ResultSet:
                categoryname = []
                category_name=db.session.query(Category).all()
                #if len(category_name) > 0:
                for code in category_name:
                    categoryname.append(code.category_name)
                #else :
                #categoryname = "Not Assigned"
                record_dict =  {'vendor_id' : record.vendor_id, 'vendor_type' : record.vendor_type,'selected_category_name': record.category_name, 'vendor_name' : record.vendor_name, 'category_name' : record.category_name, 'vendor_contact_person' : record.vendor_contact_person, 'vendor_phone_number' : record.vendor_phone_number, 'vendor_email' : record.vendor_email, 'vendor_address' : record.vendor_address, 'vendor_payment_terms' : record.vendor_payment_terms, 'vendor_terms_and_conditions' : record.vendor_terms_and_conditions, 'vendor_attachment' : record.vendor_attachment}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})

@app.route('/view-vendors-with-all-category', methods=['GET'])
@cross_origin()
def vendor_with_category_list():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Vendor).all()
            total_records = len(ResultSet)
            print(ResultSet)
            recordObject = {}
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            for record in ResultSet:
                categoryname = []
                category_name=db.session.query(Category).all()
                #if len(category_name) > 0:
                for code in category_name:
                    categoryname.append(code.category_name)
                #else :
                #categoryname = "Not Assigned"
                record_dict =  {'vendor_id' : record.vendor_id, 'vendor_type' : record.vendor_type,'selected_category_name': record.category_name, 'vendor_name' : record.vendor_name, 'category_name' : categoryname, 'vendor_contact_person' : record.vendor_contact_person, 'vendor_phone_number' : record.vendor_phone_number, 'vendor_email' : record.vendor_email, 'vendor_address' : record.vendor_address, 'vendor_payment_terms' : record.vendor_payment_terms, 'vendor_terms_and_conditions' : record.vendor_terms_and_conditions, 'vendor_attachment' : record.vendor_attachment}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})

@app.route('/add-vendor', methods=['POST'])
@cross_origin()
def vendor_insert():
    if request.method == "POST":
        #print(request.get_json(force=True))
        vendor_name = request.form['vendor_name']
        vendor_type = request.form['vendor_type']
        category_name = request.form['category_name']
        vendor_contact_person = request.form['vendor_contact_person']
        vendor_phone_number  = request.form['vendor_phone_number']
        vendor_email  = request.form['vendor_email']
        vendor_address  = request.form['vendor_address']
        vendor_payment_terms = request.form['vendor_payment_terms']
        vendor_terms_and_conditions = request.form['vendor_terms_and_conditions']
        yesfile = request.form['yesfile']
        #vendor_attachment  = request.json['vendor_attachment']
        cat_name = []
        
        try:
            inst = isinstance(category_name, list) 
            print(inst)
            
            if not inst :
                cat_name.append(category_name)
                print("not list")
                if yesfile == 'yes':
                    file = request.files['vendor_attachment']
                    name = file.filename
                    s3 = boto3.resource('s3',
                        aws_access_key_id='AKIAXLEI4XOIT7PJVTNE',
                        aws_secret_access_key= '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')
                    
                    s3.Bucket('warehouseattachments').put_object(Key=name,Body=file)
                    URL = 'https://warehouseattachments.s3.ap-south-1.amazonaws.com/'+name

                    vendor=Vendor( vendor_name = vendor_name, vendor_type = vendor_type, category_name = cat_name,
                    vendor_contact_person = vendor_contact_person,vendor_phone_number = vendor_phone_number,
                    vendor_email = vendor_email, vendor_address = vendor_address, vendor_payment_terms = vendor_payment_terms ,
                    vendor_terms_and_conditions = vendor_terms_and_conditions, vendor_attachment = URL )
                    association = Association(category = category_name, seller = vendor_name )
                else:
                    vendor=Vendor( vendor_name = vendor_name, vendor_type = vendor_type, category_name = cat_name,
                    vendor_contact_person = vendor_contact_person,vendor_phone_number = vendor_phone_number,
                    vendor_email = vendor_email, vendor_address = vendor_address, vendor_payment_terms = vendor_payment_terms ,
                    vendor_terms_and_conditions = vendor_terms_and_conditions )
                    association = Association(category = category_name, seller = vendor_name )

                    #os.remove(file_name)


                db.session.add(vendor)
                db.session.add(association)
                db.session.commit()
                print(vendor)
                print(association)
                return {str(vendor) : 'Added'} 
            else :
                print("is list")
                for categoryname in category_name:
                    cat_name.append(categoryname)
                    print("catname : ",categoryname)
                    print(vendor_name)
                    association = Association(category = categoryname, seller = vendor_name )
                    db.session.add(association)
                vendor=Vendor( vendor_name = vendor_name, vendor_type = vendor_type, category_name = cat_name,
                vendor_contact_person = vendor_contact_person,vendor_phone_number = vendor_phone_number,
                vendor_email = vendor_email, vendor_address = vendor_address, vendor_payment_terms = vendor_payment_terms ,
                vendor_terms_and_conditions = vendor_terms_and_conditions )
                db.session.add(vendor)
                db.session.commit()
                print(vendor)
                print(association)
                return {str(vendor) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

def allowed_file(filename):
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/update-vendor', methods=['PATCH'])
@cross_origin()
def vendor_update():
    if request.method == "PATCH":
        #print(request.get_json(force=True))
        category_name = request.form['category_name']
        vendor_id = request.form['vendor_id']
        vendor_name = request.form['vendor_name']
        vendor_type = request.form['vendor_type']
        vendor_contact_person = request.form['vendor_contact_person']
        vendor_phone_number = request.form['vendor_phone_number']
        vendor_email = request.form['vendor_email']
        vendor_address = request.form['vendor_address']
        vendor_payment_terms = request.form['vendor_payment_terms']
        vendor_terms_and_conditions = request.form['vendor_terms_and_conditions']
        cat_name = []
        yesfile = request.form['yesfile']
        try:
            inst = isinstance(category_name, list) 
            print(inst)
            if not inst :
                cat_name.append(category_name)
                print("not list")
                if yesfile == 'yes':
                    file = request.files['file']
                    name = file.filename
                    s3 = boto3.resource('s3',
                        aws_access_key_id='AKIAXLEI4XOIT7PJVTNE',
                        aws_secret_access_key= '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')
                    
                    s3.Bucket('warehouseattachments').put_object(Key=name,Body=file)
                    URL = 'https://warehouseattachments.s3.ap-south-1.amazonaws.com/'+name
                    ResultSet=db.session.query(Vendor).filter(Vendor.vendor_id == vendor_id).update({'vendor_type' : vendor_type, 'vendor_name' : vendor_name, 'category_name' : cat_name, 'vendor_contact_person' : vendor_contact_person, 'vendor_phone_number' : vendor_phone_number, 'vendor_email' : vendor_email, 'vendor_address' : vendor_address, 'vendor_payment_terms' : vendor_payment_terms, 'vendor_terms_and_conditions' : vendor_terms_and_conditions, 'vendor_attachment' : URL},synchronize_session=False)
                else:
                    ResultSet=db.session.query(Vendor).filter(Vendor.vendor_id == vendor_id).update({'vendor_type' : vendor_type, 'vendor_name' : vendor_name, 'category_name' : cat_name, 'vendor_contact_person' : vendor_contact_person, 'vendor_phone_number' : vendor_phone_number, 'vendor_email' : vendor_email, 'vendor_address' : vendor_address, 'vendor_payment_terms' : vendor_payment_terms, 'vendor_terms_and_conditions' : vendor_terms_and_conditions},synchronize_session=False)

                db.session.commit()
                return {'Status' : 'Updated'}
            else :
                print("is list")
                for categoryname in category_name:
                    cat_name.append(categoryname)
            
                ResultSet=db.session.query(Vendor).filter(Vendor.vendor_id == vendor_id).update({'vendor_type' : vendor_type, 'vendor_name' : vendor_name, 'category_name' : cat_name, 'vendor_contact_person' : vendor_contact_person, 'vendor_phone_number' : vendor_phone_number, 'vendor_email' : vendor_email, 'vendor_address' : vendor_address, 'vendor_payment_terms' : vendor_payment_terms, 'vendor_terms_and_conditions' : vendor_terms_and_conditions},synchronize_session=False)
        
                db.session.commit()
                return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

@app.route('/delete-vendor/<int:vendorid>', methods=['DELETE'])
@cross_origin()
def vendor_uom(vendorid):
    if request.method == "DELETE":
        record = Vendor.query.filter(Vendor.vendor_id== vendorid).delete()
        try:
            db.session.commit()
            return {'Status' : 'Deleted'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)


@app.route('/add-organisationn', methods=['PATCH'])
@cross_origin()
def organisation_isd():
    if request.method == "PATCH":
        #print(request.get_json(force=True))
        print('here')
        att = request.json['vendor_attachment']
        idd = request.json['id']
        res = db.session.query(Vendor).filter(Vendor.vendor_id == idd).update({'vendor_attachment' : BINARY(att)})
        try:
            db.session.commit()
            return jsonify({'status' : 'Inserted'}) 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return jsonify({'error':str(e)})