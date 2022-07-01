from __future__ import division
from flask import request, jsonify, make_response, Blueprint
from flask_cors import CORS, cross_origin
from modules import app ,per_page , db ,ALLOWED_EXTENSIONS ,UPLOAD_FOLDER
from sqlalchemy import create_engine
from sqlalchemy import exc
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

rate_comparative_module = Blueprint('rate_comparative', __name__)
db.create_all()
CORS(app)

@app.route('/add-rate-comparative', methods=['POST'])
@cross_origin()
def add_rate_comparative():
    if request.method == "POST":
        print(request.get_json(force=True))
        requisition_id = request.json['requisition_id']
        rate_comp_requisition_title = request.json['requisition_title']
        rate_comp_urgent_requirement = request.json['urgent_requirement']
        rate_comp_local_purchase = request.json['local_purchase']
        rate_comp_site_name  = request.json['site_name']
        rate_comp_request_date  = request.json['request_date']
        rate_comp_vendors_list = request.json['vendors_list']
        rate_comp_status = request.json['status']
        created_by = request.json['created_by']
        created_at = datetime.datetime.today()

        rate_comp_version = 0
        rate_comparative=RateComparative(rate_comp_requisition_id = requisition_id,
        rate_comp_requisition_title = rate_comp_requisition_title,
        rate_comp_urgent_requirement = rate_comp_urgent_requirement,
        rate_comp_local_purchase = rate_comp_local_purchase,
        rate_comp_site_name  = rate_comp_site_name,
        rate_comp_request_date  = rate_comp_request_date,
        rate_comp_vendors_list = rate_comp_vendors_list,
        rate_comp_status = rate_comp_status,
        rate_comp_version = rate_comp_version,
        created_by = created_by,
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




@app.route('/revise-rate-comparative', methods=['PATCH'])
@cross_origin()
def revise_rate_comparative():
    if request.method == "PATCH":
        print(request.get_json(force=True))
        requisition_id = request.json['requisition_id']
        rate_comp_requisition_title = request.json['requisition_title']
        rate_comp_urgent_requirement = request.json['urgent_requirement']
        rate_comp_local_purchase = request.json['local_purchase']
        rate_comp_site_name  = request.json['site_name']
        rate_comp_request_date  = request.json['request_date']
        rate_comp_vendors_list = request.json['vendors_list']
        rate_comp_status = request.json['status']
        update_by = request.json['created_by']
        update_at = datetime.datetime.today()
        action_by = update_by

        rate_comp_version_increment = 0

        rate_comp_version_number=db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id== requisition_id).all()
        for version_number in rate_comp_version_number:
            print("version-number :",int(version_number.rate_comp_version))
            rate_comp_version_increment  = int(version_number.rate_comp_version) + 1



        rate_comparative=RateComparative(rate_comp_requisition_id = requisition_id,
        rate_comp_requisition_title = rate_comp_requisition_title,
        rate_comp_urgent_requirement = rate_comp_urgent_requirement,
        rate_comp_local_purchase = rate_comp_local_purchase,
        rate_comp_site_name  = rate_comp_site_name,
        rate_comp_request_date  = rate_comp_request_date,
        rate_comp_vendors_list = rate_comp_vendors_list,
        rate_comp_status = rate_comp_status,
        rate_comp_version = rate_comp_version_increment,
        update_by = update_by,
        update_at = update_at,
        action_by = action_by)
        try:
            db.session.add(rate_comparative)
            db.session.commit()
            print(rate_comparative)
            return {str(rate_comparative) : 'updated'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)


@app.route('/cancel-rate-comparative/<actionbyemail>/<reqid>', methods=['DELETE'])
@cross_origin()
def cancel_rate_comparative(actionbyemail=None,reqid=None):
    if request.method == "DELETE":
        

        rate_comp_created_by=db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id== reqid).all()
        for rc_created_by in rate_comp_created_by:
            print("created by :",int(rc_created_by.created_by))
        rc_action_by=db.session.query(Employee).filter(Employee.employee_email == actionbyemail)
        for rc_action_by_name in rc_action_by:
            print("created by :",rc_action_by_name.employee_id)
      
        
        ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id == reqid).update({'rate_comp_status' : 'pending','action_to': rc_created_by.created_by ,'action_by' : rc_action_by_name.employee_id},synchronize_session=False)
    
        try:
            
            db.session.commit()
            print(rate_comparative)
            return {str(rate_comparative) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

@app.route('/reject-rate-comparative/<actionbyemail>/<reqid>', methods=['PATCH'])
@cross_origin()
def reject_rate_comparative(actionbyemail=None,reqid=None):
    if request.method == "PATCH":
        

        rate_comp_created_by=db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id== reqid).all()
        for rc_created_by in rate_comp_created_by:
            print("created by :",int(rc_created_by.created_by))
        rc_action_by=db.session.query(Employee).filter(Employee.employee_email == actionbyemail)
        for rc_action_by_name in rc_action_by:
            print("created by :",rc_action_by_name.employee_id)
      
        
        ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id == reqid).update({'rate_comp_status' : 'pending','action_to': rc_created_by.created_by ,'action_by' : rc_action_by_name.employee_id},synchronize_session=False)
    
        try:
            
            db.session.commit()
            print(rate_comparative)
            return {str(rate_comparative) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)


