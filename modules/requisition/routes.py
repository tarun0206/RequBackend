from __future__ import division
from flask import request, jsonify, make_response, Blueprint
from flask_cors import CORS, cross_origin
from modules import app ,per_page , db ,ALLOWED_EXTENSIONS ,UPLOAD_FOLDER
from sqlalchemy import create_engine
from sqlalchemy import exc, desc
from sqlalchemy.orm import sessionmaker
from modules.models import Client, Site, Employee, Requisition#, RequisitionItemAssociation
from numpy import genfromtxt
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from modules.models import Client,Site,Employee,Vendor,UOM,Org,Item,Category,RateComparative,PO,History
import os
from datetime import datetime, timedelta
import json
import datetime
import pandas as pd
import math
import base64
import uuid
    
requisition_module = Blueprint('requisition', __name__)
db.create_all()
CORS(app)
'''
@app.route('/create-requisition', methods=['POST'])
@cross_origin()
def create_requisition():
    if request.method == "POST":
        request.get_json(force=True)
        title = request.json['title']
        urgent_requirement = request.json['urgent_requirement']
        local_purchase = request.json['local_purchase']
        req_number = request.json['req_number']
        site  = request.json['site']
        items  = request.json['items']
        
        created_at = datetime.datetime.today()
        rate_comp_version = 0
        requisition = Requisition(
            req_title = rate_comp_requisition_title,
            req_site = rate_comp_urgent_requirement,
            req_created_at = rate_comp_local_purchase,
            req_urgent_requirement  = rate_comp_site_name,
            req_local_purchase  = rate_comp_request_date,
            )

@app.route('/add-requisition', methods=['POST'])
@cross_origin()
def addd_requisition():
    if request.method == "POST":
        print(request.get_json(force=True))
        req_title = request.json['req_title']
        req_site = request.json['req_site']
        #req_created_at = request.json['req_created_at']
        req_urgent_requirement = request.json['req_urgent_requirement']
        req_local_purchase  = request.json['req_local_purchase']
        #req_version  = request.json['req_version']
        #history_qty = request.json['history_qty']
        remarks = request.json['remarks']
        #created_at = request.json['created_at']
        created_by = request.json['created_by']
        req_item = request.json['req_item']
        req_uom = request.json['req_uom']
        req_category = request.json['req_category']
        req_sub_category = request.json['created_by']
        req_intended_end_use = request.json['req_intended_end_use']
        req_status = 'pending'
        created_at = datetime.datetime.today()
        update_by = request.json['update_by']
        update_at = datetime.datetime.today()
        requisition=Requisition(
        req_title = req_title,
        req_site = req_site,
        created_at = created_at,
        req_urgent_requirement = req_urgent_requirement,
        req_local_purchase  = req_local_purchase,
        #req_version  = req_version,
        req_status = req_status,
        # history_qty = history_qty,
        remarks = remarks,
        update_by = update_by,
        created_by = created_by,
        req_item = req_item,
        req_uom = req_uom,
        req_category = req_category,
        req_sub_category = req_sub_category,
        req_intended_end_use = req_intended_end_use,
        update_at = update_at)
        try:
            db.session.add(requisition)
            db.session.commit()
            print(requisition)
            return {str(requisition) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)
            '''

@app.route('/add-requisition', methods=['PUT'])
@cross_origin()
def add_requisition():
    if request.method == "PUT":
        print(request.get_json(force=True))
        req_title = request.json['req_title']
        req_site = request.json['req_site']
        req_urgent_requirement = request.json['req_urgent_requirement']
        req_local_purchase  = request.json['req_local_purchase']
        req_item_list = request.json['items']
        req_status = 'pending'
        updated_by = request.json['updated_by']
        created_by = request.json['created_by']
        req_number = request.json['req_number']
        req_no = request.json['req_no']
        site_id = request.json['site_id']
        created_at = datetime.datetime.today()
        updated_at = datetime.datetime.today()

        rate_comp_version = 0
        requisition=Requisition(
        req_title = req_title,
        req_site = req_site,
        req_urgent_requirement = req_urgent_requirement,
        req_local_purchase  = req_local_purchase,
        updated_at  = updated_at,
        req_item_list = req_item_list,
        req_status = req_status,
        created_by = created_by,
        req04 = req_number,
        updated_by = updated_by,
        created_at = created_at)

        sitess = db.session.query(Site).filter(Site.id == site_id).update({'si16': req_no})
        try:
            db.session.add(requisition)
            db.session.commit()
            print(requisition)
            return {str(requisition) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)


