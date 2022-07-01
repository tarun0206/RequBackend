from __future__ import division
from flask import request, jsonify, make_response, Blueprint
from flask_cors import CORS, cross_origin
from modules import app ,per_page , db ,ALLOWED_EXTENSIONS ,UPLOAD_FOLDER
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from modules.models import Client,Site,Employee
from numpy import genfromtxt
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from modules.models import Client,Site,Employee,Vendor,UOM,Org,Item,Category,RateComparative,PO
import os
import datetime
import json
import pandas as pd
import math
import base64

po_module = Blueprint('po', __name__)
db.create_all()
CORS(app)

@app.route('/add-purchase-order', methods=['POST'])
@cross_origin()
def add_purchase_order():
    if request.method == "POST":
        print(request.get_json(force=True))
        po_delivery_address = request.json['delivery_address']
        po_billing_address = request.json['billing_address']
        po_vendor_name = request.json['vendor_name']
        po_total_price  = request.json['total_price']
        po_freight = request.json['freight']
        po_freight_gst = request.json['freight_gst']
        po_amount = request.json['amount']
        po_org = request.json['org']
        po_site = request.json['site']
        po_status = 'pending'
        po_vendor = request.json['vendor']
        po_rate_comparative = request.json['rate_comparative']
        #po_client = request.json['client']
        content  = request.json['content']

        po=PO(
        po_delivery_address = po_delivery_address,
        po8 = content,
        po_billing_address = po_billing_address,
        po_vendor_name = po_vendor_name,
        po_status = po_status,
        po_total_price  = po_total_price,
        po_freight = po_freight,
        po_amount = po_amount,
        po_org = po_org,
        po_vendor = po_vendor,
        po_site  = po_site,
        po_rate_comparative = po_rate_comparative,
        po_freight_gst = po_freight_gst)
        try:
            db.session.add(po)
            db.session.commit()
            print(po)
            return {str(po) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)