@app.route('/sanction-rate-comparative/<actionbyemail>/<reqid>', methods=['PATCH'])
@cross_origin()
def sanction_rate_comparative(actionbyemail=None,reqid=None):
    if request.method == "PATCH":
    
        rc_action_by=db.session.query(Employee).filter(Employee.employee_email == actionbyemail)
        for rc_action_by_name in rc_action_by:
            print("action_by :",rc_action_by_name.employee_id)
      
        
        ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id == reqid).update({'rate_comp_status' : 'sanctioned','action_to': 'nextuser','action_by' : rc_action_by_name.employee_id},synchronize_session=False)
    
        try:
            
            db.session.commit()
            print(rate_comparative)
            return {str(rate_comparative) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

@app.route('/rate-comparative-after-vendor-list', methods=['GET'])
@cross_origin()
def rate_comparative_after_vendor_list():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(RateComparative).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            action_by_empname = ""
            actionto_empname = ""
            vendor_name = []
            vendors = db.session.query(Vendor).all()
            for name in vendors:
                vendor_name.append(name.vendor_name)
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    action_by_empname = action_by_name.employee_name
                    print(action_by_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name

                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : record.rate_comp_site_name,
                'rate_comp_request_date'  : record.rate_comp_request_date,
                'rate_comp_vendors_list' : record.rate_comp_vendors_list,
                'rate_comp_req_number' : record.ratecomp_1,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : action_by_empname,
                'vendors_name' : vendor_name,
                'action_to' : actionto_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/rate-comparative-after-vendor-list/<req_id>', methods=['GET'])
@cross_origin()
def rate_comparative_after_vendor_list_by_id(req_id = None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id == req_id).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            action_by_empname = ""
            actionto_empname = ""
            vendor_name = []
            vendors = db.session.query(Vendor).all()
            for name in vendors:
                vendor_name.append(name.vendor_name)
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    action_by_empname = action_by_name.employee_name
                    print(action_by_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name

                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : record.rate_comp_site_name,
                'rate_comp_request_date'  : record.rate_comp_request_date,
                'rate_comp_vendors_list' : record.rate_comp_vendors_list,
                'rate_comp_req_number' : record.ratecomp_1,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : action_by_empname,
                'vendors_name' : vendor_name,
                'action_to' : actionto_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/rc-vendor-update/<req_id>', methods=['PATCH'])
@cross_origin()
def rc_vendor_update(req_id = None):
    if request.method == "PATCH":
        print(request.get_json(force=True))
        rate_comp_vendors_list = request.json['rate_comp_vendors_list']
        update_by = request.json['updated_by']
        rate_comp_status = request.json['rate_comp_status']
        ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id == req_id).update({'rate_comp_vendors_list' : rate_comp_vendors_list, 'update_by' : update_by, 'created_by' : update_by, 'rate_comp_status' : rate_comp_status},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)



@app.route('/rc-create/<empid>', methods=['GET'])
@cross_origin()
def rc_create_by_empid(empid = None):
    if request.method == "GET":
        try :
            data = []
            records = 0
            reqq = db.session.query(RateComparative).filter(RateComparative.rate_comp_status == 'create').all()
            reqq1 = db.session.query(RateComparative).filter(RateComparative.rate_comp_status == 'draft').all()
            for record in reqq:
                empp = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                for a in empp:
                    if a.emp20 == '0':
                        record_dict = {
                            'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                            'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                            'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                            'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                            'rate_comp_site_name'  : record.rate_comp_site_name,
                            'rate_comp_request_date'  : record.rate_comp_request_date,
                            'rate_comp_vendors_list' : record.rate_comp_vendors_list,
                            'rate_comp_req_number' : record.ratecomp_1,
                            'rate_comp_status' : record.rate_comp_status}
                        data.append(record_dict)
                        records += 1
            for record in reqq1:
                empp = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                for a in empp:
                    if a.emp20 == '0':
                        record_dict = {
                            'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                            'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                            'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                            'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                            'rate_comp_site_name'  : record.rate_comp_site_name,
                            'rate_comp_request_date'  : record.rate_comp_request_date,
                            'rate_comp_vendors_list' : record.rate_comp_vendors_list,
                            'rate_comp_req_number' : record.ratecomp_1,
                            'rate_comp_status' : record.rate_comp_status}
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

            

@app.route('/rc-approves/<empid>', methods=['GET'])
@cross_origin()
def rc_approves(empid = None):
    if request.method == "GET":
        try :
            data = []
            records = 0
            reqq = db.session.query(RateComparative).all()
            rc_rank = ''
            for n in reqq:                    
                empr = db.session.query(Employee).filter(Employee.employee_id == n.update_by).all()
                for r in empr:
                    rc_rank = r.emp20
                empp = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                for a in empp:
                    if rc_rank == 1:
                        record_dict = {
                                'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                                'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                                'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                                'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                                'rate_comp_site_name'  : n.rate_comp_site_name,
                                'rate_comp_request_date'  : n.rate_comp_request_date,
                                'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                                'rate_comp_req_number' : n.ratecomp_1,
                                'rate_comp_status' : n.rate_comp_status}
                        data.append(record_dict)
                        records += 1
                        """if n.rate_comp_status == 'sanctioned':
                            record_dict = {
                                'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                                'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                                'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                                'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                                'rate_comp_site_name'  : n.rate_comp_site_name,
                                'rate_comp_request_date'  : n.rate_comp_request_date,
                                'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                                'rate_comp_req_number' : n.ratecomp_1,
                                'rate_comp_status' : n.rate_comp_status}
                            data.append(record_dict)
                    elif  a.emp20 < rc_rank:
                        record_dict = {
                            'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                            'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                            'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                            'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                            'rate_comp_site_name'  : n.rate_comp_site_name,
                            'rate_comp_request_date'  : n.rate_comp_request_date,
                            'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                            'rate_comp_req_number' : n.ratecomp_1,
                            'rate_comp_status' : n.rate_comp_status}
                        data.append(record_dict)
                        records += 1
                    if  int(a.emp20) < 100:
                        if a.emp20 == rc_rank:

                            if n.rate_comp_status == 'pending':
                                record_dict = {
                                    'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                                    'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                                    'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                                    'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                                    'rate_comp_site_name'  : n.rate_comp_site_name,
                                    'rate_comp_request_date'  : n.rate_comp_request_date,
                                    'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                                    'rate_comp_req_number' : n.ratecomp_1,
                                    'rate_comp_status' : n.rate_comp_status}
                                data.append(record_dict)
                        records += 1"""
                    elif n.rate_comp_status == 'sanctioned':
                        record_dict = {
                            'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                            'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                            'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                            'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                            'rate_comp_site_name'  : n.rate_comp_site_name,
                            'rate_comp_request_date'  : n.rate_comp_request_date,
                            'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                            'rate_comp_req_number' : n.ratecomp_1,
                            'rate_comp_status' : n.rate_comp_status}
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





@app.route('/rc-pendings/<empid>', methods=['GET'])
@cross_origin()
def rc_pendings(empid = None):
    if request.method == "GET":
        try :
            data = []
            records = 0
            reqq = db.session.query(RateComparative).filter(RateComparative.rate_comp_status == 'pending').all()
            rc_rank = ''
            req_sitename = ""
            ranks = []
            employeer = db.session.query(Employee).all()
            for r in employeer:
                if int(r.emp20) == 0:
                    pass
                else:
                    ranks.append(r.emp20)
            # fRank = sorted(ranks)
            # print(fRank[0])
            # print(fRank[1])
            for n in reqq:
                email= db.session.query(Site).filter(Site.site_name == n.rate_comp_site_name).all()
                for q in email:
                    req_sitename = q.site_name
                employee = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                for e in employee:
                    if req_sitename in e.emp_sites:
                        empr = db.session.query(Employee).filter(Employee.employee_id == n.update_by).all()
                        for r in empr:
                            rc_rank = r.emp20
                        empp = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                        for a in empp:
                                if n.created_by == int(empid):
                                    record_dict = {
                                        'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                                        'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                                        'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                                        'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                                        'rate_comp_site_name'  : n.rate_comp_site_name,
                                        'rate_comp_request_date'  : n.rate_comp_request_date,
                                        'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                                        'rate_comp_req_number' : n.ratecomp_1,
                                        'rate_comp_status' : n.rate_comp_status}
                                    data.append(record_dict)
                                    records += 1
                                elif int(rc_rank) == 0:
                                        if int(a.emp20) == 1:
                                            record_dict = {
                                            'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                                            'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                                            'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                                            'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                                            'rate_comp_site_name'  : n.rate_comp_site_name,
                                            'rate_comp_request_date'  : n.rate_comp_request_date,
                                            'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                                            'rate_comp_req_number' : n.ratecomp_1,
                                            'rate_comp_status' : n.rate_comp_status}
                                            data.append(record_dict)
                                            records += 1
                                elif int(rc_rank) == 1:
                                        if int(a.emp20) == 100:
                                            record_dict = {
                                            'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                                            'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                                            'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                                            'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                                            'rate_comp_site_name'  : n.rate_comp_site_name,
                                            'rate_comp_request_date'  : n.rate_comp_request_date,
                                            'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                                            'rate_comp_req_number' : n.ratecomp_1,
                                            'rate_comp_status' : n.rate_comp_status}
                                            data.append(record_dict)
                                            records += 1
                                elif int(rc_rank) == int(fRank[1]):
                                        if int(a.emp20) == int(fRank[2]):
                                            record_dict = {
                                            'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                                            'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                                            'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                                            'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                                            'rate_comp_site_name'  : n.rate_comp_site_name,
                                            'rate_comp_request_date'  : n.rate_comp_request_date,
                                            'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                                            'rate_comp_req_number' : n.ratecomp_1,
                                            'rate_comp_status' : n.rate_comp_status}
                                            data.append(record_dict)
                                            records += 1
                                elif int(rc_rank) == int(fRank[2]):
                                        if int(a.emp20) == int(fRank[3]):
                                            record_dict = {
                                            'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                                            'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                                            'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                                            'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                                            'rate_comp_site_name'  : n.rate_comp_site_name,
                                            'rate_comp_request_date'  : n.rate_comp_request_date,
                                            'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                                            'rate_comp_req_number' : n.ratecomp_1,
                                            'rate_comp_status' : n.rate_comp_status}
                                            data.append(record_dict)
                                            records += 1
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





@app.route('/rc-pendings-notification/<empid>', methods=['GET'])
@cross_origin()
def rc_pendings_notification(empid = None):
    if request.method == "GET":
        try :
            data = []
            records = 0
            reqq = db.session.query(RateComparative).filter(RateComparative.rate_comp_status == 'pending').all()
            rc_rank = ''
            req_sitename = ""
            ranks = []
            employeer = db.session.query(Employee).all()
            for r in employeer:
                if int(r.emp20) == 0:
                    pass
                else:
                    ranks.append(r.emp20)
            fRank = sorted(ranks)
            print(fRank[0])
            print(fRank[1])
            for n in reqq:
                email= db.session.query(Site).filter(Site.site_name == n.rate_comp_site_name).all()
                for q in email:
                    req_sitename = q.site_name
                employee = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                for e in employee:
                    if req_sitename in e.emp_sites:
                        empr = db.session.query(Employee).filter(Employee.employee_id == n.update_by).all()
                        for r in empr:
                            rc_rank = r.emp20
                        empp = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                        for a in empp:
                            if n.created_by == int(empid):
                                records += 1
                            elif int(rc_rank) == 0:
                                if int(a.emp20) == 1:
                                    records += 1
                            elif int(rc_rank) == 1:
                                if int (a.emp20) == 100:
                                    records += 1
            resp = {
                "pending_rc": records,
            }
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})




