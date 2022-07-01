from modules import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import psycopg2


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True ,autoincrement=True)
    client_name = db.Column(db.String, nullable=True, unique=True)
    #client_contact = db.Column(db.BIGINT, nullable=True)
    payment_terms = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    client_email = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=True)
    client_terms_and_condition = db.Column(db.String, nullable=True) 
    contact_person = db.Column(db.String, nullable=True) 
    site_id = db.Column(db.Integer , db.ForeignKey('site.id') , nullable=True)
    created_by = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    update_by = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    update_at = db.Column(db.DateTime, nullable=True)
    client_attachment = db.Column(db.LargeBinary, nullable=True)
    cl10 = db.Column(db.String, nullable=True)
    cl11 = db.Column(db.String, nullable=True)
    cl12 = db.Column(db.String, nullable=True)
    cl13 = db.Column(db.String, nullable=True)
    cl14 = db.Column(db.String, nullable=True)

class Site(db.Model):
    __tablename__ = 'site'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    site_name = db.Column(db.String, nullable=True, unique=True)
    location = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.BIGINT, nullable=True)
    contact_person = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    cost_center = db.Column(db.String, nullable=True)
    project_director_id = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    project_manager_id = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    store_keeper_id = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    client_name = db.Column(db.String , nullable=True)
    created_by = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    update_by = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    update_at = db.Column(db.DateTime, nullable=True)
    #ref_requisition = db.relationship('Requisition', backref='ref_site_name', lazy = 'dynamic' , foreign_keys = 'Requisition.req_site')
    client_ref = db.relationship('Client', backref='reference_client_ref', lazy = 'dynamic' , foreign_keys = 'Client.site_id')
    si16 = db.Column(db.String, nullable=True)
    si17 = db.Column(db.String, nullable=True)
    si18 = db.Column(db.String, nullable=True)
    si19 = db.Column(db.String, nullable=True)
    si20 = db.Column(db.String, nullable=True)
    

class Employee(db.Model):
    __tablename__= 'employee'
    employee_id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String)
    employee_email = db.Column(db.String, unique=True)
    employee_contact = db.Column(db.BIGINT)
    employee_designation = db.Column(db.String)
    created_by = db.Column(db.String , nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    update_by = db.Column(db.String, nullable=True)
    update_at = db.Column(db.DateTime, nullable=True)
    contact_person = db.relationship('Site', backref='site_contact_person', lazy = 'dynamic' , foreign_keys = 'Site.contact_person')
    #client_contact_person = db.relationship('Client', backref='reference_client_contact_person', lazy = 'dynamic' , foreign_keys = 'Client.contact_person')
    project_director_id = db.relationship('Site', backref='site_project_director_id', lazy = 'dynamic' , foreign_keys = 'Site.project_director_id')
    project_manager_id = db.relationship('Site', backref='site_project_manager_id', lazy = 'dynamic' , foreign_keys = 'Site.project_manager_id')
    store_keeper_id = db.relationship('Site', backref='site_store_keeper_id', lazy = 'dynamic' , foreign_keys = 'Site.store_keeper_id')
    client_created_by = db.relationship('Client', backref='client_created_by', lazy = 'dynamic' , foreign_keys = 'Client.created_by')
    client_update_by = db.relationship('Client', backref='client_update_by', lazy = 'dynamic' , foreign_keys = 'Client.update_by')
    site_created_by = db.relationship('Site', backref='site_created_by', lazy = 'dynamic' , foreign_keys = 'Site.created_by')
    site_update_by = db.relationship('Site', backref='site_update_by', lazy = 'dynamic' , foreign_keys = 'Site.update_by')
    rc_action_by = db.relationship('RateComparative', backref='ratecomparative_action_by', lazy = 'dynamic' , foreign_keys = 'RateComparative.action_by')
    rc_action_to = db.relationship('RateComparative', backref='ratecomparative_action_to', lazy = 'dynamic' , foreign_keys = 'RateComparative.action_to')
    rc_update_by = db.relationship('RateComparative', backref='ratecomparative_update_by', lazy = 'dynamic' , foreign_keys = 'RateComparative.update_by')
    ref_org_contact_person_id = db.relationship('Org', backref='ref_org_contact_person_id', lazy = 'dynamic' , foreign_keys = 'Org.org_contact_person_id')
    ratecomparative_created_by = db.relationship('RateComparative', backref='ratecomparative_created_by', lazy = 'dynamic' , foreign_keys = 'RateComparative.created_by')
    user_permission = db.Column(db.JSON, nullable=True)
    emp_sites = db.Column(db.JSON, nullable=True)
    employee_is_active = db.Column(db.Boolean, server_default='t', default=True)
    emp18 = db.Column(db.String(500), nullable=True)
    emp19 = db.Column(db.String, nullable=True)
    emp20 = db.Column(db.String, nullable=True)
    emp21 = db.Column(db.String, nullable=True)


class Category(db.Model):
    __tablename__= 'category'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String , nullable=True, unique=True)
    category_code = db.Column(db.String , nullable=False, unique=True)
    parent_category = db.Column(db.String , nullable=True)
    parent_category_code = db.Column(db.String , nullable=True)
    category_description = db.Column(db.String , nullable=True)
    item_ref = db.relationship('Item', backref='item_ref', lazy = 'dynamic' , foreign_keys = 'Item.category_id')
    sub_category_ref = db.relationship('Item', backref='sub_category_ref', lazy = 'dynamic' , foreign_keys = 'Item.category_id')
    created_at = db.Column(db.DateTime, nullable=True)
    #ref_req_category = db.relationship('Requisition', backref='reference_category', lazy = 'dynamic' , foreign_keys = 'Requisition.req_category')
    #req_sub_category = db.relationship('Requisition', backref='reference_sub_category', lazy = 'dynamic' , foreign_keys = 'Requisition.req_sub_category')
    category_is_active = db.Column(db.Boolean, server_default='t', default=True)
    cat07 = db.Column(db.String, nullable=True)
    cat08 = db.Column(db.String, nullable=True)
    cat09 = db.Column(db.String, nullable=True)
    cat10 = db.Column(db.String, nullable=True)
    cat11 = db.Column(db.String, nullable=True)