@app.route('/update-requisition', methods=['PATCH'])
@cross_origin()
def requisition_update():
    if request.method == "PATCH":
        print(request.get_json(force=True))
        req_title = request.json['req_title']
        req_urgent_requirement = request.json['req_urgent_requirement']
        req_local_purchase  = request.json['req_local_purchase']
        updated_by = request.json['updated_by']
        req_id = request.json['req_id']
        req_item_list = request.json['items']
        updated_at = datetime.datetime.today()

        ResultSet=db.session.query(Requisition).filter(Requisition.req_id == req_id).update({'req_title' : req_title, 
        'req_urgent_requirement' : req_urgent_requirement, 'req_local_purchase' : req_local_purchase, 'updated_by' : updated_by, 'req_item_list' : req_item_list, 'updated_at' : updated_at},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)


@app.route('/approval-remarks-update/<req_id>', methods=['PATCH'])
@cross_origin()
def approval_remarks_update(req_id = None):
    if request.method == "PATCH":
        print(request.get_json(force=True))
        req_remarks = request.json['remarks']
        ResultSet=db.session.query(Requisition).filter(Requisition.req_id == req_id).update({'req_remarks' : req_remarks},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)
            

@app.route('/view-approved-req', methods=['GET'])
@cross_origin()
def view_approved_req():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Requisition).filter(Requisition.req_status == 'approved').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name

                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_number' : record.req04,
                'req_site' : req_sitename}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/view-revised-req', methods=['GET'])
@cross_origin()
def view_revised_req():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Requisition).filter(Requisition.req_status == 'revised').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name

                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_number' : record.req04,
                'req_site' : req_sitename}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})



@app.route('/view-pending-req', methods=['GET'])
@cross_origin()
def view_pending_req():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Requisition).filter(Requisition.req_status == 'pending').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name

                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_number' : record.req04,
                'req_site' : req_sitename}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})



@app.route('/view-rejected-req', methods=['GET'])
@cross_origin()
def view_rejected_req():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Requisition).filter(Requisition.req_status == 'rejected').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name

                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_number' : record.req04,
                'req_site' : req_sitename}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/requisition-pending-alll', methods=['GET'])
@cross_origin()
def requisition_pending_alll():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Requisition).filter(Requisition.req_status == 'pending').all()
            total_records = len(ResultSet)
            print(total_records)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                print(record.req_id)
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name
                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_site' : req_sitename,
                'req_number' : record.req04}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/requisition-all', methods=['GET'])
@cross_origin()
def requisition_aproved():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Requisition).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name
                record_dict = {
                'req_id' : record.req_id,
                'title' : record.req_title,
                'created_at' : record.created_at,
                'site' : req_sitename,
                'items' : record.req_item_list,
                'req_number' : record.req04,
                'remarks' : record.req_remarks,
                'urgent_requirement' : record.req_urgent_requirement,
                'local_use' : record.req_local_purchase}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/requisition-pending-all', methods=['GET'])
@cross_origin()
def requisition_pending_all():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Requisition).filter(Requisition.req_status == 'pending').all()
            total_records = len(ResultSet)
            print(total_records)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                print(record.req_id)
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name
                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_site' : req_sitename,
                'req_number' : record.req04}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})
            

@app.route('/requisition-all/<reqid>', methods=['GET'])
@cross_origin()
def requisition_by_reqid(reqid = None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Requisition).filter(Requisition.req_id == reqid).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name
                record_dict = {
                'req_id' : record.req_id,
                'title' : record.req_title,
                'created_at' : record.created_at,
                'site' : req_sitename,
                'remarks' : record.req_remarks,
                'req_number' : record.req04,
                'items' : record.req_item_list,
                'urgent_requirement' : record.req_urgent_requirement,
                'local_use' : record.req_local_purchase}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/req-status-update', methods=['PATCH'])
@cross_origin()
def req_status_update():
    if request.method == "PATCH":
        print(request.get_json(force=True))
        req_status = request.json['req_status']
        updated_by = request.json['updated_by']
        req_id = request.json['req_id']
        ResultSet=db.session.query(Requisition).filter(Requisition.req_id == req_id).update({'req_status' : req_status, 'updated_by' : updated_by},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)
            