@app.route('/pending-purchase-order', methods=['GET'])
@cross_origin()
def pending_purchase_order():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(PO).filter(PO.po_status == 'pending').all()
            ResultSet1=db.session.query(PO).filter(PO.po_status == 'draft').all()
            total_records = len(ResultSet + ResultSet1)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            org_billing_address = ""
            client_name = ""
            org_contact_person = ""
            site_address = ""
            site_store_keeper = ""
            site_store_keeper_name = ""
            site_name = ""
            client_address = ""
            org_gst_no = ""
            emp_contact_person = ""
            for record in ResultSet:
                site = db.session.query(Site).filter(Site.id==record.po_site).all()
                for n in site:
                    site_address = n.address
                    site_name = n.site_name
                    store_keeper = db.session.query(Employee).filter(Employee.employee_id==n.store_keeper_id).all()
                    for contact in store_keeper:
                        site_store_keeper = contact.employee_contact
                        site_store_keeper_name = contact.employee_name
                org = db.session.query(Org).filter(Org.org_id == record.po_org).all()
                for name in org:
                    org_billing_address = name.org_address
                    org_contact_person = name.org_phone_number
                    org_gst_no = name.org_01
                    emp = db.session.query(Employee).filter(Employee.employee_id == name.org_contact_person_id).all()
                    for n in emp:
                        emp_contact_person = n.employee_name
                vendor = db.session.query(Vendor).filter(Vendor.vendor_id == record.po_vendor).all()
                for n in vendor:
                    client_address = n.vendor_address
                    client_name = n.vendor_name
                j = record.po_vendor_json
                with open('RC.json', 'w') as json_file:
                    json.dump(j, json_file)
                print("first")
                f = open('RC.json')
                po_vendor_json = json.load(f)
                asd = po_vendor_json['items']
                try:
                    final_req_id = asd[0]['req_id']
                except:
                    pass
                f.close()
                os.remove('RC.json')
                record_dict = {
                    'order_id' : record.id,
                    'req_id' : final_req_id,
                    'content' : record.po8,
                    'po_vendor_list' : record.po_vendor_json,
                    'vendor_name' : client_name,
                    'org_billing_address' : org_billing_address,
                    'org_gst_no' : org_gst_no,
                    'org_contact_person' : org_contact_person,
                    'emp_contact_person' : emp_contact_person,
                    'po_content' : record.po4,
                    'po_to' : record.po8,
                    'site_id' : record.po_site,
                    'po_from' : record.po3,
                    'site_address' : site_address,
                    'site_store_keeper_contact' : site_store_keeper,
                    'site_store_keeper_name' : site_store_keeper_name,
                    'site_name' : site_name,
                    'vendor_address' : client_address,
                    'vendor_payment_terms' : record.po7,
                    'po_req_number' : record.po_vendor_name,
                    'vendor_terms_and_conditions' : record.po6,
                    'po_number' : record.po5
                }
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/waiting-for-approval-po', methods=['GET'])
@cross_origin()
def waiting_for_approval_po():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(PO).filter(PO.po_status == 'sentforvendorapproval').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            org_billing_address = ""
            client_name = ""
            org_contact_person = ""
            site_address = ""
            site_store_keeper = ""
            site_store_keeper_name = ""
            site_name = ""
            client_address = ""
            emp_contact_person = ""
            org_gst_no = ""
            for record in ResultSet:
                site = db.session.query(Site).filter(Site.id==record.po_site).all()
                for n in site:
                    site_address = n.address
                    site_name = n.site_name
                    store_keeper = db.session.query(Employee).filter(Employee.employee_id==n.store_keeper_id).all()
                    for contact in store_keeper:
                        site_store_keeper = contact.employee_contact
                        site_store_keeper_name = contact.employee_name
                org = db.session.query(Org).filter(Org.org_id == record.po_org).all()
                for name in org:
                    org_billing_address = name.org_address
                    org_contact_person = name.org_phone_number
                    org_gst_no = name.org_01
                    emp = db.session.query(Employee).filter(Employee.employee_id == name.org_contact_person_id).all()
                    for n in emp:
                        emp_contact_person = n.employee_name
                vendor = db.session.query(Vendor).filter(Vendor.vendor_id == record.po_vendor).all()
                for n in vendor:
                    client_address = n.vendor_address
                    client_name = n.vendor_name
                j = record.po_vendor_json
                with open('RC.json', 'w') as json_file:
                    json.dump(j, json_file)
                print("first")
                f = open('RC.json')
                po_vendor_json = json.load(f)
                asd = po_vendor_json['items']
                try:
                    final_req_id = asd[0]['req_id']
                except:
                    pass
                f.close()
                os.remove('RC.json')
                record_dict = {
                    'order_id' : record.id,
                    'req_id' : final_req_id,
                    'content' : record.po8,
                    'po_vendor_list' : record.po_vendor_json,
                    'vendor_name' : client_name,
                    'org_billing_address' : org_billing_address,
                    'org_gst_no' : org_gst_no,
                    'org_contact_person' : org_contact_person,
                    'emp_contact_person' : emp_contact_person,
                    'po_content' : record.po4,
                    'po_to' : record.po8,
                    'site_id' : record.po_site,
                    'po_from' : record.po3,
                    'site_address' : site_address,
                    'site_store_keeper_contact' : site_store_keeper,
                    'site_store_keeper_name' : site_store_keeper_name,
                    'po_req_number' : record.po_vendor_name,
                    'site_name' : site_name,
                    'vendor_address' : client_address,
                    'vendor_payment_terms' : record.po7,
                    'vendor_terms_and_conditions' : record.po6,
                    'po_number' : record.po5
                }
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})



