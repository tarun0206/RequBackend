
from __future__ import division
from flask import request, jsonify, make_response, Blueprint
from flask_cors import CORS, cross_origin
from modules import app ,per_page , db ,ALLOWED_EXTENSIONS ,UPLOAD_FOLDER
from sqlalchemy import create_engine
from sqlalchemy import exc
from numpy import genfromtxt
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from sqlalchemy.orm import sessionmaker
from modules.models import Item,Category,UOM,Vendor,Org,Association,Employee,User
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask import Flask, flash, request, redirect, url_for
import os
import datetime
import json
import pandas as pd
import math
import base64
import boto3
from botocore.exceptions import ClientError
    
org_module = Blueprint('org', __name__)
db.create_all()
CORS(app)

@app.route('/view-organisations', methods=['GET'])
@cross_origin()
def organisation():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Org).all()
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
                emp_details=db.session.query(Employee).filter(Employee.employee_id==record.org_contact_person_id).all()
                if len(emp_details) > 0:
                    employee_name = emp_details[0].employee_name
                    employee_email = emp_details[0].employee_email
                    employee_contact = emp_details[0].employee_contact
                    employee_designation = emp_details[0].employee_designation

                record_dict =  {'org_id' :record.org_id, 'org_location' : record.org_location, 'emp_contact_person' : employee_name, 'emp_designation' : employee_designation, 'org_phone_number' : record.org_phone_number, 'org_email' : record.org_email, 'org_address' : record.org_address, 'gst_no' : record.org_01, 'org_attachment' : record.org_02, 'org_code' : record.org_03}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})

@app.route('/add-organisation', methods=['POST'])
@cross_origin()
def organisation_insert():
    if request.method == "POST":
        #print(request.get_json(force=True))
        print('here')
        org_location = request.form['org_location']
        print(org_location)
        org_contact_person = request.form['org_contact_person']
        org_phone_number = request.form['org_phone_number']
        org_email = request.form['org_email']
        org_designation  = request.form['org_designation']
        org_address  = request.form['org_address']
        gst_no = request.form['gst_no']
        org_code = request.form['org_code']
        fileyes = request.form['yesfile']
        #file = request.files['file']
        if fileyes == 'yes':
            file = request.files['file']
            name = file.filename
            s3 = boto3.resource('s3',
                aws_access_key_id='AKIAXLEI4XOIT7PJVTNE',
                aws_secret_access_key= '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')
            
            s3.Bucket('warehouseattachments').put_object(Key=name,Body=file)
            URL = 'https://warehouseattachments.s3.ap-south-1.amazonaws.com/'+name

            org=Org(org_location = org_location, org_contact_person_id = org_contact_person, 
            org_phone_number = org_phone_number, org_email = org_email, org_designation = org_designation, org_01 = gst_no, org_address = org_address, org_03 = org_code, org_02 = URL)
       
        else:
            
            file = None
            org=Org(org_location = org_location, org_contact_person_id = org_contact_person, 
            org_phone_number = org_phone_number, org_email = org_email, org_designation = org_designation, org_01 = gst_no, org_address = org_address, org_03 = org_code)
            
        
        try:
            db.session.add(org)
            db.session.commit()
            print(org)
            return jsonify({str(org) : 'Inserted'}) 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return jsonify({'error':str(e)})

@app.route('/update-organisation', methods=['PATCH'])
@cross_origin()
def organisation_update():
    if request.method == "PATCH":
        #print(request.get_json(force=True))
        org_id = request.form['org_id']
        org_location = request.form['org_location']
        org_contact_person = request.form['org_contact_person_id']
        org_address = request.form['org_address']
        org_designation  = request.form['org_designation']
        org_phone_number = request.form['org_phone_number']
        org_email = request.form['org_email']
        gst_no = request.form['gst_no']
        org_code = request.form['org_code']
        yesfile = request.form['yesfile']
        if yesfile == 'yes':
            file = request.files['file']
            name = file.filename
            s3 = boto3.resource('s3',
                aws_access_key_id='AKIAXLEI4XOIT7PJVTNE',
                aws_secret_access_key= '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')
            
            s3.Bucket('warehouseattachments').put_object(Key=name,Body=file)
            URL = 'https://warehouseattachments.s3.ap-south-1.amazonaws.com/'+name
            ResultSet=db.session.query(Org).filter(Org.org_id == org_id).update({'org_location' : org_location, 'org_contact_person_id' : org_contact_person, 
            'org_address' : org_address, 'org_01' : gst_no,'org_phone_number' : org_phone_number, 'org_email' : org_email,'org_designation' : org_designation, 'org_03' : org_code , 'org_02' : URL},synchronize_session=False)
        else:
            ResultSet=db.session.query(Org).filter(Org.org_id == org_id).update({'org_location' : org_location, 'org_contact_person_id' : org_contact_person, 
            'org_address' : org_address, 'org_01' : gst_no,'org_phone_number' : org_phone_number, 'org_email' : org_email,'org_designation' : org_designation, 'org_03' : org_code},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

def allowed_file(filename):
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/delete-org/<int:orgid>', methods=['DELETE'])
@cross_origin()
def org_uom(orgid):
    if request.method == "DELETE":
        record = Org.query.filter(Org.org_id== orgid).delete()
        try:
            db.session.commit()
            return {'Status' : 'Deleted'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!" 

@app.route('/login', methods=['POST'])
def do_admin_login():

    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])

    Session = sessionmaker()
    query = db.session.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) ).first()
    #result = query.first()
    if query:
        session['logged_in'] = True
        return "hey there"
    else:
        flash('wrong password!')
        return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()