@app.route('/approver1-pending', methods=['GET'])
@cross_origin()
def approver1_pending():
    if request.method == "GET":
        try :
            emprank = ''
            reqq = db.session.query(Requisition).all()
            for rank in reqq:
                emp = db.session.query(Employee).filter(Employee.employee_id == rank.updated_by).all()
                for n in emp:
                    emprank = n.emp19
            ResultSet=db.session.query(Requisition).filter(Requisition.req_status == 'pending', Requisition.updated_by == emprank).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name

                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_number' : record.req04,
                'req_site' : req_sitename}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/approver2-pending', methods=['GET'])
@cross_origin()
def approver2_pending():
    if request.method == "GET":
        try :
            emprank = ''
            reqq = db.session.query(Requisition).all()
            for rank in reqq:
                emp = db.session.query(Employee).filter(Employee.employee_id == rank.updated_by).all()
                for n in emp:
                    if (int(n.emp19) == 1):
                        emprank = n.employee_id
            
            if emprank:
                emprank = '0'
            else:
                emprank = emprank
            ResultSet=db.session.query(Requisition).filter(Requisition.updated_by == emprank, Requisition.req_status == "approved").all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name

                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_number' : record.req04,
                'req_site' : req_sitename}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})
            


@app.route('/approver2-revise', methods=['GET'])
@cross_origin()
def approver2_revise():
    if request.method == "GET":
        try :
            emprank = ''
            reqq = db.session.query(Requisition).all()
            for rank in reqq:
                emp = db.session.query(Employee).filter(Employee.employee_id == rank.updated_by).all()
                for n in emp:
                    if int(n.emp19) == 2:
                        emprank = n.employee_id
            ResultSet=db.session.query(Requisition).filter(Requisition.updated_by == emprank, Requisition.req_status == "revised").all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name

                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_number' : record.req04,
                'req_site' : req_sitename}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/approver2-rejected', methods=['GET'])
@cross_origin()
def approver2_rejected():
    if request.method == "GET":
        try :
            emprank = ''
            reqq = db.session.query(Requisition).all()
            for rank in reqq:
                emp = db.session.query(Employee).filter(Employee.employee_id == rank.updated_by).all()
                for n in emp:
                    if int(n.emp19) == 2:
                        emprank = n.employee_id
            ResultSet=db.session.query(Requisition).filter(Requisition.updated_by == emprank, Requisition.req_status == "rejected").all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name

                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_number' : record.req04,
                'req_site' : req_sitename}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/approver2-approved', methods=['GET'])
@cross_origin()
def approver2_approved():
    if request.method == "GET":
        try :
            emprank = ''
            final_approver = ''
            reqq = db.session.query(Requisition).all()
            for rank in reqq:
                emp = db.session.query(Employee).filter(Employee.employee_id == rank.updated_by).all()
                for n in emp:
                    if int(n.emp19) == 2:
                        if int(n.emp20) == 100:
                            final_approver = n.employee_id
                        emprank = n.employee_id
            ResultSet=db.session.query(Requisition).filter(Requisition.updated_by == emprank, Requisition.req_status == "approved").all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name

                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_number' : record.req04,
                'req_site' : req_sitename}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/requisition-to-rc', methods=['PUT'])
@cross_origin()
def requisition_to_rc():
    if request.method == "PUT":
        print(request.get_json(force=True))
        req_status = 'finalapproved'
        updated_by = request.json['updated_by']
        req_id = request.json['req_id']
        ResultSet=db.session.query(Requisition).filter(Requisition.req_id == req_id).update({'req_status' : req_status, 'updated_by' : updated_by},synchronize_session=False)

        
        ResultSet2=db.session.query(Requisition).filter(Requisition.req_id == req_id).all()
        req_sitename = ""
        for record in ResultSet2:
            email=db.session.query(Site).filter(Site.id==record.req_site).all()
            for n in email:
                req_sitename = n.site_name
            created_at = datetime.datetime.today()
            rate_comparative=RateComparative(rate_comp_requisition_id = record.req_id,
            rate_comp_requisition_title = record.req_title,
            rate_comp_urgent_requirement = record.req_urgent_requirement,
            rate_comp_local_purchase = record.req_local_purchase,
            rate_comp_site_name  = req_sitename,
            rate_comp_request_date  = created_at,
            rate_comp_status = 'created',
            created_by = record.created_by,
            created_at = created_at)
        try:
            db.session.add(rate_comparative)
            db.session.commit()
            print(rate_comparative)
            return {str(rate_comparative) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)