@app.route('/rate-comparative-approved', methods=['GET'])
@cross_origin()
def rate_comparative_aproved():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_status=='sanctioned').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            actionby_empname = ""
            actionto_empname = ""
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    actionby_empname = action_by_name.employee_name
                    print(actionby_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name

                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : record.rate_comp_site_name,
                'rate_comp_request_date'  : record.rate_comp_request_date,
                'rate_comp_vendors_list' : record.rate_comp_vendors_list,
                'rate_comp_req_number' : record.ratecomp_1,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : actionby_empname,
                'action_to' : actionto_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})



@app.route('/rate-comparative-pendings', methods=['GET'])
@cross_origin()
def rate_comparative_all_pending():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_status=='pending').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            actionby_empname = ""
            actionto_empname = ""
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    actionby_empname = action_by_name.employee_name
                    print(actionby_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name

                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : record.rate_comp_site_name,
                'rate_comp_request_date'  : record.rate_comp_request_date,
                'rate_comp_req_number' : record.ratecomp_1,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})



@app.route('/rc-revise/<empid>', methods=['GET'])
@cross_origin()
def rc_revise(empid = None):
    if request.method == "GET":
        try :
            data = []
            records = 0
            reqq = db.session.query(RateComparative).filter(RateComparative.rate_comp_status == 'revised').all()
            req_rank = ''
            for n in reqq:
                empr = db.session.query(Employee).filter(Employee.employee_id == n.update_by).all()
                for r in empr:
                    req_rank = r.emp19
                empp = db.session.query(Employee).filter(Employee.employee_id == empid).all()
                for a in empp:
                    if n.created_by == int(empid):
                        record_dict = {
                            'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                            'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                            'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                            'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                            'rate_comp_site_name'  : n.rate_comp_site_name,
                            'rate_comp_request_date'  : n.rate_comp_request_date,
                            'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                            'rate_comp_req_number' : n.ratecomp_1,
                            'rate_comp_status' : n.rate_comp_status}
                        data.append(record_dict)
                        records += 1
                    elif n.update_by == int(empid):
                        record_dict = {
                            'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                            'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                            'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                            'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                            'rate_comp_site_name'  : n.rate_comp_site_name,
                            'rate_comp_request_date'  : n.rate_comp_request_date,
                            'rate_comp_req_number' : n.ratecomp_1,
                            'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                            'rate_comp_status' : n.rate_comp_status}
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


                        
@app.route('/rc-rejects/<empid>', methods=['GET'])
@cross_origin()
def rc_rejects(empid = None):
    if request.method == "GET":
        try :
            data = []
            records = 0
            reqq = db.session.query(RateComparative).filter(RateComparative.rate_comp_status == 'rejected').all()
            req_sitename = ""
            for n in reqq:
                if n.created_by == int(empid):
                    record_dict = {
                            'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                            'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                            'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                            'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                            'rate_comp_site_name'  : n.rate_comp_site_name,
                            'rate_comp_request_date'  : n.rate_comp_request_date,
                            'rate_comp_req_number' : n.ratecomp_1,
                            'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                            'rate_comp_status' : n.rate_comp_status}
                    data.append(record_dict)
                    records += 1
                elif n.update_by == int(empid):
                    record_dict = {
                            'rate_comp_requisition_id' : n.rate_comp_requisition_id,
                            'rate_comp_requisition_title' : n.rate_comp_requisition_title,
                            'rate_comp_urgent_requirement' : n.rate_comp_urgent_requirement,
                            'rate_comp_req_number' : n.ratecomp_1,
                            'rate_comp_local_purchase' : n.rate_comp_local_purchase,
                            'rate_comp_site_name'  : n.rate_comp_site_name,
                            'rate_comp_request_date'  : n.rate_comp_request_date,
                            'rate_comp_vendors_list' : n.rate_comp_vendors_list,
                            'rate_comp_status' : n.rate_comp_status}
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



@app.route('/rc-approvals/<req_id>', methods=['PATCH'])
@cross_origin()
def rc_status_approvals(req_id = None, updated_by = None):
    if request.method == "PATCH":

        try:
                print(request.get_json(force=True))
                update_by = request.json['update_by']
                updated_at = datetime.datetime.today()
                rate_comp_vendors_list = request.json['rate_comp_vendors_list']

                ResultSet1 = db.session.query(Employee).filter(Employee.employee_id == update_by).all()
                for rank in ResultSet1:
                    if rank.emp20 == '1':
                        print(rank.emp20)
                        approval = "pending"
                        print(approval)
                        ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id == req_id).update({'rate_comp_status' : approval, 'update_by' : update_by, 'rate_comp_vendors_list' : rate_comp_vendors_list},synchronize_session=False)
                        db.session.commit()
                        return {'Status' : 'Updated'}
                    elif rank.emp20 == '2':
                        print(rank.emp20)
                        approval = "pending"
                        print(approval)
                        ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id == req_id).update({'rate_comp_status' : approval, 'update_by' : update_by, 'rate_comp_vendors_list' : rate_comp_vendors_list},synchronize_session=False)
                        db.session.commit()
                        return {'Status' : 'Updated'}
                    elif rank.emp20 == '100':
                        print(rank.emp20)
                        approval = "sanctioned"
                        print(approval)
                        ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id == req_id).update({'rate_comp_status' : approval, 'update_by' : update_by, 'rate_comp_vendors_list' : rate_comp_vendors_list, 'update_at' : updated_at},synchronize_session=False)
                        db.session.commit()
                        return {'Status' : 'Updated'}
                    else:
                        pass
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)