class Item(db.Model):
    __tablename__= 'item'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String , nullable=True, unique=True)
    item_gst = db.Column(db.String , nullable=True)
    item_specification = db.Column(db.String , nullable=True)
    item_description = db.Column(db.String , nullable=True)
    category_id = db.Column(db.Integer , db.ForeignKey('category.category_id') , nullable=True)
    sub_category = db.Column(db.Integer , db.ForeignKey('category.category_id') , nullable=True)
    uom = db.Column(db.ARRAY(Integer), nullable=True)
    vendor_name = db.Column(db.ARRAY(Integer), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    #req_item = db.relationship('Requisition', backref='reference_req_item', lazy = 'dynamic' , foreign_keys = 'Requisition.req_item')
    item_is_active = db.Column(db.Boolean, server_default='t', default=True)
    it09 = db.Column(db.String, nullable=True)
    it10 = db.Column(db.String, nullable=True)
    it11 = db.Column(db.String, nullable=True)
    it12 = db.Column(db.String, nullable=True)
    it13 = db.Column(db.String, nullable=True)

class ItemAssociation(db.Model):
    __tablename__='itemassociation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String, nullable=True)
    seller = db.Column(db.ARRAY(String), nullable=True)

class UOM(db.Model):
    __tablename__ = 'uom'
    uom_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol_code = db.Column(db.String , nullable=True, unique=True)
    category_id = db.Column(db.Integer , db.ForeignKey('category.category_id') , nullable=True)
    uom_name = db.Column(db.String , nullable=True)
    messurement = db.Column(db.String , nullable=True)
    description = db.Column(db.String , nullable=True)
    #req_uom = db.relationship('Requisition', backref='reference_req_uom', lazy = 'dynamic' , foreign_keys = 'Requisition.req_uom')
    created_at = db.Column(db.DateTime, nullable=True)
    uom06 = db.Column(db.String, nullable=True)
    uom07 = db.Column(db.String, nullable=True)
    uom08 = db.Column(db.String, nullable=True)
    uom09 = db.Column(db.String, nullable=True)
    uom10 = db.Column(db.String, nullable=True)
'''
class Requisition(db.Model):
    __tablename__='requisition'
    req_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    req_title  = db.Column(db.String, nullable=True)	
    req_site = db.Column(db.Integer , db.ForeignKey('site.id') , nullable=True)	
    req_created_at = db.Column(db.DateTime, nullable=True)
    req_rejectondate = db.Column(db.DateTime, nullable=True)
    req_approvedate = db.Column(db.DateTime, nullable=True)
    req_urgent_requirement = db.Column(db.String, nullable=True)
    req_local_purchase = db.Column(db.String, nullable=True)
    req_quantity = db.Column(db.String, nullable=True)
    req_intended_end_use = db.Column(db.String, nullable=True)
    req_item = db.Column(db.Integer , db.ForeignKey('item.item_id') , nullable=True)
    req_category = db.Column(db.Integer , db.ForeignKey('category.category_id') , nullable=True)
    req_sub_category = db.Column(db.Integer , db.ForeignKey('category.category_id') , nullable=True)
    req_uom = db.Column(db.Integer , db.ForeignKey('uom.uom_id') , nullable=True)
    req_version = db.Column(db.Integer , db.ForeignKey('history.history_id') , nullable=True)
    req_attachment = db.Column(db.LargeBinary, nullable=True)
    histroy_req_id = db.relationship('History', backref='ref_histroy_req_id', lazy = 'dynamic' , foreign_keys = 'History.histroy_req_id')
    history_qty = db.relationship('History', backref='ref_history_qty', lazy = 'dynamic' , foreign_keys = 'History.history_qty')
    rq17 = db.Column(db.String, nullable=True)
    rq18 = db.Column(db.String, nullable=True)
    rq19 = db.Column(db.String, nullable=True)
    rq20 = db.Column(db.String, nullable=True)
    rq21 = db.Column(db.String, nullable=True)
    rq22 = db.Column(db.String, nullable=True)

class Requisition(db.Model):
    __tablename__='requisition'
    req_id = db.Column(db.Integer, primary_key=True, autoincrement=True) #unique
    req_title  = db.Column(db.String, nullable = True) #required
    req_site = db.Column(db.Integer , db.ForeignKey('site.id'), nullable = True)	#required
    # workflow_status = db.Column(db.Integer , db.ForeignKey('approvalWorkflow.workflow_id') , nullable=True)	
    #req_created_at = db.Column(db.DateTime, nullable=True) #required
    req_urgent_requirement = db.Column(db.Boolean, nullable=True) #required
    req_local_purchase = db.Column(db.Boolean, nullable=True)    #required
    #req_version = db.Column(db.Integer , db.ForeignKey('history.history_id') , nullable=True) #required
    #history_qty = db.relationship('History', backref='ref_history_qty', lazy = 'dynamic' , foreign_keys = 'History.history_qty')
    remarks = db.Column(db.String, nullable=True) 
    created_by = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    update_by = db.Column(db.Integer , db.ForeignKey('employee.employee_id') ) # As discussed by Satish
    update_at = db.Column(db.DateTime, nullable=True)
    req_attachment = db.Column(db.LargeBinary, nullable=True)
    req_status = db.Column(db.String, nullable=True) 
    req_item = db.Column(db.Integer , db.ForeignKey('item.item_id') , nullable=True)
    req_uom = db.Column(db.Integer , db.ForeignKey('uom.uom_id') , nullable=True)
    #req_attachment = db.Column(db.LargeBinary, nullable=True)
    req_category = db.Column(db.Integer , db.ForeignKey('category.category_id') , nullable=True)
    req_sub_category = db.Column(db.Integer , db.ForeignKey('category.category_id') , nullable=True)
    req_intended_end_use = db.Column(db.String, nullable=True)
    req_quantity = db.Column(db.Float, nullable=True)   '''

class Requisition(db.Model):
    _tablename_='requisition'
    req_id = db.Column(db.Integer, primary_key=True, autoincrement=True) #unique
    req_title  = db.Column(db.String, nullable = True) #required
    req_site = db.Column(db.Integer , db.ForeignKey('site.id'), nullable = True)	#require
    req_urgent_requirement = db.Column(db.Boolean, nullable=True) #required
    req_local_purchase = db.Column(db.Boolean, nullable=True)    #required
    created_by = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    updated_by = db.Column(db.Integer , db.ForeignKey('employee.employee_id') ) # As discussed by Satish
    updated_at = db.Column(db.DateTime, nullable=True)
    req_attachment = db.Column(db.LargeBinary, nullable=True)
    req_status = db.Column(db.String, nullable=True) 
    req_item_list = db.Column(db.JSON, nullable=True)
    action_by = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    action_to = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    req_version = db.Column(db.Integer, nullable=True)
    req_remarks = db.Column(db.String, nullable=True)
    req01 = db.Column(db.Integer, nullable=True)
    req02 = db.Column(db.Integer, nullable=True)
    req03 = db.Column(db.Integer, nullable=True)
    req04 = db.Column(db.String, nullable=True)
    req05 = db.Column(db.String, nullable=True)
    req06 = db.Column(db.String, nullable=True)
    #update_at = db.Column(db.DateTime, nullable=True)


class RequisitionItemAssociation(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    req_quantity = db.Column(db.Float, nullable=True)
    req_intended_end_use = db.Column(db.String, nullable=True)
    req_item = db.Column(db.Integer , db.ForeignKey('item.item_id') , nullable=True)
    req_id = db.Column(db.Integer , db.ForeignKey('requisition.req_id') , nullable=True)
    req_uom = db.Column(db.Integer , db.ForeignKey('uom.uom_id') , nullable=True)
    req_attachment = db.Column(db.LargeBinary, nullable=True)
    req_category = db.Column(db.Integer , db.ForeignKey('category.category_id') , nullable=True)
    req_sub_category = db.Column(db.Integer , db.ForeignKey('category.category_id') , nullable=True)
    
    

class History(db.Model):
    __tablename__='history'
    history_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #histroy_req_id = db.Column(db.Integer, nullable=True)# , db.ForeignKey('requisition.req_id') , nullable=True)
    #history_qty = db.Column(db.Integer , db.ForeignKey('requisition.req_id') , nullable=True)
    history_req_id = db.Column(db.String, nullable=True)
    history_rc_id = db.Column(db.String, nullable=True)
    history_user = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    history_req = db.Column(db.JSON, nullable=True)	
    history_rc = db.Column(db.JSON, nullable=True)
    history_status = db.Column(db.String, nullable=True)
    history_reject = db.Column(db.String, nullable=True)
    history_revise = db.Column(db.String, nullable=True)  
    hsitory_approve = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    #ref_req_version = db.relationship('Requisition', backref='reference_req_version', lazy = 'dynamic' , foreign_keys = 'Requisition.req_version')
    hi13 = db.Column(db.String, nullable=True)
    hi14 = db.Column(db.String, nullable=True)
    hi15 = db.Column(db.String, nullable=True)
    hi16 = db.Column(db.String, nullable=True)
    hi17 = db.Column(db.String, nullable=True)
    hi18 = db.Column(db.String, nullable=True)

class Vendor(db.Model):
    _tablename_='vendor'
    vendor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vendor_name = db.Column(db.String, nullable=True, unique=True)
    vendor_type = db.Column(db.String, nullable=True)
    vendor_category = db.Column(db.Integer, db.ForeignKey('category.category_id') , nullable=True)
    category_name = db.Column(db.ARRAY(String), nullable=True)
    vendor_contact_person = db.Column(db.String, nullable=True)
    vendor_phone_number = db.Column(db.BIGINT, nullable=True)
    vendor_email = db.Column(db.String, nullable=True)
    vendor_address = db.Column(db.String, nullable=True)
    vendor_payment_terms = db.Column(db.String, nullable=True)
    vendor_terms_and_conditions = db.Column(db.String, nullable=True)
    vendor_attachment = db.Column(db.String, nullable=True)
    vendor_01 = db.Column(db.String, nullable=True)
    vendor_02 = db.Column(db.String, nullable=True)
    vendor_03 = db.Column(db.Integer, nullable=True)

class Org(db.Model):
    _tablename_='org'
    org_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    org_location = db.Column(db.String, nullable=True, unique=True)
    org_contact_person_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id') , nullable=True)
    org_designation = db.Column(db.String, nullable=True)
    org_phone_number = db.Column(db.BIGINT, nullable=True)
    org_email = db.Column(db.String, nullable=True)
    org_address = db.Column(db.String, nullable=True)
    org_attachment = db.Column(db.LargeBinary, nullable=True)
    org_01 = db.Column(db.String, nullable=True)
    org_02 = db.Column(db.String, nullable=True)
    org_03 = db.Column(db.String, nullable=True)
    org_04 = db.Column(db.Integer, nullable=True)
    org_05 = db.Column(db.Integer, nullable=True)

class Association(db.Model):
    __tablename__='association'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String, nullable=True)
    seller = db.Column(db.String, nullable=True)

class RateComparative(db.Model):
    __tablename__='ratecomparative'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rate_comp_requisition_id = db.Column(db.String, nullable=True)
    rate_comp_requisition_title = db.Column(db.String, nullable=True)
    rate_comp_urgent_requirement = db.Column(db.String, nullable=True)
    rate_comp_local_purchase = db.Column(db.String, nullable=True)
    rate_comp_site_name = db.Column(db.String, nullable=True)
    rate_comp_request_date = db.Column(db.DateTime, nullable=True)
    rate_comp_vendors_list = db.Column(db.JSON, nullable=True)
    rate_comp_total = db.Column(db.JSON, nullable=True)
    rate_comp_status = db.Column(db.String, nullable=True)
    action_by = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    action_to = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    rate_comp_version = db.Column(db.Integer, nullable=True)
    created_by = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    created_at = db.Column(db.DateTime, nullable=True)
    update_by = db.Column(db.Integer , db.ForeignKey('employee.employee_id') , nullable=True)
    update_at = db.Column(db.DateTime, nullable=True)
    ratecomp_1 = db.Column(db.String, nullable=True)
    ratecomp_2 = db.Column(db.String, nullable=True)
    ratecomp_3 = db.Column(db.String, nullable=True)
    ratecomp_4 = db.Column(db.String, nullable=True)
    ratecomp_5 = db.Column(db.String, nullable=True)
    

class PO(db.Model):
    __tablename__='po'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #po_delivery_address = db.Column(db.String, nullable=True) #site_address
    #po_billing_address = db.Column(db.String, nullable=True)    
    po_vendor_name = db.Column(db.String, nullable=True)#making_req_id
    #po_total_price = db.Column(db.String, nullable=True)
    #po_freight = db.Column(db.String, nullable=True)
    #po_freight_gst = db.Column(db.String, nullable=True)
    #po_amount = db.Column(db.String, nullable=True)
    po_status = db.Column(db.String, nullable=True)
    po_org = db.Column(db.Integer , db.ForeignKey('org.org_id') , nullable=True)
    po_site = db.Column(db.Integer , db.ForeignKey('site.id') , nullable=True)
    po_vendor = db.Column(db.Integer , db.ForeignKey('vendor.vendor_id') , nullable=True)
    po_rate_comparative = db.Column(db.Integer , db.ForeignKey('ratecomparative.id') , nullable=True)
    po_client = db.Column(db.Integer , db.ForeignKey('client.id') , nullable=True)
    po_vendor_json = db.Column(db.JSON, nullable=True)
    po_site_no = db.Column(db.String, nullable=True)
    po8 = db.Column(db.String, nullable=True)#to
    po3 = db.Column(db.String, nullable=True)#from
    po4 = db.Column(db.String, nullable=True)#content
    po5 = db.Column(db.String, nullable=True)#po_number
    po6 = db.Column(db.String, nullable=True)#po_t&c
    po7 = db.Column(db.String, nullable=True)#payment_terms
    po8 = db.Column(db.String, nullable=True)
    po9 = db.Column(db.String, nullable=True)


class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    
class TransferOut(db.Model):
    __tablename__='transferout'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    to_title = db.Column(db.String, nullable=True)
    to_sending_site = db.Column(db.String, nullable=True)
    to_receiving_site = db.Column(db.String, nullable=True)
    to_id = db.Column(db.String, nullable=True)
    to_date = db.Column(db.String, nullable=True)
    to_vehicle_no = db.Column(db.DateTime, nullable=True)
    to_item_list = db.Column(db.JSON, nullable=True)
    to_1 = db.Column(db.String, nullable=True)
    to_2 = db.Column(db.String, nullable=True)
    to_3 = db.Column(db.String, nullable=True)
    to_4 = db.Column(db.String, nullable=True)
    to_5 = db.Column(db.String, nullable=True)
    to_7 = db.Column(db.JSON, nullable=True)
    to_8 = db.Column(db.JSON, nullable=True)
    to_9 = db.Column(db.JSON, nullable=True)
    to_10 = db.Column(db.String, nullable=True)
    to_11 = db.Column(db.Integer, nullable=True)
    to_12 = db.Column(db.Integer, nullable=True)
    to_13 = db.Column(db.Integer, nullable=True)
    to_14 = db.Column(db.Integer, nullable=True)
    to_15 = db.Column(db.Integer, nullable=True)