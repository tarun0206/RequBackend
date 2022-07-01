from __future__ import division
from logging import error
from flask import request, jsonify, make_response, Blueprint
from flask_cors import CORS, cross_origin
from modules import app, db, per_page
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from modules.models import Item,Category,UOM,Association,Vendor,ItemAssociation
import datetime
import json
import pandas
import math
    
item_module = Blueprint('item', __name__)
db.create_all()
CORS(app)

@app.route('/update-item', methods=['PATCH'])
@cross_origin()
def item_update():
    if request.method == "PATCH":
        print(request.get_json(force=True))
        category_id = request.json['category_id']
        symbol_code = request.json['symbol_code']
        item_id = request.json['item_id']
        item_name = request.json['item_name']
        item_gst = request.json['item_gst']
        item_specification = request.json['item_specification']
        seller_name = request.json['seller_name']
        #category_id=db.session.query(Category).filter(Category.category_name==category_name).all()
        if len(category_id) > 0:
            categoryid = int(category_id)
        else :

            categoryid = "Not Assigned category"
        uomid = []
        inst = isinstance(symbol_code, list) 
        print(inst)
        if not inst :

            print("inside")
            uom_id=db.session.query(UOM).filter(UOM.symbol_code==symbol_code).all()
            for uid in uom_id:
                uomid.append(int(uid.uom_id))
        else :
            
            for code in symbol_code:
                if code :
                    print(code)
                    uom_id=db.session.query(UOM).filter(UOM.symbol_code==code).all()
                    for uid in uom_id:
                        uomid.append(int(uid.uom_id))
                else :
                    uomid.append(int(0))
        print(uomid)
        sellerid = []
        inst_seller = isinstance(seller_name, list) 
        print(inst_seller)
        if not inst_seller :

            print("inside")
            seller_id=db.session.query(Vendor).filter(Vendor.vendor_name==seller_name).all()
            for sid in seller_id:
                sellerid.append(int(sid.vendor_id))
        else :
            
            for code in seller_name:
                if code :
                    print(code)
                    seller_id=db.session.query(Vendor).filter(Vendor.vendor_name==code).all()
                    for sid in seller_id:
                        sellerid.append(int(sid.vendor_id))
                else :
                    sellerid.append(int(0))
        print(sellerid)
        ResultSet=db.session.query(Item).filter(Item.item_id == item_id).update({'item_name' : item_name,'item_gst' : item_gst,'item_specification' : item_specification,
        'category_id' : categoryid, 'uom' : uomid, 'vendor_name' : sellerid},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)    

@app.route('/update-category', methods=['PATCH'])
@cross_origin()
def category_update():
    if request.method == "PATCH":
        print(request.get_json(force=True))
        category_id = request.json['category_id']
        category_name = request.json['category_name']
        parent_category = request.json['parent_category']
        #parent_category_code = request.json['parent_category_code']
        category_code = request.json['category_code']
        ResultSet=db.session.query(Category).filter(Category.category_id == category_id).update({'category_name' : category_name, 'parent_category' : parent_category, 'category_code' : category_code},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)
        
    