@app.route('/approved-po', methods=['GET'])
@cross_origin()
def approved_po():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(PO).filter(PO.po_status == 'approvedbyvendor').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            org_billing_address = ""
            client_name = ""
            org_contact_person = ""
            site_address = ""
            site_store_keeper_name = ""
            site_store_keeper = ""
            emp_contact_person = ""
            site_name = ""
            client_address = ""
            org_gst_no = ""
            for record in ResultSet:
                site = db.session.query(Site).filter(Site.id==record.po_site).all()
                for n in site:
                    site_address = n.address
                    site_name = n.site_name
                    store_keeper = db.session.query(Employee).filter(Employee.employee_id==n.store_keeper_id).all()
                    for contact in store_keeper:
                        site_store_keeper = contact.employee_contact
                        site_store_keeper_name = contact.employee_name
                org = db.session.query(Org).filter(Org.org_id == record.po_org).all()
                for name in org:
                    org_billing_address = name.org_address
                    org_contact_person = name.org_phone_number
                    org_gst_no = name.org_01
                    emp = db.session.query(Employee).filter(Employee.employee_id == name.org_contact_person_id).all()
                    for n in emp:
                        emp_contact_person = n.employee_name
                vendor = db.session.query(Vendor).filter(Vendor.vendor_id == record.po_vendor).all()
                for n in vendor:
                    client_address = n.vendor_address
                    client_name = n.vendor_name
                j = record.po_vendor_json
                with open('RC.json', 'w') as json_file:
                    json.dump(j, json_file)
                print("first")
                f = open('RC.json')
                po_vendor_json = json.load(f)
                asd = po_vendor_json['items']
                try:
                    final_req_id = asd[0]['req_id']
                except:
                    pass
                f.close()
                os.remove('RC.json')
                record_dict = {
                    'order_id' : record.id,
                    'req_id' : final_req_id,
                    'content' : record.po8,
                    'po_vendor_list' : record.po_vendor_json,
                    'vendor_name' : client_name,
                    'org_billing_address' : org_billing_address,
                    'org_gst_no' : org_gst_no,
                    'org_contact_person' : org_contact_person,
                    'emp_contact_person' : emp_contact_person,
                    'po_content' : record.po4,
                    'po_to' : record.po8,
                    'site_id' : record.po_site,
                    'po_from' : record.po3,
                    'site_address' : site_address,
                    'po_req_number' : record.po_vendor_name,
                    'site_store_keeper_contact' : site_store_keeper,
                    'site_store_keeper_name' : site_store_keeper_name,
                    'site_name' : site_name,
                    'vendor_address' : client_address,
                    'vendor_payment_terms' : record.po7,
                    'vendor_terms_and_conditions' : record.po6,
                    'po_number' : record.po5
                }
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/view-purchase-order', methods=['GET'])
@cross_origin()
def view_po():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(PO).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            org_billing_address = ""
            client_name = ""
            org_contact_person = ""
            site_address = ""
            site_store_keeper = ""
            site_store_keeper_name = ""
            site_name = ""
            client_address = ""
            org_gst_no = ""
            emp_contact_person = ""
            for record in ResultSet:
                site = db.session.query(Site).filter(Site.id==record.po_site).all()
                for n in site:
                    site_address = n.address
                    site_name = n.site_name
                    store_keeper = db.session.query(Employee).filter(Employee.employee_id==n.store_keeper_id).all()
                    for contact in store_keeper:
                        site_store_keeper = contact.employee_contact
                        site_store_keeper_name = contact.employee_name
                org = db.session.query(Org).filter(Org.org_location == record.po9).all()
                for name in org:
                    #org_billing_name = name.org_location
                    org_billing_address = name.org_address
                    org_contact_person = name.org_phone_number
                    org_gst_no = name.org_01
                    emp = db.session.query(Employee).filter(Employee.employee_id == name.org_contact_person_id).all()
                    for n in emp:
                        emp_contact_person = n.employee_name
                vendor = db.session.query(Vendor).filter(Vendor.vendor_id == record.po_vendor).all()
                for n in vendor:
                    client_address = n.vendor_address
                    client_name = n.vendor_name
                j = record.po_vendor_json
                with open('RC.json', 'w') as json_file:
                    json.dump(j, json_file)
                print("first")
                f = open('RC.json')
                po_vendor_json = json.load(f)
                asd = po_vendor_json['items']
                try:
                    final_req_id = asd[0]['req_id']
                except:
                    pass
                f.close()
                os.remove('RC.json')
                record_dict = {
                    'order_id' : record.id,
                    'req_id' : final_req_id,
                    'content' : record.po8,
                    'po_vendor_list' : record.po_vendor_json,
                    'vendor_name' : client_name,
                    'org_billing_name' : record.po9,
                    'org_billing_address' : org_billing_address,
                    'org_gst_no' : org_gst_no,
                    'org_contact_person' : org_contact_person,
                    'emp_contact_person' : emp_contact_person,
                    'po_content' : record.po4,
                    'po_to' : record.po8,
                    'po_from' : record.po3,
                    'site_address' : site_address,
                    'po_req_number' : record.po_vendor_name,
                    'site_id' : record.po_site,
                    'site_store_keeper_contact' : site_store_keeper,
                    'site_store_keeper_name' : site_store_keeper_name,
                    'site_name' : site_name,
                    'vendor_address' : client_address,
                    'vendor_payment_terms' : record.po7,
                    'vendor_terms_and_conditions' : record.po6,
                    'po_number' : record.po5
                }
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})



