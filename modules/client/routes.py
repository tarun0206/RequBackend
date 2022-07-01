from __future__ import division
from modules.item.routes import uom_update
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
from modules.models import Client,Site,Employee,Vendor,UOM,Org,Item,Category
import numpy as np
import os
import datetime
import json
import pandas as pd
import math
import base64
import boto3
from botocore.exceptions import ClientError

client_module = Blueprint('client', __name__)
db.create_all()
CORS(app)

@app.route('/update-client', methods=['PATCH'])
@cross_origin()
def client_update():
    if request.method == "PATCH":
        #print(request.get_json(force=True))
        #client_id = request.json['client_id']
        client_name = request.form['client_name']
        payment_terms = request.form['payment_terms']
        id = request.form['client_id']
        #client_contact = request.form['client_contact']
        site_id = request.form['site_id']
        address = request.form['address']
        client_email = request.form['client_email']
        phone_number = request.form['phone_number']
        client_terms_and_condition = request.form['client_terms_and_condition']
        contact_person = request.form['contact_person']
        #client_attachment = request.json['client_attachment']
        #update_by = request.json['update_by']
        update_at = datetime.datetime.today()
        #ResultSet=db.session.query(Client).filter(Client.client_name == client_name )
        #for record in ResultSet:
            #print(record.id)
        yesfile = request.form['yesfile']
        if yesfile == 'yes':
            file = request.files['file']
            name = file.filename
            s3 = boto3.resource('s3',
                aws_access_key_id='AKIAXLEI4XOIT7PJVTNE',
                aws_secret_access_key= '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')
            
            s3.Bucket('warehouseattachments').put_object(Key=name,Body=file)
            URL = 'https://warehouseattachments.s3.ap-south-1.amazonaws.com/'+name
            ResultSet=db.session.query(Client).filter(Client.id == id).update({'client_name' : client_name,'payment_terms' : payment_terms,
            'site_id' : site_id, 'address' : address, 'client_email' : client_email,
            'phone_number' : phone_number, 'client_terms_and_condition' : client_terms_and_condition, 
            'contact_person': contact_person, 'update_at' : update_at, 'cl10' : URL},synchronize_session=False)
        else:
            ResultSet=db.session.query(Client).filter(Client.id == id).update({'client_name' : client_name,'payment_terms' : payment_terms,
            'site_id' : site_id, 'address' : address, 'client_email' : client_email,
            'phone_number' : phone_number, 'client_terms_and_condition' : client_terms_and_condition, 
            'contact_person': contact_person, 'update_at' : update_at},synchronize_session=False)
        try:
            db.session.commit()
            return jsonify({'Status' : 'Updated'})
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return jsonify({'error':str(e)})    

@app.route('/update-site', methods=['PATCH'])
@cross_origin()
def site_update():
    if request.method == "PATCH":
        #print(request.get_json(force=True))
        site_id = request.form['site_id']
        site_name = request.form['site_name']
        location = request.form['location']
        #city = request.form['city']
        address = request.form['delivery_address']
        #phone_number = request.form['phone_number']
        #contact_person = request.form['contact_person']
        #cost_center = request.form['cost_center']
        project_director_id = request.form['project_director_id']
        project_manager_id = request.form['project_manager_id']
        store_keeper_id = request.form['store_keeper_id']
        client_name = request.form['client_name']
        update_by = 1
        update_at = datetime.datetime.today()
        #ResultSet=db.session.query(Site).filter(Site.site_name == site_name)
        #for record in ResultSet:
        #    print(record.id)
        yesfile = request.form['yesfile']
        if yesfile == 'yes':
            file = request.files['file']
            name = file.filename
            s3 = boto3.resource('s3',
                aws_access_key_id='AKIAXLEI4XOIT7PJVTNE',
                aws_secret_access_key= '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')
            
            s3.Bucket('warehouseattachments').put_object(Key=name,Body=file)
            URL = 'https://warehouseattachments.s3.ap-south-1.amazonaws.com/'+name
            ResultSet=db.session.query(Site).filter(Site.id == site_id).update({'site_name' : site_name, 'location' : location,
            'address' : address,'project_director_id' : project_director_id, 'project_manager_id' : project_manager_id, 
            'store_keeper_id' : store_keeper_id, 'client_name' : client_name, 'update_by' : update_by, 'update_at' : update_at, 'si16' : URL},synchronize_session=False)
        else:
            ResultSet=db.session.query(Site).filter(Site.id == site_id).update({'site_name' : site_name, 'location' : location,
            'address' : address,'project_director_id' : project_director_id, 'project_manager_id' : project_manager_id, 
            'store_keeper_id' : store_keeper_id, 'client_name' : client_name, 'update_by' : update_by, 'update_at' : update_at},synchronize_session=False)
        try:
            db.session.commit()
            return jsonify({'Status' : 'Updated'})
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return jsonify({'error':str(e)})
        