@app.route('/update-unit-of-measurement', methods=['PATCH'])
@cross_origin()
def uom_update():
    if request.method == "PATCH":
        print(request.get_json(force=True))
        uom_id = request.json['uom_id']
        symbol_code = request.json['symbol_code']
        description = request.json['description']
        ResultSet=db.session.query(UOM).filter(UOM.uom_id == uom_id).update({'symbol_code' : symbol_code, 'description' : description},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Updated'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)   

@app.route('/add-item', methods=['POST'])
@cross_origin()
def item_insert():
    if request.method == "POST":
        print(request.get_json(force=True))
        item_name = request.json['item_name']
        item_gst = request.json['item_gst']
        item_specification = request.json['item_specification']
        symbol_code = request.json['symbol_code']
        print(symbol_code)
        category_id = request.json['category_name']
        seller_name = request.json['seller_name']
        #category_id=db.session.query(Category).filter(Category.category_name==category_name).all()
        if len(category_id) > 0:
            categoryid = int(category_id)
        else :
            categoryid = "Not Assigned"
        uomid = []
        inst = isinstance(symbol_code, list) 
        print(inst)
        if not inst :

            print("inside")
            uom_id=db.session.query(UOM).filter(UOM.symbol_code==symbol_code).all()
            for uid in uom_id:
                uomid.append(int(uid.uom_id))
        else :
            
            for code in symbol_code:
                if code :
                    print(code)
                    uom_id=db.session.query(UOM).filter(UOM.symbol_code==code).all()
                    for uid in uom_id:
                        uomid.append(int(uid.uom_id))
                else :
                    uomid.append(int(0))
        print(uomid)
        sellerid = []
        seller_asst = []
        inst_seller = isinstance(seller_name, list) 
        print(inst_seller)
        if not inst_seller :

            print("inside")
            seller_asst.append(seller_name)
            seller_id=db.session.query(Vendor).filter(Vendor.vendor_name==seller_name).all()
            for sid in seller_id:
                sellerid.append(int(sid.vendor_id))
        else :
            
            for code in seller_name:
                if code :
                    print(code)
                    seller_asst.append(code)
                    seller_id=db.session.query(Vendor).filter(Vendor.vendor_name==code).all()
                    for sid in seller_id:
                        sellerid.append(int(sid.vendor_id))
                else :
                    sellerid.append(int(0))
        print(sellerid)
        created_at = datetime.datetime.today()
        
        item_association = ItemAssociation(item_name = item_name,seller = seller_asst)
        item=Item(item_name = item_name, item_gst = item_gst, item_specification = item_specification, category_id = categoryid, uom = uomid,  created_at = created_at, vendor_name = sellerid)
        try:
            db.session.add(item)
            db.session.add(item_association)
            db.session.commit()
            print(item)
            return {str(item) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

@app.route('/add-category', methods=['POST'])
@cross_origin()
def category_insert():
    if request.method == "POST":
        print(request.get_json(force=True))
        parent_category = request.json['parent_category']
        category_name = request.json['category_name']
        #parent_category_code = request.json['parent_category_code']
        category_code = request.json['category_code']
        created_at = datetime.datetime.today()
        category=Category(parent_category = parent_category, category_name = category_name, category_code = category_code, created_at = created_at)
        try:
            db.session.add(category)
            db.session.commit()
            print(category)
            return {str(category) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

@app.route('/add-subcategory', methods=['POST'])
@cross_origin()
def subcategory_insert():
    if request.method == "POST":
        print(request.get_json(force=True))
        category_id = request.json['category_id']
        category_name = request.json['category_name']
        parent_category_code = request.json['parent_category_code']
        category_code = request.json['category_code']
        created_at = datetime.datetime.today()
        subcategory=Category(category_id = category_id, category_name = category_name, category_code = category_code, parent_category_code = parent_category_code, created_at = created_at)
        try:
            db.session.add(subcategory)
            db.session.commit()
            print(subcategory)
            return {str(subcategory) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

@app.route('/add-uom', methods=['POST'])
@cross_origin()
def uom_insert():
    if request.method == "POST":
        print(request.get_json(force=True))
        symbol_code = request.json['symbol_code']
        description = request.json['description']
        created_at = datetime.datetime.today()
        uom=UOM(symbol_code = symbol_code, description = description, created_at = created_at)
        try:
            db.session.add(uom)
            db.session.commit()
            print(uom)
            return {str(uom) : 'Added'} 
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

@app.route('/item/<itemid>', methods=['GET'])
@cross_origin()
def item_by_item_id(itemid=None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Item).filter(Item.item_id == itemid , Item.item_is_active == 'true').all()
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
                record_dict =  {'item_id' : record.item_id,'item_name' : record.item_name,'item_gst' : record.item_gst, 'item_specification' : record.item_specification, 'category_id' : record.category_id, 'sub_category' : record.sub_category, 'uom' : record.uom}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})

@app.route('/category/<categoryid>', methods=['GET'])
@cross_origin()
def category_by_cat_id(categoryid=None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Category).filter(Category.category_id == categoryid,Category.category_is_active == 'true').all()
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
                record_dict =  {'category_id' : record.category_id, 'category_name' : record.category_name, 'category_code' : record.category_code, 'parent_category_code' : record.parent_category_code}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})