@app.route('/approver22-pending', methods=['GET'])
@cross_origin()
def approver22_pending():
    if request.method == "GET":
        try :
            emprank = ''
            reqq = db.session.query(Requisition).all()
            for rank in reqq:
                emp = db.session.query(Employee).filter(Employee.employee_id == rank.updated_by).all()
                for n in emp:
                    if n.emp19 == '1':
                        emprank = n.employee_id
            
            print(emprank)
            ResultSet=db.session.query(Requisition).filter(Requisition.updated_by == 3).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name

                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_number' : record.req04,
                'req_site' : req_sitename}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


            

@app.route('/req-approvals/<req_id>', methods=['PATCH'])
@cross_origin()
def req_status_approvals(req_id = None, updated_by = None):
    if request.method == "PATCH":

        try:
                print(request.get_json(force=True))
                updated_by = request.json['updated_by']
                ResultSet1 = db.session.query(Employee).filter(Employee.employee_id == updated_by).all()
                for rank in ResultSet1:
                    if rank.emp19 == '1':
                        print(rank.emp19)
                        approval = "pending"
                        print(approval)
                        ResultSet=db.session.query(Requisition).filter(Requisition.req_id == req_id).update({'req_status' : approval, 'updated_by' : updated_by},synchronize_session=False)
                        db.session.commit()
                        return {'Status' : 'Updated'}
                    elif rank.emp19 == '2':
                        print(rank.emp19)
                        approval = "pending"
                        print(approval)
                        ResultSet=db.session.query(Requisition).filter(Requisition.req_id == req_id).update({'req_status' : approval, 'updated_by' : updated_by},synchronize_session=False)
                        db.session.commit()
                        return {'Status' : 'Updated'}
                    elif rank.emp19 == '100':
                        print(rank.emp19)
                        approval = "finalapproved"
                        print(approval)
                        ResultSet=db.session.query(Requisition).filter(Requisition.req_id == req_id).update({'req_status' : approval, 'updated_by' : updated_by},synchronize_session=False)
                        ResultSet2=db.session.query(Requisition).filter(Requisition.req_id == req_id).all()
                        req_sitename = ""
                        for record in ResultSet2:
                            if record.req_local_purchase == True:
                                db.session.commit()
                                return {'status' : 'updated'}
                            else:
                                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                                for n in email:
                                    req_sitename = n.site_name
                                created_at = datetime.datetime.today()
                                rate_comparative=RateComparative(rate_comp_requisition_id = record.req_id,
                                rate_comp_requisition_title = record.req_title,
                                rate_comp_urgent_requirement = record.req_urgent_requirement,
                                rate_comp_local_purchase = record.req_local_purchase,
                                rate_comp_site_name  = req_sitename,
                                rate_comp_request_date  = created_at,
                                ratecomp_1 = record.req04,
                                rate_comp_status = 'create',
                                created_by = record.created_by,
                                created_at = created_at)
                                db.session.add(rate_comparative)
                                db.session.commit()
                                print(rate_comparative)
                                return {str(rate_comparative) : 'Added'}
                    else:
                        pass
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)
            