@app.route('/add-client', methods=['POST'])
@cross_origin()
def client_insert():
    if request.method == "POST":
        #print(request.get_json(force=True))
        client_name =  request.form['client_name']
        #formify({str(client) : 'Inserted'}) 
        print(client_name)
        payment_terms = request.form['payment_terms']
        created_at = datetime.datetime.today()
        site_id = request.form['site_id']
        address = request.form['address']
        client_email = request.form['client_email']
        phone_number = request.form['phone_number']
        client_terms_and_condition = request.form['client_terms_and_condition']
        contact_person = request.form['contact_person']
        created_at = datetime.datetime.today()
        yesfile = request.form['yesfile']
        if yesfile == 'yes':

            file = request.files['file']
            name = file.filename
            s3 = boto3.resource('s3',
                aws_access_key_id='AKIAXLEI4XOIT7PJVTNE',
                aws_secret_access_key= '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')
            
            s3.Bucket('warehouseattachments').put_object(Key=name,Body=file)
            URL = 'https://warehouseattachments.s3.ap-south-1.amazonaws.com/'+name

            client=Client(client_name = client_name,payment_terms = payment_terms,created_at = created_at,
            site_id = int(site_id), address = address, client_email = client_email, phone_number = phone_number, client_terms_and_condition = client_terms_and_condition,
            contact_person = contact_person, cl10 = URL)

        else:
        
            file = None
            client=Client(client_name = client_name,payment_terms = payment_terms,created_at = created_at,
            site_id = int(site_id), address = address, client_email = client_email, phone_number = phone_number, client_terms_and_condition = client_terms_and_condition,
            contact_person = contact_person)
        
        
        
            
        try:
            db.session.add(client)
            db.session.commit()
            print(client)
            return jsonify({str(client) : 'Inserted'}) 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return jsonify({'error':str(e)})

@app.route('/add-site', methods=['POST'])
@cross_origin()
def site_insert():
    if request.method == "POST":
        #site_id = request.json['site_id']
        site_name = request.form['site_name']
        location = request.form['location']
        #city = request.form['city']
        address = request.form['address']
        #phone_number = request.form['phone_number']
        #contact_person = request.form['contact_person']
        #cost_center = request.form['cost_center']
        project_director_id = request.form['project_director_id']
        project_manager_id = request.form['project_manager_id']
        store_keeper_id = request.form['store_keeper_id']
        client_name = request.form['client_name']
        yesfile = request.form['yesfile']
        created_by = 1
        created_at = datetime.datetime.today()
        if yesfile == 'yes':
            file = request.files['client_attachment']
            name = file.filename
            s3 = boto3.resource('s3',
                aws_access_key_id='AKIAXLEI4XOIT7PJVTNE',
                aws_secret_access_key= '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')
                        
            s3.Bucket('warehouseattachments').put_object(Key=name,Body=file)
            URL = 'https://warehouseattachments.s3.ap-south-1.amazonaws.com/'+name

                    
            site=Site(site_name = site_name, location = location, address = address, project_director_id = project_director_id, project_manager_id = project_manager_id, store_keeper_id = store_keeper_id, client_name = client_name, created_by = created_by, created_at = created_at, si16 = URL)
        else:

            site=Site(site_name = site_name, location = location, address = address, project_director_id = project_director_id, project_manager_id = project_manager_id, store_keeper_id = store_keeper_id, client_name = client_name, created_by = created_by, created_at = created_at)
        try:
            db.session.add(site)
            db.session.commit()
            print(site)
            return jsonify({str(site) : 'Inserted'}) 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return jsonify({'error':str(e)})





@app.route('/sites/<clientid>', methods=['GET'])
@cross_origin()
def site_by_client_id(clientid=None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Site).filter(Site.client_id == clientid)
            total_records = ResultSet.count()
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            for record in ResultSet:
                record_dict = {'site_id' : record.site_id, 'site_name' : record.site_name, 'location' : record.location, 'city' : record.city, 'address' : record.address, 'phone_number' : record.phone_number, 'contact_person' : record.contact_person, 'cost_center' : record.cost_center, 'project_director_id' : record.project_director_id, 'project_manager_id' : record.project_manager_id, 'client_id' : record.client_id, 'created_by' : record.created_by, 'created_at' : record.created_at, 'update_by' : record.update_by , 'update_at' : record.update_at}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/sites/<siteid>', methods=['GET'])