@app.route('/items/category/<category>', methods=['GET'])
@cross_origin()
def item_by_category(category=None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Item).filter(Item.category_id == category, Item.item_is_active == 'true').all()
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
                record_dict =  {'category_id' : record.category_id, 'uom' : record.uom}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})

@app.route('/categories', methods=['GET'])
@cross_origin()
def category():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Category).filter(Category.category_is_active == 'true').all()
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
                record_dict =  {'category_id' : record.category_id, 'category_name' : record.category_name, 'category_code' : record.category_code, 'parent_category' : record.parent_category}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})

@app.route('/view-items', methods=['GET'])
@cross_origin()
def items():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Item).filter(Item.item_is_active == 'true').all()
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
                category_name=db.session.query(Category).filter(Category.category_id==record.category_id).all()
                if len(category_name) > 0:
                    categoryname = category_name[0].category_name
                else :
                    categoryname = "Not Assigned"
                sellername = []
                print(record.vendor_name)
                for vid in record.vendor_name:
                    print(vid)
                    seller_name=db.session.query(Vendor).filter(Vendor.vendor_id ==vid).all()
                   
                    for code in seller_name:
                        #if code.count() > 0:
                        print("i am here",code.vendor_name)
                        sellername.append(code.vendor_name)
                print(sellername)
                symbol_code_name = []
                for idv in record.uom:
                    symbol_code=db.session.query(UOM).filter(UOM.uom_id==idv).all()
                
                    for code in symbol_code:
                    #if code.count() > 0:
                        symbol_code_name.append(code.symbol_code)
                    #else :
                        #symbol_code= "Not Assigned"
                #selected_symbol_code = []
                #for idv in record.uom:
                #    new_Symbol = db.session.query(UOM.symbol_code).filter(UOM.uom_id==idv).all()
                #    print(new_Symbol)
                #    selected_symbol_code.extend(new_Symbol)
                record_dict =  {'item_id' : record.item_id, 'item_name' : record.item_name,'item_gst' : record.item_gst,'item_specification' : record.item_specification, 'item_description' : record.item_description, 'category_name' : categoryname, 'symbol_code' : symbol_code_name,  'seller_name' : sellername}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})

@app.route('/items-page/<pagee>/<per_pagee>', methods=['GET'])
@cross_origin()
def items_page(pagee=None,per_pagee=None):
    if request.method == "GET":
        try :
            page = int(pagee)
            per_page = int(per_pagee)
            ResultSett=db.session.query(Item).filter(Item.item_is_active == 'true').paginate(page = page, per_page = per_page, error_out = False)
            ResultSet = ResultSett.items
            ResultSettt=db.session.query(Item).all()
            total_records = len(ResultSettt)
            print(total_records)
            recordObject = {}
            data = []
            resp = {
                "per_page": per_page,
                "total": total_records,
                "total_pages": int(math.ceil(total_records/per_page))
            }
            for record in ResultSet:
                category_name=db.session.query(Category).filter(Category.category_id==record.category_id).all()
                if len(category_name) > 0:
                    categoryname = category_name[0].category_name
                else :
                    categoryname = "Not Assigned"
                sellername = []
                #print(record.vendor_name)
                for vid in record.vendor_name:
                    #print(vid)
                    seller_name=db.session.query(Vendor).filter(Vendor.vendor_id ==vid).all()
                   
                    for code in seller_name:
                        #if code.count() > 0:
                        #print("i am here",code.vendor_name)
                        sellername.append(code.vendor_name)
                #print(sellername)
                symbol_code_name = []
                for idv in record.uom:
                    symbol_code=db.session.query(UOM).filter(UOM.uom_id==idv).all()
                
                    for code in symbol_code:
                    #if code.count() > 0:
                        symbol_code_name.append(code.symbol_code)
                    #else :
                        #symbol_code= "Not Assigned"
                #selected_symbol_code = []
                #for idv in record.uom:
                #    new_Symbol = db.session.query(UOM.symbol_code).filter(UOM.uom_id==idv).all()
                #    print(new_Symbol)
                #    selected_symbol_code.extend(new_Symbol)
                record_dict =  {'item_id' : record.item_id, 'item_name' : record.item_name,'item_gst' : record.item_gst,'item_specification' : record.item_specification, 'item_description' : record.item_description, 'category_name' : categoryname, 'symbol_code' : symbol_code_name,  'seller_name' : sellername}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})