@app.route('/approver-approves/<empid>', methods=['GET'])
@cross_origin()
def approver_approves(empid = None):
    if request.method == "GET":
        try :
            data = []
            records = 0
            reqq = db.session.query(Requisition).all()
            req_rank = ''
            req_sitename = ""
            for n in reqq:           
                email= db.session.query(Site).filter(Site.id == n.req_site).all()
                for q in email:
                    req_sitename = q.site_name
                employee = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                for e in employee:
                    if req_sitename in e.emp_sites:         
                        empr = db.session.query(Employee).filter(Employee.employee_id == n.updated_by).all()
                        for r in empr:
                            req_rank = r.emp19
                        email= db.session.query(Site).filter(Site.id == n.req_site).all()
                        for q in email:
                            req_sitename = q.site_name
                        empp = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                        for a in empp:
                            if  req_rank == 1:
                                record_dict = {
                                    'req_id' : n.req_id,
                                    'req_title' : n.req_title,
                                    'created_at' : n.created_at,
                                    'req_number' : n.req04,
                                    'req_site' : req_sitename}
                                data.append(record_dict)
                                records += 1
                            """elif  2 <int(a.emp19) < 100:
                                if a.emp19 == req_rank:

                                    if n.req_status == 'pending':
                                        record_dict = {
                                            'req_id' : n.req_id,
                                            'req_title' : n.req_title,
                                            'created_at' : n.created_at,
                                            'req_number' : n.req04,
                                            'req_site' : req_sitename}
                                        data.append(record_dict)
                                records += 1"""
                            if n.req_status == 'finalapproved':
                                record_dict = {
                                    'req_id' : n.req_id,
                                    'req_title' : n.req_title,
                                    'created_at' : n.created_at,
                                    'req_number' : n.req04,
                                    'req_site' : req_sitename}
                                data.append(record_dict)
                                records += 1
            resp = {
                "page": 1,
                "per_page": per_page,
                "total_records": records,
                "total_pages": math.ceil(records/per_page)
            }
            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})



@app.route('/approver-pendings/<empid>', methods=['GET'])
@cross_origin()
def approver_pendings(empid = None):
    if request.method == "GET":
        try :
            data = []
            records = 0
            reqq = db.session.query(Requisition).filter(Requisition.req_status == 'pending').all()
            req_rank = ''
            req_sitename = ""
            ranks = []
            employeer = db.session.query(Employee).all()
            for r in employeer:
                if int(r.emp19) == 0:
                    pass
                else:
                    ranks.append(r.emp19)
            fRank = sorted(ranks)
            print(fRank[0])
            print(fRank[1])
            for n in reqq:
                email= db.session.query(Site).filter(Site.id == n.req_site).all()
                for q in email:
                    req_sitename = q.site_name
                employee = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                for e in employee:
                    if req_sitename in e.emp_sites:
                        empr = db.session.query(Employee).filter(Employee.employee_id == n.updated_by).all()
                        for r in empr:
                            req_rank = r.emp19
                        empp = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                        for a in empp:
                            try:
                                if n.created_by == int(empid):
                                    record_dict = {
                                        'req_id' : n.req_id,
                                        'req_title' : n.req_title,
                                        'created_at' : n.created_at,
                                        'req_number' : n.req04,
                                        'req_site' : req_sitename}
                                    data.append(record_dict)
                                    records += 1
                                elif int(req_rank) == 0:
                                    if int(a.emp19) == 1:
                                        record_dict = {
                                            'req_id' : n.req_id,
                                            'req_title' : n.req_title,
                                            'created_at' : n.created_at,
                                            'req_number' : n.req04,
                                            'req_site' : req_sitename}
                                        data.append(record_dict)
                                        records += 1
                                elif int(req_rank) == 1:
                                    if int(a.emp19) == 100:
                                        record_dict = {
                                            'req_id' : n.req_id,
                                            'req_title' : n.req_title,
                                            'created_at' : n.created_at,
                                            'req_number' : n.req04,
                                            'req_site' : req_sitename}
                                        data.append(record_dict)
                                        records += 1
                                elif int(req_rank) == int(fRank[1]):
                                    if int(a.emp19) == int(fRank[2]):
                                        record_dict = {
                                            'req_id' : n.req_id,
                                            'req_title' : n.req_title,
                                            'created_at' : n.created_at,
                                            'req_number' : n.req04,
                                            'req_site' : req_sitename}
                                        data.append(record_dict)
                                        records += 1
                                elif int(req_rank) == int(fRank[2]):
                                    if int(a.emp19) == int(fRank[3]):
                                        record_dict = {
                                            'req_id' : n.req_id,
                                            'req_title' : n.req_title,
                                            'created_at' : n.created_at,
                                            'req_number' : n.req04,
                                            'req_site' : req_sitename}
                                        data.append(record_dict)
                                        records += 1
                                    else:
                                        pass
                            except:
                                pass
                    else:
                        pass
            resp = {
                "page": 1,
                "per_page": per_page,
                "total_records": records,
                "total_pages": math.ceil(records/per_page)
            }
            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

                        