@cross_origin()
def sites_by_site_id(siteid=None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Site).filter(Site.site_id == siteid)
            total_records = ResultSet.count()
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            for record in ResultSet:
                record_dict =  {'site_id' : record.site_id, 'site_name' : record.site_name, 'location' : record.location, 'city' : record.city, 'address' : record.address, 'phone_number' : record.phone_number, 'contact_person' : record.contact_person, 'cost_center' : record.cost_center, 'project_director_id' : record.project_director_id, 'project_manager_id' : record.project_manager_id, 'client_id' : record.client_id, 'created_by' : record.created_by, 'created_at' : record.created_at, 'update_by' : record.update_by , 'update_at' : record.update_at}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/employee/<designation>', methods=['GET'])
@cross_origin()
def employee_designation(designation=None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Employee).filter(Employee.employee_designation == designation)
            total_records = ResultSet.count()
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            for record in ResultSet:
                record_dict =  {'employee_id' : record.employee_id, 'employee_name' : record.employee_name, 'employee_email' : record.employee_email, 'employee_designation' : record.employee_designation, 'employee_contact' : record.employee_contact, 'created_by' : record.created_by, 'created_at' : record.created_at, 'update_by' : record.update_by , 'update_at' : record.update_at }
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/client', methods=['GET'])
@cross_origin()
def client():   
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Client).all()
            total_records = len(ResultSet)
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            for record in ResultSet:
                #print(record)
                site_name=db.session.query(Site).filter(Site.id==record.site_id).all()
                if len(site_name) > 0:
                    sitename = site_name[0].site_name
                else :
                    sitename = "Not Assigned"
                record_dict = {'client_id' : record.id, 'client_name' : record.client_name, 'payment_terms' : record.payment_terms
                ,'site_name' : sitename , 'address' : record.address , 'client_email' : record.client_email, 'client_attachment' : str(record.client_attachment)
                ,'phone_number' : record.phone_number, 'client_terms_and_condition' : record.client_terms_and_condition, 'contact_person' : record.contact_person
                , 'client_attachment' : record.cl10}
                data.append(record_dict)

                resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})

@app.route('/delete-client/<id>', methods=['DELETE'])
@cross_origin()
def client_delete(id):
    if request.method == "DELETE":
        record = db.session.query(Client).filter(Client.id == int(id)).delete()
        try:
            db.session.commit()
            return jsonify({'Status' : 'Deleted'})
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return jsonify({'error':str(e)})

@app.route('/delete-site/<id>', methods=['DELETE'])
@cross_origin()
def site_delete(id):
    if request.method == "DELETE":
        record = db.session.query(Site).filter(Site.id == int(id)).delete()
        try:
            db.session.commit()
            return jsonify({'Status' : 'Deleted'})
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return jsonify({'error':str(e)})