@app.route('/view-purchase-order/<poid>', methods=['GET'])
@cross_origin()
def view_po_by_poid(poid):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(PO).filter(PO.id == poid).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            org_billing_address = ""
            client_name = ""
            org_contact_person = ""
            site_address = ""
            site_store_keeper = ""
            site_store_keeper_name = ""
            site_name = ""
            emp_contact_person = ""
            client_address = ""
            org_gst_no = ""
            for record in ResultSet:
                site = db.session.query(Site).filter(Site.id==record.po_site).all()
                for n in site:
                    site_address = n.address
                    site_name = n.site_name
                    store_keeper = db.session.query(Employee).filter(Employee.employee_id==n.store_keeper_id).all()
                    for contact in store_keeper:
                        site_store_keeper = contact.employee_contact
                        site_store_keeper_name = contact.employee_name
                org = db.session.query(Org).filter(Org.org_location == record.po9).all()
                for name in org:
                    #org_billing_name = name.org_location
                    org_billing_address = name.org_address
                    org_contact_person = name.org_phone_number
                    org_gst_no = name.org_01
                    emp = db.session.query(Employee).filter(Employee.employee_id == name.org_contact_person_id).all()
                    for n in emp:
                        emp_contact_person = n.employee_name
                vendor = db.session.query(Vendor).filter(Vendor.vendor_id == record.po_vendor).all()
                for n in vendor:
                    client_address = n.vendor_address
                    client_name = n.vendor_name
                j = record.po_vendor_json
                with open('RC.json', 'w') as json_file:
                    json.dump(j, json_file)
                print("first")
                f = open('RC.json')
                po_vendor_json = json.load(f)
                asd = po_vendor_json['items']
                try:
                    final_req_id = asd[0]['req_id']
                except:
                    pass
                f.close()
                os.remove('RC.json')
                record_dict = {
                    'order_id' : record.id,
                    'req_id' : final_req_id,
                    'content' : record.po8,
                    'po_vendor_list' : record.po_vendor_json,
                    'vendor_name' : client_name,
                    'org_billing_name' : record.po9,
                    'org_billing_address' : org_billing_address,
                    'org_gst_no' : org_gst_no,
                    'org_contact_person' : org_contact_person,
                    'emp_contact_person' : emp_contact_person,
                    'po_content' : record.po4,
                    'po_to' : record.po8,
                    'po_from' : record.po3,
                    'site_address' : site_address,
                    'po_req_number' : record.po_vendor_name,
                    'site_store_keeper_contact' : site_store_keeper,
                    'site_store_keeper_name' : site_store_keeper_name,
                    'site_id' : record.po_site,
                    'site_name' : site_name,
                    'vendor_address' : client_address,
                    'vendor_payment_terms' : record.po7,
                    'vendor_terms_and_conditions' : record.po6,
                    'po_number' : record.po5
                }
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/po-status-update', methods=['PATCH'])
@cross_origin()
def po_status_update():
    if request.method == "PATCH":
        print(request.get_json(force=True))
        po_status = request.json['po_status']
        po_id = request.json['po_id']
        ResultSet=db.session.query(PO).filter(PO.id == po_id).update({'po_status' : po_status},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)