@app.route('/approver-revise/<empid>', methods=['GET'])
@cross_origin()
def approver_revise(empid = None):
    if request.method == "GET":
        try :
            data = []
            records = 0
            reqq = db.session.query(Requisition).filter(Requisition.req_status == 'revised').all()
            req_rank = ''
            req_sitename = ""
            for n in reqq:
                empr = db.session.query(Employee).filter(Employee.employee_id == n.updated_by).all()
                for r in empr:
                    req_rank = r.emp19
                email= db.session.query(Site).filter(Site.id == n.req_site).all()
                for q in email:
                    req_sitename = q.site_name
                empp = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                for a in empp:
                    if n.created_by == int(empid):
                        record_dict = {
                            'req_id' : n.req_id,
                            'req_title' : n.req_title,
                            'created_at' : n.created_at,
                            'req_number' : n.req04,
                            'req_site' : req_sitename}
                        data.append(record_dict)
                        records += 1
                    elif n.updated_by == int(empid):
                        record_dict = {
                            'req_id' : n.req_id,
                            'req_title' : n.req_title,
                            'created_at' : n.created_at,
                            'req_number' : n.req04,
                            'req_site' : req_sitename}
                        data.append(record_dict)
                        records += 1
            resp = {
                "page": 1,
                "per_page": per_page,
                "total_records": records,
                "total_pages": math.ceil(records/per_page)
            }
            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

                        
@app.route('/approver-rejects/<empid>', methods=['GET'])
@cross_origin()
def approver_rejects(empid = None):
    if request.method == "GET":
        try :
            data = []
            records = 0
            reqq = db.session.query(Requisition).filter(Requisition.req_status == 'rejected').all()
            req_sitename = ""
            for n in reqq:
                email= db.session.query(Site).filter(Site.id == n.req_site).all()
                for q in email:
                    req_sitename = q.site_name
                    if n.created_by == int(empid):
                        record_dict = {
                            'req_id' : n.req_id,
                            'req_title' : n.req_title,
                            'created_at' : n.created_at,
                            'req_number' : n.req04,
                            'req_site' : req_sitename}
                        data.append(record_dict)
                        records += 1
                    elif n.updated_by == int(empid):
                        record_dict = {
                            'req_id' : n.req_id,
                            'req_title' : n.req_title,
                            'created_at' : n.created_at,
                            'req_number' : n.req04,
                            'req_site' : req_sitename}
                        data.append(record_dict)
                        records += 1
                    else:
                        record_dict = {
                            'req_id' : n.req_id,
                            'req_title' : n.req_title,
                            'created_at' : n.created_at,
                            'req_number' : n.req04,
                            'req_site' : req_sitename}
                        data.append(record_dict)
                        records += 1
            resp = {
                "page": 1,
                "per_page": per_page,
                "total_records": records,
                "total_pages": math.ceil(records/per_page)
            }
            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/req-rejects-notification/<empid>', methods=['GET'])
@cross_origin()
def req_rejects_noti(empid = None):
    if request.method == "GET":
        try :
            data = []
            records = 0
            reqq = db.session.query(Requisition).filter(Requisition.req_status == 'rejected').all()
            req_sitename = ""
            for n in reqq:
                if n.created_by == int(empid):
                    records += 1
                elif n.updated_by == int(empid):
                    records += 1
                else:
                    records += 1
            resp = {
                "rejected": records,
            }
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})



@app.route('/req-pendings-notification/<empid>', methods=['GET'])
@cross_origin()
def req_pendings_notification(empid = None):
    if request.method == "GET":
        try :
            data = []
            records = 0
            reqq = db.session.query(Requisition).filter(Requisition.req_status == 'pending').all()
            req_rank = ''
            req_sitename = ""
            ranks = []
            employeer = db.session.query(Employee).all()
            for r in employeer:
                if int(r.emp19) == 0:
                    pass
                else:
                    ranks.append(r.emp19)
            fRank = sorted(ranks)
            print(fRank[0])
            print(fRank[1])
            for n in reqq:
                email= db.session.query(Site).filter(Site.id == n.req_site).all()
                for q in email:
                    req_sitename = q.site_name
                employee = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                for e in employee:
                    if req_sitename in e.emp_sites:
                        empr = db.session.query(Employee).filter(Employee.employee_id == n.updated_by).all()
                        for r in empr:
                            req_rank = r.emp19
                        empp = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                        for a in empp:
                            if n.created_by == int(empid):
                                records += 1
                            elif int(req_rank) == 0:
                                if int(a.emp19) == 1:
                                    records += 1
                            elif int(req_rank) == 1:
                                if int(a.emp19) == 100:
                                    records += 1
            resp = {
                "pending_req": records,
            }
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

                        