@app.route('/sites', methods=['GET'])
@cross_origin()
def site():
    if request.method == "GET":
        try :
            
            ResultSet=db.session.query(Site).all()
            print(ResultSet)            
            total_records = len(ResultSet)
            record_dict =  {}
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            for record in ResultSet:
                proj_director=db.session.query(Employee).filter(Employee.employee_id==record.project_director_id).all()
                #for dir_details in proj_director :
                    #pass
                if len(proj_director) > 0:
                    dir_employee_id = proj_director[0].employee_id
                    dir_employee_name = proj_director[0].employee_name
                    dir_employee_email = proj_director[0].employee_email
                    dir_employee_contact = proj_director[0].employee_contact
                else :
                    dir_employee_id = "Not Assigned"
                    dir_employee_name = "Not Assigned"
                    dir_employee_email = "Not Assigned"
                    dir_employee_contact = "Not Assigned"
                    #print(dir_details.employee_id, dir_details.employee_name, dir_details.employee_email, dir_details.employee_contact)

                proj_manager=db.session.query(Employee).filter(Employee.employee_id==record.project_manager_id).all()
                #for manager_details in proj_manager :
                #    pass
                if len(proj_manager) > 0:
                    man_employee_id = proj_manager[0].employee_id
                    man_employee_name = proj_manager[0].employee_name
                    man_employee_email = proj_manager[0].employee_email
                    man_employee_contact = proj_manager[0].employee_contact
                else :
                    man_employee_id = "Not Assigned"
                    man_employee_name = "Not Assigned"
                    man_employee_email = "Not Assigned"
                    man_employee_contact = "Not Assigned"
                    #print(manager_details.employee_id, manager_details.employee_name, manager_details.employee_email, manager_details.employee_contact)

                proj_store_keeper=db.session.query(Employee).filter(Employee.employee_id==record.store_keeper_id)
                for store_keeper_details in proj_store_keeper :
                    pass
                    #print(store_keeper_details.employee_id, store_keeper_details.employee_name, store_keeper_details.employee_email, store_keeper_details.employee_contact)
                #client_name=db.session.query(Client).filter(Client.id==record.client_id).all()
                #if len(client_name) > 0:
                #    clientname = client_name[0].client_name
                #else :
                #    clientname = "Not Assigned"
                record_dict = {'site_id' : record.id, 'site_name' : record.site_name, 'location' : record.location, 'delivery_address' : record.address, 'client_name' : record.client_name,
                'project_director_id' : dir_employee_id, 'project_director_name' : dir_employee_name , 'project_director_contact' : dir_employee_contact, 'project_director_email' : dir_employee_email,
                'project_manager_id' : man_employee_id, 'project_manager_name' : man_employee_name , 'project_manager_contact' : man_employee_contact, 'project_manager_email' : man_employee_email,
                'store_keeper_id' : store_keeper_details.employee_id,'store_keeper_name' : store_keeper_details.employee_name , 'site_attachment' : record.si16, 'store_keeper_contact' : store_keeper_details.employee_contact, 'store_keeper_email' : store_keeper_details.employee_email
                }
                data.append(record_dict)
            
           
            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})


@app.route('/sites-without-client', methods=['GET'])
@cross_origin()
def site_with_client():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Site).filter(Site.client_id != None)
            total_records = ResultSet.count()
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            for record in ResultSet:
                proj_director=db.session.query(Employee).filter(Employee.employee_id==record.project_director_id)
                for dir_details in proj_director :
                    pass
                    #print(dir_details.employee_id, dir_details.employee_name, dir_details.employee_email, dir_details.employee_contact)

                proj_manager=db.session.query(Employee).filter(Employee.employee_id==record.project_manager_id)
                for manager_details in proj_manager :
                    pass
                    #print(manager_details.employee_id, manager_details.employee_name, manager_details.employee_email, manager_details.employee_contact)

                proj_store_keeper=db.session.query(Employee).filter(Employee.employee_id==record.store_keeper_id)
                for store_keeper_details in proj_store_keeper :
                    pass
                    #print(store_keeper_details.employee_id, store_keeper_details.employee_name, store_keeper_details.employee_email, store_keeper_details.employee_contact)

                record_dict = {'site_id' : record.id, 'site_name' : record.site_name, 'location' : record.location, 'delivery_address' : record.address,  
                'project_director_id' : dir_details.employee_id, 'project_director_name' : dir_details.employee_name , 'project_director_conatct' : dir_details.employee_contact, 'project_director_email' : dir_details.employee_email,
                'project_manager_id' : manager_details.employee_id, 'project_manager_name' : manager_details.employee_name , 'project_manager_conatct' : manager_details.employee_contact, 'project_manager_email' : manager_details.employee_email,
                'store_keeper_id' : store_keeper_details.employee_id,'store_keeper_name' : store_keeper_details.employee_name , 'store_keeper_conatct' : store_keeper_details.employee_contact, 'store_keeper_email' : store_keeper_details.employee_email
                }
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/sites-with-client', methods=['GET'])
@cross_origin()
def site_without_client():
    if request.method == "GET":
        try :
        
            ResultSet=db.session.query(Site).filter(Site.client_id == None) 
            print(ResultSet)            
            total_records = ResultSet.count()
            record_dict =  {}
            data = []
            resp = {
                "page": 1,
                "per_page": per_page,
                "total": total_records,
                "total_pages": math.ceil(total_records/per_page)
            }
            for record in ResultSet:
                proj_director=db.session.query(Employee).filter(Employee.employee_id==record.project_director_id)
                for dir_details in proj_director :
                    pass
                    #print(dir_details.employee_id, dir_details.employee_name, dir_details.employee_email, dir_details.employee_contact)

                proj_manager=db.session.query(Employee).filter(Employee.employee_id==record.project_manager_id)
                for manager_details in proj_manager :
                    pass
                    #print(manager_details.employee_id, manager_details.employee_name, manager_details.employee_email, manager_details.employee_contact)

                proj_store_keeper=db.session.query(Employee).filter(Employee.employee_id==record.store_keeper_id)
                for store_keeper_details in proj_store_keeper :
                    pass
                    #print(store_keeper_details.employee_id, store_keeper_details.employee_name, store_keeper_details.employee_email, store_keeper_details.employee_contact)

                record_dict = {'site_id' : record.id, 'site_name' : record.site_name, 'location' : record.location, 'delivery_address' : record.address,  
                'project_director_id' : dir_details.employee_id, 'project_director_name' : dir_details.employee_name , 'project_director_conatct' : dir_details.employee_contact, 'project_director_email' : dir_details.employee_email,
                'project_manager_id' : manager_details.employee_id, 'project_manager_name' : manager_details.employee_name , 'project_manager_conatct' : manager_details.employee_contact, 'project_manager_email' : manager_details.employee_email,
                'store_keeper_id' : store_keeper_details.employee_id,'store_keeper_name' : store_keeper_details.employee_name , 'store_keeper_conatct' : store_keeper_details.employee_contact, 'store_keeper_email' : store_keeper_details.employee_email
                }
                data.append(record_dict)
               
           
            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