@app.route('/po-update-access', methods=['PATCH'])
@cross_origin()
def po_status_access():
    if request.method == "PATCH":
        print(request.get_json(force=True))
        po_content = request.json['po_content']
        po_from = request.json['po_from']
        po_to = request.json['po_to']
        po_number = request.json['po_number']
        po_payment_terms = request.json['po_payment_terms']
        po_terms_conditions = request.json['po_terms_conditions']
        po_id = request.json['po_id']
        po_billing_name = request.json['org_billing_name']
        site=db.session.query(PO).filter(PO.id == po_id).all()
        for s in site:
            #s.po_site = site_id
            ResultSet=db.session.query(PO).filter(PO.id == po_id).update({'po4' : po_content, 'po8' : po_to, 'po3' : po_from, 'po5' : po_number, 'po6' : po_terms_conditions, 'po7' : po_payment_terms, 'po_site_no' : s.po_site, 'po9' : po_billing_name},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

@app.route('/po-update-table/<po_id>', methods=['PATCH'])
@cross_origin()
def po_table_update(po_id = None):
    if request.method == "PATCH":
        ResultSet = db.session.query(PO).filter(PO.id == po_id).all()
        for record in ResultSet:
            j = record.po_vendor_json
            with open('RC.json', 'w') as json_file:
                json.dump(j, json_file)
            f = open('RC.json')
            po_vendor_json = json.load(f)
            po_vendor_json['CGST'] = request.json['CGST']
            po_vendor_json['SGST'] = request.json['SGST']
            po_vendor_json['IGST'] = request.json['IGST']
            Update = db.session.query(PO).filter(PO.id == po_id).update({'po_vendor_json' : po_vendor_json},synchronize_session=False)
            db.session.commit()
        f.close()
        os.remove('RC.json')
        try:
            db.session.commit()
            return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

@app.route('/landing-po', methods=['GET'])
@cross_origin()
def view_po_screen():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(PO).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            org_billing_address = ""
            client_name = ""
            org_contact_person = ""
            site_address = ""
            site_store_keeper = ""
            site_store_keeper_name = ""
            client_address = ""
            org_gst_no = ""
            emp_contact_person = ""
            for record in ResultSet:
                site = db.session.query(Site).filter(Site.id==record.po_site).all()
                for n in site:
                    site_address = n.address
                    store_keeper = db.session.query(Employee).filter(Employee.employee_id==n.store_keeper_id).all()
                    for contact in store_keeper:
                        site_store_keeper = contact.employee_contact
                        site_store_keeper_name = contact.employee_name
                org = db.session.query(Org).filter(Org.org_id == record.po_org).all()
                for name in org:
                    org_billing_address = name.org_address
                    org_contact_person = name.org_phone_number
                    org_gst_no = name.org_01
                    emp = db.session.query(Employee).filter(Employee.employee_id == name.org_contact_person_id).all()
                    for n in emp:
                        emp_contact_person = n.employee_name
                vendor = db.session.query(Vendor).filter(Vendor.vendor_id == record.po_vendor).all()
                for n in vendor:
                    client_address = n.vendor_address
                    client_name = n.vendor_name
                record_dict = {
                    'order_id' : record.id,
                    'content' : record.po8,
                    'vendor_name' : client_name,
                    'org_billing_address' : org_billing_address,
                    'org_gst_no' : org_gst_no,
                    'org_contact_person' : org_contact_person,
                    'emp_contact_person' : emp_contact_person,
                    'po_vendor_list' : record.po_vendor_json,
                    'site_address' : site_address,
                    'site_store_keeper_contact' : site_store_keeper,
                    'site_store_keeper_name' : site_store_keeper_name,
                    'vendor_address' : client_address,
                    'site_id' : record.po_site,
                    'po_req_number' : record.po_vendor_name,
                    'vendor_payment_terms' : record.po7,
                    'vendor_terms_and_conditions' : record.po6,
                    'po_number' : record.po5
                }
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})
            


@app.route('/view-last-po/<siteid>', methods=['GET'])
@cross_origin()
def view_last_po(siteid = None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(PO).all()
            sites = 1
            for record in ResultSet:
                if record.po_site_no == None:
                    pass
                elif int(record.po_site_no)== int(siteid):
                    sites += 1
                else:
                    pass
            if sites > 1:
                record_dict = {
                'po_id' : sites}
            else:
                record_dict = {
                'po_id' : 1}
                #data.append(record_dict)
            return jsonify(record_dict)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

                        