@app.route('/view-last-req/<site_id>', methods=['GET'])
@cross_origin()
def view_last_req(site_id = None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Site).all()
            for record in ResultSet:
                if record.id == int(site_id):
                    sites = int(record.si16) + 1
                    record_dict = {
                    'req_id' : sites}
                # else:
                #     record_dict = {
                #     'req_id' : 1}
                #data.append(record_dict)
            return jsonify(record_dict)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

                        


@app.route('/add-history', methods=['POST'])
@cross_origin()
def add_history():
    if request.method == "POST":
        print(request.get_json(force=True))
        history_req_id = request.json['req_id']
        #history_rc_id = request.json['rc_id']
        history_user = request.json['user']
        history_req  = request.json['req_data']
        history_rc = request.json['rc_data']
        history_status = request.json['status']
        created_at = datetime.today()+ timedelta(hours=5.5)

        history=History(
        history_req_id = history_req_id,
        history_user = history_user,
        history_req = history_req,
        history_rc  = history_rc,
        history_status  = history_status,
        created_at = created_at)
        try:
            db.session.add(history)
            db.session.commit()
            print(history)
            return {str(history) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

@app.route('/view-history', methods=['GET'])
@cross_origin()
def view_history():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(History).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            emp_email = ""
            for record in ResultSet:
                employeee = db.session.query(Employee).filter(Employee.employee_id == record.history_user).all()
                for emp in employeee:
                    emp_email = emp.employee_name
                record_dict = {
                'req_id' : int(record.history_req_id),
                'user' : emp_email,
                'req_data' : record.history_req,
                'rc_data' : record.history_rc,
                'history_status' : record.history_status,
                'created_at' : record.created_at}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/view-history-req/<req_id>', methods=['GET'])
@cross_origin()
def view_history_req_by_req_id(req_id = None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(History).filter(History.history_req_id == req_id).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            emp_email = ""
            for record in ResultSet:
                employeee = db.session.query(Employee).filter(Employee.employee_id == record.history_user).all()
                for emp in employeee:
                    emp_email = emp.employee_name
                if record.history_req == None:
                    pass
                else:
                    record_dict = {
                    'req_id' : int(record.history_req_id),
                    'user' : emp_email,
                    'req_data' : record.history_req,
                    'history_status' : record.history_status,
                    'created_at' : record.created_at}
                    data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})



@app.route('/view-history-rc/<req_id>', methods=['GET'])
@cross_origin()
def view_history_rc_by_req_id(req_id = None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(History).filter(History.history_req_id == req_id).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            emp_email = ""
            for record in ResultSet:
                employeee = db.session.query(Employee).filter(Employee.employee_id == record.history_user).all()
                for emp in employeee:
                    emp_email = emp.employee_name
                if record.history_rc == None:
                    pass
                else:
                    record_dict = {
                    'req_id' : int(record.history_req_id),
                    'user' : emp_email,
                    'rc_data' : record.history_rc,
                    'history_status' : record.history_status,
                    'created_at' : record.created_at}
                    data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})



'''
IMPORTANT CODE

data = []
            reqq = db.session.query(Requisition).all()
            req_rank = ''
            req_sitename = ""
            for n in reqq:
                empr = db.session.query(Employee).filter(Employee.employee_id == n.update_by).all()
                for r in empr:
                    req_rank = r.emp19
                email= db.session.query(Site).filter(Site.id == n.req_site).all()
                for q in email:
                    req_sitename = q.site_name
                empp = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                for a in empp:
                    
                    if a.emp19 == '0':
                        if n.req_status == 'revise':
                            if n.created_by = empid:
                                record = {
                                    'req_id' : n.req_id,
                                    'req_title' : n.req_title,
                                    'created_at' : n.created_at,
                                    'req_site' : req_sitename}
                        elif n.req_status == 'pending':
                            record = {
                                'req_id' : n.req_id,
                                'req_title' : n.req_title,
                                'created_at' : n.created_at,
                                'req_site' : req_sitename}

'''