def allowed_file(filename):
    
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/import', methods=['POST'])
@cross_origin()
def import_file():
   if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
        print(filename[:-4].title())
       
        file_name = os.path.join(filename)
        print(file_name)
        csv_data=pd.read_csv(file_name) 
        #print(csv_data)
        created_at = datetime.datetime.today()
        try:
            if filename[:-4] == 'client':
                csv_data_org = csv_data.loc[ : , ['client_name','payment_terms','created_by','site_id','address','client_email',
                                                    'phone_number','client_terms_and_condition','contact_person'] ]
                csv_data_list=csv_data_org.values.tolist()
                print(csv_data_list)
                for row in csv_data_list:
                
                    print(row[0])
                    client=Client(client_name = row[0], payment_terms = row[1],created_by = row[2],created_at = created_at
                    ,site_id = row[3], address = row[4], client_email = row[5], phone_number = row[6], client_terms_and_condition = row[7],
                    contact_person = row[8])

        
                    db.session.add(client)
                    db.session.commit()
                    print(client)
                    #os.remove(file_name)
                return jsonify({str(client) : 'Inserted'}) 

            elif filename[:-4] == 'employee':
                csv_data_org = csv_data.loc[ : , ['employee_name','created_by','employee_contact','employee_is_active','employee_email',
                                                    'employee_designation','user_permission','emp18','emp19','emp20','emp21'] ]
                csv_data_list=csv_data_org.values.tolist()
                print(csv_data_list)
                for row in csv_data_list:
                
                    print(json.loads(row[6]))
                    employee=Employee(employee_name = row[0], created_by = None, created_at = created_at, employee_contact = row[2]
                    , employee_is_active = row[3], employee_email = row[4], employee_designation = row[5],
                    user_permission = json.loads(row[6]),emp18 = row[7],emp19 = int(row[8]),emp20 = int(row[9]),emp21 = row[10])

        
                    db.session.add(employee)
                    db.session.commit()
                    print(employee)
                os.remove(file_name)
                return jsonify({str(employee) : 'Inserted'})

            elif filename[:-4] == 'category':
                csv_data_org = csv_data.loc[ : , ['category_name','category_code','parent_category','parent_category_code','category_description',
                                                    'category_is_active'] ]
                csv_data_list=csv_data_org.values.tolist()
                print(csv_data_list)
                for row in csv_data_list:
                
                    #print(row[1])
                    category=Category(category_name = row[0], category_code = row[1], created_at = created_at, parent_category = row[2]
                    , parent_category_code = row[3], category_description = row[4], category_is_active = row[5])

        
                    db.session.add(category)
                    db.session.commit()
                    print(category)
                    os.remove(file_name)
                return jsonify({str(category) : 'Inserted'})

            elif filename[:-4] == 'item':

                csv_data_org = csv_data.loc[ : , ['item_name','item_gst','item_specification','item_description','category_id',
                                                'sub_category','uom','item_is_active'] ]
                csv_data_list=csv_data_org.values.tolist()
                print(csv_data_list)
                for row in csv_data_list:
                    print(row[6][1:-1])
                    uomid = int(row[6][1:-1])
                    #print(row[1])
                    item=Item(item_name = row[0], item_gst = row[1], item_specification = row[2], created_at = created_at, item_description = row[3]
                    , category_id = row[4], sub_category = row[5], uom = uomid, item_is_active = row[7])

        
                    db.session.add(item)
                    db.session.commit()
                    print(item)
                    os.remove(file_name)
                return jsonify({str(item) : 'Inserted'})

            elif filename[:-4] == 'uom':

                csv_data_org = csv_data.loc[ : , ['symbol_code','category_id','uom_name','messurement',
                                                'description'] ]
                csv_data_list=csv_data_org.values.tolist()
                print(csv_data_list)
                for row in csv_data_list:
                
                    #print(row[1])
                    uom=UOM(symbol_code = row[0], category_id = row[1],uom_name = row[2],created_at = created_at,messurement = row[3]
                    ,description = row[4])

        
                    db.session.add(uom)
                    db.session.commit()
                    print(uom)
                    os.remove(file_name)
                return jsonify({str(uom) : 'Inserted'})

            elif filename[:-4] == 'vendor':

                csv_data_org = csv_data.loc[ : , ['vendor_name','vendor_type','category_name','vendor_contact_person','vendor_phone_number',
                                                'vendor_email','vendor_address','vendor_payment_terms','vendor_terms_and_conditions'] ]
                csv_data_list=csv_data_org.values.tolist()
                print(csv_data_list)
                for row in csv_data_list:
                
                
                    vendor=Vendor(vendor_name = row[0], vendor_type = row[1],category_name = row[2]
                    ,vendor_contact_person = row[3], vendor_phone_number = row[4], vendor_email = row[5], vendor_address = row[6], vendor_payment_terms = row[7],
                    vendor_terms_and_conditions = row[8])

        
                    db.session.add(vendor)
                    db.session.commit()
                    print(vendor)
                    os.remove(file_name)
                return jsonify({str(vendor) : 'Inserted'})

            elif filename[:-4] == 'org':

                csv_data_org = csv_data.loc[ : , ['org_location','org_contact_person_id','org_designation','org_phone_number','org_email',
                                                'org_address'] ]
                csv_data_list=csv_data_org.values.tolist()
                print(csv_data_list)
                for row in csv_data_list:
               
                
                    #print(row[1])
                    org=Org(org_location = row[0], org_contact_person_id = row[1],org_designation = row[2]
                    ,org_phone_number = row[3], org_email = row[4], org_address = row[5])
        
                    db.session.add(org)
                    db.session.commit()
                    print(org)
                    os.remove(file_name)
                return jsonify({str(org) : 'Inserted'})

            
            elif filename[:-4] == 'site':

                csv_data_org = csv_data.loc[ : , ['site_name','location','city','address','phone_number',
                                                'contact_person','cost_center','project_director_id','project_manager_id','store_keeper_id',
                                                'client_name','created_by'] ]
                csv_data_list=csv_data_org.values.tolist()
                print(csv_data_list)
                for row in csv_data_list:
                
                    site=Site(site_name = row[0], location = row[1],city = row[2]
                    ,address = row[3], phone_number = row[4], contact_person = row[5], cost_center = row[6], project_director_id = row[7], project_manager_id = row[8],
                    store_keeper_id = row[9], client_name = row[10], created_at = created_at, created_by = row[11])
        
                    db.session.add(site)
                    db.session.commit()
                    print(site)
                    os.remove(file_name)
                return jsonify({str(site) : 'Inserted'})

        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})





