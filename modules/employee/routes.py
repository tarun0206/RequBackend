from __future__ import division
from flask import request, jsonify, make_response, Blueprint
from flask_cors import CORS, cross_origin
from modules import app ,per_page , db
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from modules.models import Client,Site,Employee,Org
import datetime
import json
import pandas
import math
import logging
import boto3
from botocore.exceptions import ClientError

employee_module = Blueprint('employee', __name__)
db.create_all()
CORS(app)

@app.route('/add-employee-permission', methods=['POST'])
@cross_origin()
def employee_insert():
    if request.method == "POST":
        print(request.get_json(force=True))
        #employee_name = request.json['employee_name']
        employee_email = request.json['employee_email']
        employee_designation = "productmanager"
        employee_contact = request.json['employee_contact']
        #created_by = request.json['created_by']
        created_at = datetime.datetime.today()
        user_permission = request.json['user_permission']
        site_name = request.json['site_name']
        created_by = request.json['site_name']
        update_at = datetime.datetime.today()

        employee=Employee(  employee_email = employee_email, created_at = created_at, created_by = created_by,
        user_permission = user_permission, emp_sites = '[]'
        )
        
        try:
            db.session.add(employee)
            db.session.commit()
            print(employee)
            employee_ResultSet=db.session.query(Employee.employee_id).filter(Employee.employee_email == employee_email)
            print("i am here")
            for x in employee_ResultSet:
                print(x.employee_id)
                site_ResultSet=db.session.query(Site).filter(Site.site_name == site_name)
                for record in site_ResultSet:
                    print(record.id)
                    ResultSet=db.session.query(Site).filter(Site.id == record.id).update({ 'project_manager_id' : x.employee_id, 
                    'update_at' : update_at},synchronize_session=False)
            db.session.commit()
            return jsonify({str(employee) : 'Inserted'}) 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return jsonify({'error':str(e)})



@app.route('/employee/update-permisiions', methods=['PATCH'])
@cross_origin()
def update_employee_permisiions():
    if request.method == "PATCH":
        print(request.get_json(force=True))
        #employee_name = request.json['employee_name']
        employee_email = request.json['employee_email']
        employee_designation = "productmanager"
        #employee_contact = request.json['employee_contact']
        #created_by = request.json['created_by']
        #created_at = datetime.datetime.today()
        user_permission = request.json['user_permission']
        site_name = request.json['site_name']
        approver_rank = request.json['approver_rank']
        sanctioner_rank = request.json['sanctioner_rank']
        #employee_is_active =request.json['employee_is_active']
        update_at = datetime.datetime.today()
        employee_ResultSet=db.session.query(Employee.employee_id).filter(Employee.employee_email == employee_email)
        print("i am here")
        for email in employee_ResultSet:
            print(email.employee_id)
        ResultSet=db.session.query(Employee).filter(Employee.employee_id == email.employee_id).update({ 'user_permission' : user_permission, 'update_at' : update_at, 'emp_sites' : site_name, 'emp19' : int(approver_rank), 'emp20' : int(sanctioner_rank)},synchronize_session=False)
        try:
            db.session.commit()
            return jsonify({'Status' : 'Updated'})
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return jsonify({'error':str(e)})  

'''
{
	"data": [{
			"employee_email": "Email.com",
			"site_name": [
				"VMM",
				"All Cargo ",
				"Logos-B",
				"Pragati One",
				"Logos",
				"Ecom Express"
			],
			"permissions": [{
					"item_manager": {
						"create": 1,
						"edit": 1
					}
				},
				{
					"item_manager": {
						"create": 1,
						"edit": 1
					}
				},
				{
					"approver": {
						"rank": 1,
						"final": false
					}
				},
				{
					"sanction": {
						"rank": 2,
						"final": true
					}
				}
			]
		},
		{
			"employee_email": "email",
			"site_name": [
				"VMM",
				"All Cargo ",
				"Logos-B",
				"Pragati One",
				"Logos",
				"Ecom Express"
			],
			"user_permission": null
		}
	],
	"page": 1,
	"per_page": 6,
	"total": 20,
	"total_pages": 4.0
}
'''