@app.route('/rc-status-update/<req_id>', methods=['PATCH'])
@cross_origin()
def rc_status_update(req_id = None):
    if request.method == "PATCH":
        print(request.get_json(force=True))
        rate_comp_status = request.json['rate_comp_status']
        update_by = request.json['update_by']
        rate_comp_vendors_list = request.json['rate_comp_vendors_list']
        ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id == req_id).update({'rate_comp_status' : rate_comp_status, 'update_by' : update_by, 'rate_comp_vendors_list' : rate_comp_vendors_list},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

                        


@app.route('/rate-comparative-revise', methods=['GET'])
@cross_origin()
def rate_comparative_revised():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_status=='revised').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            actionby_empname = ""
            actionto_empname = ""
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    actionby_empname = action_by_name.employee_name
                    print(actionby_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name

                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : record.rate_comp_site_name,
                'rate_comp_request_date'  : record.rate_comp_request_date,
                'rate_comp_vendors_list' : record.rate_comp_vendors_list,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : actionby_empname,
                'action_to' : actionto_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/rate-comparative-pending', methods=['GET'])
@cross_origin()
def rate_comparative_pending():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_status=='pending').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            actionby_empname = ""
            actionto_empname = ""
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    actionby_empname = action_by_name.employee_name
                    print(actionby_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name

                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : record.rate_comp_site_name,
                'rate_comp_request_date'  : record.rate_comp_request_date,
                'rate_comp_vendors_list' : record.rate_comp_vendors_list,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : actionby_empname,
                'action_to' : actionto_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/rate-comparative-reject', methods=['GET'])
@cross_origin()
def rate_comparative_reject():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_status=='rejected').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            actionby_empname = ""
            actionto_empname = ""
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    actionby_empname = action_by_name.employee_name
                    print(actionby_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name

                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : record.rate_comp_site_name,
                'rate_comp_request_date'  : record.rate_comp_request_date,
                'rate_comp_vendors_list' : record.rate_comp_vendors_list,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : actionby_empname,
                'action_to' : actionto_empname}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/sanctioner2-rc-pending', methods=['GET'])
