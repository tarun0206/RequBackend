from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import config

#UPLOAD_FOLDER = "D:\downloaded_videos"
UPLOAD_FOLDER = "/attachments"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = config()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
per_page = 6

from modules.client.routes import client_module
from modules.item.routes import item_module
from modules.employee.routes import employee_module
from modules.vendor.routes import vendor_module
from modules.org.routes import org_module
from modules.rate_comparative.routes import rate_comparative_module
from modules.requisition.routes import requisition_module
from modules.po.routes import po_module
from modules.grn.routes import grn_module
app.register_blueprint(client.routes.client_module, url_prefix = '/')
app.register_blueprint(item.routes.item_module, url_prefix = '/')
app.register_blueprint(employee.routes.employee_module, url_prefix = '/')
app.register_blueprint(vendor.routes.vendor_module, url_prefix = '/')
app.register_blueprint(org.routes.org_module, url_prefix = '/')
app.register_blueprint(rate_comparative.routes.rate_comparative_module, url_prefix = '/')
app.register_blueprint(requisition.routes.requisition_module, url_prefix = '/')
app.register_blueprint(po.routes.po_module, url_prefix = '/')
app.register_blueprint(grn.routes.grn_module, url_prefix = '/')