@app.route('/import-new', methods=['POST'])
@cross_origin()
def import_new():
   if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
        print(filename[:-4].title())
       
        file_name = os.path.join(filename)
        print(file_name)
        csv_data=pd.read_csv(file_name) 
        #print(csv_data)
        created_at = datetime.datetime.today()
        try:
                csv_data_org = csv_data.loc[ : , ['category_name','category_code','parent_category','parent_category_code','category_description',
                                                    'category_is_active'] ]
                csv_data_list=csv_data_org.values.tolist()
                print(csv_data_list)
                for row in csv_data_list:
                
                    #print(row[1])
                    category=Category(category_name = row[0], category_code = row[1], created_at = created_at, parent_category = row[2]
                    , parent_category_code = row[3], category_description = row[4], category_is_active = row[5])

        
                    db.session.add(category)
                    db.session.commit()
                    print(category)
                    os.remove(file_name)
                return jsonify({str(category) : 'Inserted'})


        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/item-import-csv', methods=['POST'])
@cross_origin()
def import_temp():
   if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
        print(filename[:-4].title())
       
        file_name = os.path.join(filename)
        print(file_name)
        csv_data=pd.read_csv(file_name)
        df1 = csv_data.where((pd.notnull(csv_data)), None)
        #created_at = datetime.datetime.today()
        try:
                csv_data_org = df1.loc[ : , ['Item','Category','UOM','GST %','Vendors','Description'] ]
                csv_data_list=csv_data_org.values.tolist()
                #print(csv_data_list)
                
                for row in csv_data_list:
                    item_name = row[0]
                    item_gst = row[3]
                    symbol_code = row[2]
                    categoryname = row[1]
                    vendors = row[4]
                    seller_name = vendors.split(",")
                    categoryiid = ''
                    category_id=db.session.query(Category).filter(Category.category_name==categoryname).all()
                    for cat in category_id:
                        categoryiid = cat.category_id
                    uomid = []
                    inst = isinstance(symbol_code, list) 
                    if not inst :

                        uom_id=db.session.query(UOM).filter(UOM.symbol_code==symbol_code).all()
                        for uid in uom_id:
                            uomid.append(int(uid.uom_id))
                    else :
                        
                        for code in symbol_code:
                            if code :
                                uom_id=db.session.query(UOM).filter(UOM.symbol_code==code).all()
                                for uid in uom_id:
                                    uomid.append(int(uid.uom_id))
                            else :
                                uomid.append(int(0))
                    sellerid = []
                    seller_asst = []
                    inst_seller = isinstance(seller_name, list) 
                    if not inst_seller :

                        seller_asst.append(seller_name)
                        seller_id=db.session.query(Vendor).filter(Vendor.vendor_name==seller_name).all()
                        for sid in seller_id:
                            sellerid.append(int(sid.vendor_id))
                    else :
                        
                        for code in seller_name:
                            if code :
                                seller_asst.append(code)
                                seller_id=db.session.query(Vendor).filter(Vendor.vendor_name==code).all()
                                for sid in seller_id:
                                    sellerid.append(int(sid.vendor_id))
                            else :
                                sellerid.append(int(0))
                    created_at = datetime.datetime.today()
                    ResultSet = db.session.query(Item).filter(Item.item_name == row[0]).all()
                    if len(ResultSet) == 0:
                        item=Item(item_name = item_name, item_gst = item_gst, category_id = categoryiid, uom = uomid,  created_at = created_at, vendor_name = sellerid, item_specification = row[5])
                        db.session.add(item)
                        db.session.commit()
                    else:
                        pass
                '''
                    ResultSet = db.session.query(Category).filter(Category.category_name == row[1]).all()
                    if len(ResultSet) == 0:
                        category=Category(category_name = row[1], category_code = code, created_at = created_at, parent_category = '1', category_is_active = True)
                        db.session.add(category)
                        db.session.commit()
                    else:
                        pass
                '''
                os.remove(file_name)
                return jsonify({str('category') : 'Inserted'})


        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/vendor-import', methods=['POST'])