'''




            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            req_sitename = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name

                record_dict = {
                'req_id' : record.req_id,
                'req_title' : record.req_title,
                'created_at' : record.created_at,
                'req_site' : req_sitename}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})




@app.route('/requisition-revised', methods=['GET'])
@cross_origin()
def requisition_revised():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Requisition).filter(Requisition.req_status == 'revised').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            items = []
            categoryname = ""
            subcatname = ""
            req_sitename = ""
            requom = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name
                category_name = db.session.query(Category).filter(Category.category_id == record.req_category).all()
                for name in category_name:
                    categoryname = name.category_name
                sub_category_name = db.session.query(Category).filter(Category.category_id == record.req_sub_category).all()
                for name in sub_category_name:
                    subcatname = name.category_name
                uom_name = db.session.query(UOM).filter(UOM.uom_id == record.req_uom).all()
                for name in uom_name:
                    requom = name.uom_name
                record_dict2 = {
                    'category' : categoryname,
                    'quantity' : record.req_quantity,
                    'intended_end_use' : record.req_intended_end_use,
                    'sub_category' : subcatname,
                    'remarks' : record.remarks,
                    'uom' : requom}
                items.append(record_dict2)
                record_dict = {
                'id' : record.req_id,
                'title' : record.req_title,
                'created_at' : record.created_at,
                'site' : req_sitename,
                'items' : items,
                'urgent_requirement' : record.req_urgent_requirement,
                'local_use' : record.req_local_purchase}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/requisition-pending', methods=['GET'])
@cross_origin()
def requisition_pending():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Requisition).filter(Requisition.req_status == 'pending').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            items = []
            categoryname = ""
            subcatname = ""
            req_sitename = ""
            requom = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name
                category_name = db.session.query(Category).filter(Category.category_id == record.req_category).all()
                for name in category_name:
                    categoryname = name.category_name
                sub_category_name = db.session.query(Category).filter(Category.category_id == record.req_sub_category).all()
                for name in sub_category_name:
                    subcatname = name.category_name
                uom_name = db.session.query(UOM).filter(UOM.uom_id == record.req_uom).all()
                for name in uom_name:
                    requom = name.uom_name
                record_dict2 = {
                    'category' : categoryname,
                    'quantity' : record.req_quantity,
                    'intended_end_use' : record.req_intended_end_use,
                    'sub_category' : subcatname,
                    'remarks' : record.remarks,
                    'uom' : requom}
                items.append(record_dict2)
                record_dict = {
                'id' : record.req_id,
                'title' : record.req_title,
                'created_at' : record.created_at,
                'site' : req_sitename,
                'items' : items,
                'urgent_requirement' : record.req_urgent_requirement,
                'local_use' : record.req_local_purchase}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/requisition-rejected', methods=['GET'])
@cross_origin()
def requisition_rejected():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Requisition).filter(Requisition.req_status == 'rejected').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            items = []
            categoryname = ""
            subcatname = ""
            req_sitename = ""
            requom = ""
            for record in ResultSet:
                email=db.session.query(Site).filter(Site.id==record.req_site).all()
                for n in email:
                    req_sitename = n.site_name
                category_name = db.session.query(Category).filter(Category.category_id == record.req_category).all()
                for name in category_name:
                    categoryname = name.category_name
                sub_category_name = db.session.query(Category).filter(Category.category_id == record.req_sub_category).all()
                for name in sub_category_name:
                    subcatname = name.category_name
                uom_name = db.session.query(UOM).filter(UOM.uom_id == record.req_uom).all()
                for name in uom_name:
                    requom = name.uom_name
                record_dict2 = {
                    'category' : categoryname,
                    'quantity' : record.req_quantity,
                    'intended_end_use' : record.req_intended_end_use,
                    'sub_category' : subcatname,
                    'remarks' : record.remarks,
                    'uom' : requom}
                items.append(record_dict2)
                record_dict = {
                'id' : record.req_id,
                'title' : record.req_title,
                'created_at' : record.created_at,
                'site' : req_sitename,
                'items' : items,
                'urgent_requirement' : record.req_urgent_requirement,
                'local_use' : record.req_local_purchase}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

'''