@cross_origin()
def sanctioner2_rc_pending():
    if request.method == "GET":
        try :
            empsanction = ''
            reqq = db.session.query(RateComparative).all()
            for rank in reqq:
                emp = db.session.query(Employee).filter(Employee.employee_id == rank.update_by).all()
                for n in emp:
                    if int(n.emp20) == 1:
                        empsanction = n.employee_id
            ResultSet=db.session.query(RateComparative).filter(RateComparative.update_by == empsanction ,RateComparative.rate_comp_status=='sanctioned').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            actionby_empname = ""
            actionto_empname = ""
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    actionby_empname = action_by_name.employee_name
                    print(actionby_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name

                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : record.rate_comp_site_name,
                'rate_comp_request_date'  : record.rate_comp_request_date,
                'rate_comp_vendors_list' : record.rate_comp_vendors_list,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : actionby_empname,
                'action_to' : actionto_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})




@app.route('/sanctioner2-rc-revise', methods=['GET'])
@cross_origin()
def sanctioner2_rc_revise():
    if request.method == "GET":
        try :
            empsanction = ''
            reqq = db.session.query(RateComparative).all()
            for rank in reqq:
                emp = db.session.query(Employee).filter(Employee.employee_id == rank.update_by).all()
                for n in emp:
                    if int(n.emp20) == 2:
                        empsanction = n.employee_id
            ResultSet=db.session.query(RateComparative).filter(RateComparative.update_by == empsanction ,RateComparative.rate_comp_status=='revised').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            actionby_empname = ""
            actionto_empname = ""
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    actionby_empname = action_by_name.employee_name
                    print(actionby_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name

                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : record.rate_comp_site_name,
                'rate_comp_request_date'  : record.rate_comp_request_date,
                'rate_comp_vendors_list' : record.rate_comp_vendors_list,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : actionby_empname,
                'action_to' : actionto_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/sanctioner2-rc-rejected', methods=['GET'])
@cross_origin()
def sanctioner2_rc_rejected():
    if request.method == "GET":
        try :
            empsanction = ''
            reqq = db.session.query(RateComparative).all()
            for rank in reqq:
                emp = db.session.query(Employee).filter(Employee.employee_id == rank.update_by).all()
                for n in emp:
                    if int(n.emp20) == 2:
                        empsanction = n.employee_id
            ResultSet=db.session.query(RateComparative).filter(RateComparative.update_by == empsanction ,RateComparative.rate_comp_status=='rejected').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            actionby_empname = ""
            actionto_empname = ""
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    actionby_empname = action_by_name.employee_name
                    print(actionby_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name

                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : record.rate_comp_site_name,
                'rate_comp_request_date'  : record.rate_comp_request_date,
                'rate_comp_vendors_list' : record.rate_comp_vendors_list,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : actionby_empname,
                'action_to' : actionto_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})