@cross_origin()
def import_vendor():
   if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
        #print(filename[:-4].title())
       
        file_name = os.path.join(filename)
        #print(file_name)
        csv_data=pd.read_csv(file_name)
        df1 = csv_data.where((pd.notnull(csv_data)), None)
        #created_at = datetime.datetime.today()
        try:
                csv_data_org = df1.loc[ : , ['Vendor Name','Type','Category Name','Phone Number','Email','Address','Payment Terms','Contact Person'] ]
                csv_data_list=csv_data_org.values.tolist()
                #print(csv_data_list)
                for row in csv_data_list:
                
                    #new = {}
                    c = row[2].replace('/', ',')
                    string_list = c.split(",")
                    ResultSet = db.session.query(Vendor).filter(Vendor.vendor_name == row[0]).all()
                    pno1 = str(row[3])
                    pno = pno1.replace(" ","")
                    if len(pno) == 13:
                        pno = pno[3:]
                    else:
                        pass
                    if len(pno) == 4:
                        pno = None
                    if len(ResultSet) == 0:
                        category=Vendor(vendor_name = row[0], vendor_type = row[1], vendor_contact_person = row[7], vendor_phone_number = pno, vendor_email = row[4], vendor_address = row[5], vendor_payment_terms = row[6], category_name = string_list)
                        db.session.add(category)
                        db.session.commit()
                    else:
                        pass
                os.remove(file_name)
                return jsonify({str('vendor') : 'Inserted'})


        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/temp-importt', methods=['POST'])