@app.route('/view-items-by-symbol-code', methods=['GET'])
@cross_origin()
def items_by_symbol_code():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Item).filter(Item.item_is_active == 'true').all()
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
                category_name=db.session.query(Category).filter(Category.category_id==record.category_id).all()
                if len(category_name) > 0:
                    categoryname = category_name[0].category_name
                else :
                    categoryname = "Not Assigned"
                seller_name=db.session.query(Association).filter(Association.category==categoryname).all()
                sellername = []
                for code in seller_name:
                    #if code.count() > 0:
                    print("i am here")
                    sellername.append(code.seller)
                symbol_code=db.session.query(UOM).all()
                symbol_code_name = []
                for code in symbol_code:
                    #if code.count() > 0:
                    symbol_code_name.append(code.symbol_code)
                    #else :
                        #symbol_code= "Not Assigned"
                
                record_dict =  {'item_id' : record.item_id, 'item_name' : record.item_name,'item_gst' : record.item_gst,'item_specification' : record.item_specification, 'item_description' : record.item_description, 'category_name' : categoryname, 'symbol_code' : symbol_code_name,  'seller_name' : sellername}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})

@app.route('/view-uom', methods=['GET'])
@cross_origin()
def view_uom():
    if request.method == "GET":
        try :
            ResultSet=db.session.query(UOM).all()
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
                record_dict =  {'uom_id' : record.uom_id, 'symbol_code' : record.symbol_code, 'description' : record.description}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})


@app.route('/items/subcategory/<subcategory>', methods=['GET'])
@cross_origin()
def item_by_subcategory(subcategory=None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Item).filter(Item.sub_category == subcategory, Item.item_is_active == 'true').all()
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
                record_dict =  {'sub_category' : record.sub_category}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})


@app.route('/sub-category/<categoryid>', methods=['GET'])
@cross_origin()
def subcategory_by_cat_id(categoryid=None):
    if request.method == "GET":
        try :
            ResultSet=db.session.query(Category).filter(Category.category_id == categoryid , Category.category_is_active == 'true').all()
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
                record_dict =  {'category_id' : record.category_id, 'category_name' : record.category_name}
                data.append(record_dict)

            resp['data'] = data
            return jsonify(resp)
        except exc.SQLAlchemyError as e  :
            return jsonify({'error':str(e)})

@app.route('/delete-category/<int:categoryid>', methods=['DELETE'])
@cross_origin()
def category_delete(categoryid):
    if request.method == "DELETE":
        #record = Category.query.filter(Category.category_id == categoryid).delete()
        category_is_active = 0
        ResultSet=db.session.query(Category).filter(Category.category_id == categoryid).update({'category_is_active' : category_is_active},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Deleted'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)
        
@app.route('/delete-item/<int:itemid>', methods=['DELETE'])
@cross_origin()
def item_delete(itemid):
    if request.method == "DELETE":
        item_is_active = 0
        ResultSet=db.session.query(Item).filter(Item.item_id == itemid).update({'item_is_active' : item_is_active},synchronize_session=False)
        try:
            db.session.commit()
            return {'Status' : 'Deleted'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)

@app.route('/delete-uom/<int:uomid>', methods=['DELETE'])
@cross_origin()
def item_uom(uomid):
    if request.method == "DELETE":
        record = UOM.query.filter(UOM.uom_id == uomid).delete()
        try:
            db.session.commit()
            return {'Status' : 'Deleted'}
        except exc.SQLAlchemyError as e  :
            print(e)
            db.session.rollback()
            return str(e)