@app.route('/sanctioner2-rc-approved', methods=['GET'])
@cross_origin()
def sanctioner2_rc_approved():
    if request.method == "GET":
        try :
            empsanction = ''
            reqq = db.session.query(RateComparative).all()
            for rank in reqq:
                emp = db.session.query(Employee).filter(Employee.employee_id == rank.update_by).all()
                for n in emp:
                    if int(n.emp20) == 2:
                        empsanction = n.employee_id
            ResultSet=db.session.query(RateComparative).filter(RateComparative.update_by == empsanction ,RateComparative.rate_comp_status=='sanctioned').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            actionby_empname = ""
            actionto_empname = ""
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    actionby_empname = action_by_name.employee_name
                    print(actionby_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name

                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : record.rate_comp_site_name,
                'rate_comp_request_date'  : record.rate_comp_request_date,
                'rate_comp_vendors_list' : record.rate_comp_vendors_list,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : actionby_empname,
                'action_to' : actionto_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/rc-post-in-po/<req_id>', methods=['PUT'])
@cross_origin()
def rc_approvals(req_id = None):
    if request.method == "PUT":

        print(request.get_json(force=True))
        update_by = request.json['update_by']
        vendor_json = request.json['vendor_json']
        ResultSet = db.session.query(RateComparative).filter(RateComparative.rate_comp_requisition_id == req_id).all()
        for record in ResultSet:
            site_id = ''
            site = db.session.query(Site).filter(Site.site_name == record.rate_comp_site_name).all()
            for s in site:
                site_id = s.id
            vendor_id = ''
            payment_terms = ''
            terms_and_conditions = ''
            pon = 0
            #f = open('main.json')
            j = vendor_json
            print(record.rate_comp_vendors_list)
            print("____________________________________________________________")
            with open('RC.json', 'w') as json_file:
                json.dump(j, json_file)
            print("first")
            f = open('RC.json')
            rate_comp_vendors_list = json.load(f)
            for x in range(len(rate_comp_vendors_list)):
                
                vendor_id = ""

                sanctioned_json = rate_comp_vendors_list[x]
                print('after breaking')
                asd = sanctioned_json['items']
                # for y in range(len(asd)):
                #     new = asd[y]
                #     summ = new['Quantity']
                #     try:
                #         if new['isChecked'] == True:
                rc_vendor = sanctioned_json['vendor_name']
                vendor = db.session.query(Vendor).filter(Vendor.vendor_name == rc_vendor).all()
                for n in vendor:
                    vendor_id = n.vendor_id
                    payment_terms = n.vendor_payment_terms
                    terms_and_conditions = n.vendor_terms_and_conditions
                purchaseOrder = PO(po_vendor_json = sanctioned_json, po_org = None, po_site = site_id, po_status = 'pending', po_vendor = vendor_id, po7 = payment_terms, po6 = terms_and_conditions, po_vendor_name = record.ratecomp_1)
                db.session.add(purchaseOrder)
                db.session.commit()
                    # except:
                    #     pass
            f.close()
            os.remove('RC.json')
            try:
                return {'Status' : 'Updated'}
                
            except exc.SQLAlchemyError as e  :
                print(e)
                db.session.rollback()
                return str(e)


            

@app.route('/view-mrc', methods=['GET'])
@cross_origin()
def view_mrc():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_status == 'sanctioned').all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            action_by_empname = ""
            actionto_empname = ""
            vendor_name = []
            vendors = db.session.query(Vendor).all()
            for name in vendors:
                vendor_name.append(name.vendor_name)
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    action_by_empname = action_by_name.employee_name
                    print(action_by_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name
                vendor_id = ''
                j = record.rate_comp_vendors_list
                with open('RC.json', 'w') as json_file:
                    json.dump(j, json_file)
                f = open('RC.json')
                rate_comp_vendors_list = json.load(f)
                for x in range(len(rate_comp_vendors_list)):
                    
                    vendor_id = ""

                    sanctioned_json = rate_comp_vendors_list[x]
                    shipping_cost = int(sanctioned_json['Shipping_cost'])
                    asd = sanctioned_json['items']
                    request_date = record.rate_comp_request_date
                    updated_at = record.update_at
                    site_name = record.rate_comp_site_name
                    total = 0                                      
                    for y in range(len(asd)):
                        new = asd[y]
                        summ = new['Quantity']
                        try:
                            if new['isAvailable'] == True:
                                total =  total + summ
                                shipping_gst_cost = sanctioned_json['shipping_cost_gst']
                                sumShippingCost = shipping_cost + shipping_gst_cost
                        except:
                            pass
                    for y in range(len(asd)):
                        new = asd[y]
                        summ = new['Quantity']
                        try:
                            if new['isAvailable'] == True:

                                algo = summ *sumShippingCost/total
                                round_off = round(algo, 2)
                                item_gst = int(new['item_gst'])
                                t_amount = int(new['total_amount'])
                                new['item_shipping_cost_with_gst'] = round_off
                                new['requisition_id'] = record.ratecomp_1
                                new['Site_name'] = site_name
                                new['rate_comp_request_date'] = request_date
                                new['sanctioned_date'] = updated_at
                                new['total_amount_with_gst'] = (t_amount * (item_gst/100)) + t_amount
                        except:
                            pass
                f.close()
                os.remove('RC.json')
                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'requisition_id' : record.ratecomp_1,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : site_name,
                'rate_comp_request_date'  : request_date,
                'rate_comp_vendors_list' : rate_comp_vendors_list,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : action_by_empname,
                'vendors_name' : vendor_name,
                'last_updated' : record.update_at,
                'action_to' : actionto_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

            

@app.route('/view-mrc/<req_id>', methods=['GET'])
@cross_origin()
def view_mrc_by_req_id(req_id = None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(RateComparative).filter(RateComparative.rate_comp_status == 'sanctioned', RateComparative.rate_comp_requisition_id == req_id).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            action_by_empname = ""
            actionto_empname = ""
            vendor_name = []
            vendors = db.session.query(Vendor).all()
            for name in vendors:
                vendor_name.append(name.vendor_name)
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    action_by_empname = action_by_name.employee_name
                    print(action_by_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name
                vendor_id = ''
                j = record.rate_comp_vendors_list
                #print(record.rate_comp_vendors_list)
                print("____________________________________________________________")
                with open('RC.json', 'w') as json_file:
                    json.dump(j, json_file)
                print("first")
                f = open('RC.json')
                rate_comp_vendors_list = json.load(f)
                for x in range(len(rate_comp_vendors_list)):
                    
                    vendor_id = ""

                    sanctioned_json = rate_comp_vendors_list[x]
                    shipping_cost = int(sanctioned_json['Shipping_cost'])
                    asd = sanctioned_json['items']
                    #gst_amount = sanctioned_json['GST_amount']
                    #shipping_gst = int(sanctioned_json['shipping_cost_gst'])
                    request_date = record.rate_comp_request_date
                    updated_at = record.update_at
                    site_name = record.rate_comp_site_name
                    total = 0                                      
                    for y in range(len(asd)):
                        new = asd[y]
                        summ = new['Quantity']
                        try:
                            if new['isAvailable'] == True:
                                total =  total + summ
                                shipping_gst_cost = sanctioned_json['shipping_cost_gst']
                                sumShippingCost = shipping_cost + shipping_gst_cost
                        except:
                            pass
                    for y in range(len(asd)):
                        new = asd[y]
                        summ = new['Quantity']
                        try:
                            if new['isAvailable'] == True:

                                algo = summ *sumShippingCost/total
                                round_off = round(algo, 2)
                                item_gst = int(new['item_gst'])
                                t_amount = int(new['total_amount'])
                                new['item_shipping_cost_with_gst'] = round_off
                                new['Site_name'] = site_name
                                new['rate_comp_request_date'] = request_date
                                new['sanctioned_date'] = updated_at
                                new['total_amount_with_gst'] = (t_amount * (item_gst/100)) + t_amount
                        except:
                            pass
                f.close()
                os.remove('RC.json')
                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : site_name,
                'rate_comp_request_date'  : request_date,
                'rate_comp_vendors_list' : rate_comp_vendors_list,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : action_by_empname,
                'vendors_name' : vendor_name,
                'last_updated' : record.update_at,
                'action_to' : actionto_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/view-mrc-all', methods=['GET'])
@cross_origin()
def view_mrc_all():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(RateComparative).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            action_by_empname = ""
            actionto_empname = ""
            vendor_name = []
            vendors = db.session.query(Vendor).all()
            for name in vendors:
                vendor_name.append(name.vendor_name)
            for record in ResultSet:
                emp_name=db.session.query(Employee).filter(Employee.employee_id==record.created_by).all()
                for name in emp_name:
                    createby_empname = name.employee_name
                action_by_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_by).all()
                for action_by_name in action_by_emp_name:
                    action_by_empname = action_by_name.employee_name
                    print(action_by_empname)
                action_to_emp_name=db.session.query(Employee).filter(Employee.employee_id==record.action_to).all()
                for action_to_name in action_to_emp_name:
                    actionto_empname = action_to_name.employee_name
                vendor_id = ''
                j = record.rate_comp_vendors_list
                with open('RC.json', 'w') as json_file:
                    json.dump(j, json_file)
                f = open('RC.json')
                rate_comp_vendors_list = json.load(f)
                # print(rate_comp_vendors_list)
                if rate_comp_vendors_list != None:
                    for x in range(len(rate_comp_vendors_list)):
                        
                        vendor_id = ""

                        sanctioned_json = rate_comp_vendors_list[x]
                        shipping_cost = int(sanctioned_json['Shipping_cost'])
                        asd = sanctioned_json['items']
                        request_date = record.rate_comp_request_date
                        updated_at = record.update_at
                        site_name = record.rate_comp_site_name
                        total = 0                                      
                        for y in range(len(asd)):
                            new = asd[y]
                            summ = new['Quantity']
                            try:
                                if new['isAvailable'] == True:
                                    total =  total + summ
                                    shipping_gst_cost = sanctioned_json['shipping_cost_gst']
                                    sumShippingCost = shipping_cost + shipping_gst_cost
                            except:
                                pass
                        for y in range(len(asd)):
                            new = asd[y]
                            summ = new['Quantity']
                            try:
                                if new['isAvailable'] == True:

                                    algo = summ *sumShippingCost/total
                                    round_off = round(algo, 2)
                                    item_gst = int(new['item_gst'])
                                    t_amount = int(new['total_amount'])
                                    new['item_shipping_cost_with_gst'] = round_off
                                    new['requisition_id'] = record.ratecomp_1
                                    new['Site_name'] = site_name
                                    new['rate_comp_request_date'] = request_date
                                    new['sanctioned_date'] = updated_at
                                    new['total_amount_with_gst'] = (t_amount * (item_gst/100)) + t_amount
                            except:
                                pass
                else:
                    site_name = None
                    request_date = None
                f.close()
                os.remove('RC.json')
                record_dict = {
                'rate_comp_requisition_id' : record.rate_comp_requisition_id,
                'requisition_id' : record.ratecomp_1,
                'rate_comp_requisition_title' : record.rate_comp_requisition_title,
                'rate_comp_urgent_requirement' : record.rate_comp_urgent_requirement,
                'rate_comp_local_purchase' : record.rate_comp_local_purchase,
                'rate_comp_site_name'  : site_name,
                'rate_comp_request_date'  : request_date,
                'rate_comp_vendors_list' : rate_comp_vendors_list,
                'rate_comp_status' : record.rate_comp_status,
                'created_by' : createby_empname,
                'action_by' : action_by_empname,
                'vendors_name' : vendor_name,
                'last_updated' : record.update_at,
                'action_to' : actionto_empname}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})