@cross_origin()
def import_ttemp():
   if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
        print(filename[:-4].title())
       
        file_name = os.path.join(filename)
        print(file_name)
        csv_data=pd.read_csv(file_name)
        created_at = datetime.datetime.today()
        
        n = 79
        try:
                csv_data_org = csv_data.loc[ : , ['Category'] ]
                csv_data_list=csv_data_org.values.tolist()
                print(csv_data_list)
                for row in csv_data_list:
                    n = n + 1
                    strr = str(n)
                    code = ""
                    if len(strr) == 1:
                        code = '00' + strr
                    elif len(strr) == 2:
                        code = '0' + strr
                    else:
                        code = strr
                    print(code)
                    ResultSet = db.session.query(Category).filter(Category.category_name == row[0]).all()
                    if len(ResultSet) == 0:
                        category=Category(category_name = row[0], category_code = code, created_at = created_at, parent_category = '1', category_is_active = True)
                        db.session.add(category)
                        db.session.commit()
                    else:
                        pass
                os.remove(file_name)
                return jsonify({str('category') : 'Inserted'})


        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/vendor-importtt', methods=['POST'])
@cross_origin()
def importtt_vendor():
   if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)

        file_name = os.path.join(filename)
        csv_data=pd.read_csv(file_name)
        #created_at = datetime.datetime.today()
        no=1
        try:
                csv_data_org = csv_data.loc[ : , ['Vendors'] ]
                csv_data_list=csv_data_org.values.tolist()
                for row in csv_data_list:

                    
                    string_list = row[0].split(",")
                    
                    for n in string_list:
                        ResultSet = db.session.query(Vendor).filter(Vendor.vendor_name == n).all()
                        if len(ResultSet) == 0:
                            category=Vendor(vendor_name = n, vendor_type = 'Material', vendor_contact_person = 'abcd', vendor_phone_number = 9923546234, vendor_email = 'abcd@gmail.com', vendor_address = 'abcd dummy address', vendor_payment_terms = 'dummy payment terms' , vendor_terms_and_conditions = 'dummy terms and conditions')
                            db.session.add(category)
                            db.session.commit()
                        else:
                            pass
                    '''
                    ResultSet = db.session.query(Vendor).filter(Vendor.vendor_name == row[0]).all()
                    if len(ResultSet) == 0:
                        category=Vendor(vendor_name = row[0], vendor_type = 'Material', vendor_contact_person = 'abcd', vendor_phone_number = 9923546234, vendor_email = 'abcd@gmail.com', vendor_address = 'abcd dummy address', vendor_payment_terms = 'dummy payment terms' , vendor_terms_and_conditions = 'dummy terms and conditions')
                        db.session.add(category)
                        db.session.commit()
                    else:
                        pass
                    '''
                os.remove(file_name)
                return jsonify({str('vendor') : 'Inserted'})


        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})


@app.route('/temp-importtt', methods=['POST'])
@cross_origin()
def import_tttemp():
   if request.method == 'POST':
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
        print(filename[:-4].title())
       
        file_name = os.path.join(filename)
        print(file_name)
        csv_data=pd.read_csv(file_name)
        #created_at = datetime.datetime.today()
        
        #n = 79
        try:
                csv_data_org = csv_data.loc[ : , ['UOM'] ]
                csv_data_list=csv_data_org.values.tolist()
                print(csv_data_list)
                for row in csv_data_list:
                    ResultSet = db.session.query(UOM).filter(UOM.symbol_code == row[0]).all()
                    if len(ResultSet) == 0:
                        category=UOM(symbol_code = row[0])
                        db.session.add(category)
                        db.session.commit()
                    else:
                        pass
                os.remove(file_name)
                return jsonify({str('category') : 'Inserted'})


        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})

@app.route('/itemm-import-csv', methods=['PATCH'])
@cross_origin()
def importt_temp():
   if request.method == 'PATCH':
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)
        print(filename[:-4].title())
       
        file_name = os.path.join(filename)
        print(file_name)
        csv_data=pd.read_csv(file_name)
        df1 = csv_data.where((pd.notnull(csv_data)), None)
        #created_at = datetime.datetime.today()
        try:
            
                csv_data_org = df1.loc[ : , ['item_id','vendor_name(column to be added)'] ]
                csv_data_list=csv_data_org.values.tolist()
                #print(csv_data_list)
                vendor = []
                for row in csv_data_list:
                    mList = [int(e) if e.isdigit() else e for e in row[1].split(',')]
                    ResultSet=db.session.query(Item).filter(Item.item_id == row[0]).update({'vendor_name' : mList})
                    db.session.commit()
                os.remove(file_name)
                return jsonify({str('category') : 'Inserted'})


        except exc.SQLAlchemyError as e  :
            print(e)
            return jsonify({'error':str(e)})