@app.route('/employee-permissions', methods=['GET'])
@cross_origin()
def employee_permissions():   
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Employee).filter(Employee.employee_is_active=='true').all()
            total_records = len(ResultSet)
            data = []
            sitename = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            for record in ResultSet:

                site_ResultSet=db.session.query(Site.site_name).filter(Site.project_manager_id == record.employee_id)
                for name in site_ResultSet:
                    sitename.append(name.site_name)
                record_dict = {'employee_email' : record.employee_email, 
                'user_permission' : record.user_permission,
                'site_name' : record.emp_sites,
                'sites' : sitename}
                data.append(record_dict)
                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})



@app.route('/employee-id/<email>', methods=['GET'])
@cross_origin()
def employee_by_email(email):
    print(email)
    ResultSet=db.session.query(Employee).filter(Employee.employee_email == email).all()
    total_records = len(ResultSet)
    data = []
    resp = {
        "page": 1,
        "per_page": per_page,
        "total": total_records,
        "total_pages": math.ceil(total_records/per_page)
    }
    for record in ResultSet:
        record_dict = {'employee_id' : record.employee_id}
        data.append(record_dict)
        resp['data'] = data
    return jsonify(resp)



@app.route('/add-employee', methods=['POST'])
@cross_origin()
def employee_insert_by_name():
    if request.method == "POST":
        print(request.get_json(force=True))
        employee_name = request.json['employee_name']
        employee_email = request.json['employee_email']
        employee_designation = request.json['employee_designation']
        employee_contact = request.json['employee_contact']
        employee_address = request.json['employee_address']
        #created_by = request.json['created_by']
        created_at = datetime.datetime.today()
       

        employee=Employee( employee_name = employee_name, emp19 = 0, emp20 = 0, employee_email = employee_email, employee_designation = employee_designation, employee_contact = employee_contact, emp18=employee_address, created_at = created_at, emp_sites = json.loads('[]')
        )
        try:
            db.session.add(employee)
            db.session.commit()
            print(employee)
            return jsonify({str(employee) : 'Inserted'}) 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return jsonify({'error':str(e)})



@app.route('/employees', methods=['GET'])
@cross_origin()
def employee_name():   
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Employee).filter(Employee.employee_is_active=='true').all()
            total_records = len(ResultSet)
            data = []
            sitename = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            for record in ResultSet:

    
                record_dict = {'employee_id': record.employee_id,'employee_name' : record.employee_name ,'employee_email' : record.employee_email,
                'employee_address' : record.emp18, 'employee_designation' : record.employee_designation,'employee_contact' : record.employee_contact,  }
                data.append(record_dict)
                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})


@app.route('/employee/update-employee', methods=['PATCH'])
@cross_origin()
def employee_update():
    if request.method == "PATCH":
        print(request.get_json(force=True))
        employee_id = request.json['employee_id']
        employee_name = request.json['employee_name']
        employee_email = request.json['employee_email']
        employee_designation = request.json['employee_designation']
        employee_contact = request.json['employee_contact']
        employee_address = request.json['employee_address']
        update_at = datetime.datetime.today()
        
        ResultSet=db.session.query(Employee).filter(Employee.employee_id == employee_id).update( {'employee_name' : employee_name ,'employee_email' : employee_email,
                'emp18' : employee_address, 'employee_designation' : employee_designation,'employee_contact' : employee_contact },synchronize_session=False)
        try:
            db.session.commit()
            return jsonify({'Status' : 'Updated'})
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return jsonify({'error':str(e)})  


@app.route('/employee/delete-employee/<int:empid>', methods=['DELETE'])
@cross_origin()
def employee_delete(empid):
    if request.method == "DELETE":
        
        employee_is_active = 0
        ResultSet=db.session.query(Employee).filter(Employee.employee_id == empid).update({'employee_is_active' : employee_is_active},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Deleted'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e) 



@app.route('/upload-attachment', methods=['PUT'])
@cross_origin()
def upload_file():
    category = request.form['category']
    file = request.files['file']
    name = file.filename
    s3 = boto3.resource('s3',
         aws_access_key_id='AKIAXLEI4XOIT7PJVTNE',
         aws_secret_access_key= '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')
    #vendor, site

    s3.Bucket('warehouseattachments').put_object(Key=name,Body=file)
    if category == 'organisation':
        org_id = request.form['org_id']
        URL = 'https://warehouseattachments.s3.ap-south-1.amazonaws.com/'+name
        ResultSet =db.session.query(Org).filter(Org.org_id == org_id).update({'org_02' : URL},synchronize_session=False)
        db.session.commit()

    elif category == 'client':
        client_id = request.form['client_id']
        URL = 'https://warehouseattachments.s3.ap-south-1.amazonaws.com/'+name
        ResultSet =db.session.query(Client).filter(Client.id == client_id).update({'cl10' : URL},synchronize_session=False)
        db.session.commit()

    elif category == 'vendor':
        client_id = request.form['client_id']
        URL = 'https://warehouseattachments.s3.ap-south-1.amazonaws.com/'+name
        ResultSet =db.session.query(Client).filter(Client.id == client_id).update({'cl10' : URL},synchronize_session=False)
        db.session.commit()

    elif category == 'site':
        client_id = request.form['client_id']
        URL = 'https://warehouseattachments.s3.ap-south-1.amazonaws.com/'+name
        ResultSet =db.session.query(Client).filter(Client.id == client_id).update({'cl10' : URL},synchronize_session=False)
        db.session.commit()

    else:
        pass

    

    return 'uploaded'
   



@app.route('/view-approver', methods=['GET'])
@cross_origin()
def view_approver():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Employee).all()
            total_records = len(ResultSet)
            print(ResultSet)
            data = []
            approver_11 = []
            approver_22 = []
            approver_33 = []
            final_approver1 = []
            
            for record in ResultSet:
                if record.emp19 == None:
                    pass
                elif int(record.emp19) == 1:
                    approver_1 = record.employee_email
                    approver_11.append(approver_1)
                elif int(record.emp19) == 2:
                    approver_2 = record.employee_email
                    approver_22.append(approver_2)
                elif int(record.emp19) == 3:
                    approver_3 = record.employee_email
                    approver_33.append(approver_3)
                elif int(record.emp19) == 100:
                    final_approver = record.employee_email
                    final_approver1.append(final_approver)
            record_dict = {'approver_1' : approver_11, 'approver_2' : approver_22, 'approver_3' : approver_33, 'final_approver' : final_approver1}
            data.append(record_dict)
            #resp['data'] = data
            return jsonify(data)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})



@app.route('/view-sanctioner', methods=['GET'])
@cross_origin()
def view_sanctioner():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Employee).all()
            print(ResultSet)
            data = []
            approver_11 = []
            approver_22 = []
            approver_33 = []
            final_approver1 = []
            approver_1 = ''
            approver_2 = ''
            approver_3 = ''
            final_approver = ''
            for record in ResultSet:
                if record.emp20 == None:
                    pass
                elif int(record.emp20) == 1:
                    approver_1 = record.employee_email
                    approver_11.append(approver_1)
                elif int(record.emp20) == 2:
                    approver_2 = record.employee_email
                    approver_22.append(approver_2)
                elif int(record.emp20) == 3:
                    approver_3 = record.employee_email
                    approver_33.append(approver_3)
                elif int(record.emp20) == 100:
                    final_approver = record.employee_email
                    final_approver1.append(final_approver)
            record_dict = {'sanctioner_1' : approver_11, 'sanctioner_2' : approver_22, 'sanctioner_3' : approver_33, 'final_sanctioner' : final_approver1}
            data.append(record_dict)

            #resp['data'] = data
            return jsonify(data)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})