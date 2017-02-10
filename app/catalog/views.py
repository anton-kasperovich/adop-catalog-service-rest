# -*- coding: utf-8 -*-
import urllib, json, string, requests, os
from requests.auth import HTTPBasicAuth
from flask import Blueprint
from app import db, manager, admin
from app.catalog.models import Extensions, Metadata, Install
from flask.ext.admin.contrib.sqla import ModelView

catalog = Blueprint('catalog', __name__)

def pre_get_catalog(**kw):
    url = "https://raw.githubusercontent.com/anton-kasperovich/adop-catalog/master/catalog.json"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    #print data
    Extensions.query.delete()
    Metadata.query.delete()
    for extensions, subdict in data.iteritems():
        #print subdict
	for urls in subdict:
            #print urls
            url = ""
            description = ""
            for k, v in urls.iteritems():
                if k == "url":
                    url = v
                if k == "description":
                    description = v
            #print url, " : ", description
            extension_rec = Extensions(url, description)
            db.session.add(extension_rec)
            db.session.commit()
            # Get metadata and save in Metadata table
            modified_url = string.replace(url, 'github.com', 'raw.githubusercontent.com') + "/master/extension.metadata"
            #print modified_url
            response = urllib.urlopen(modified_url)
            sdk_version,name,type,description,image,source_url = "","","","","",""
            for line in response:
                params = line.rstrip().split("=")
                if params[0] == "PLATFORM_EXTENSION_SDK_VERSION":
                    sdk_version = params[1]
                if params[0] == "PLATFORM_EXTENSION_NAME":
                    name = params[1]
                if params[0] == "PLATFORM_EXTENSION_TYPE":
                    type = params[1]
                if params[0] == "PLATFORM_EXTENSION_DESCRIPTION":
                    description = params[1]
                if params[0] == "PLATFORM_EXTENSION_IMAGE":
                    image = params[1]
                if params[0] == "PLATFORM_EXTENSION_SOURCE_URL":
                    source_url = params[1]
            metadata_rec = Metadata(sdk_version,name,type,description,image,source_url)
            db.session.add(metadata_rec)
            db.session.commit()
    pass

def pre_get_installapp(instance_id=None,**kw):
    #print instance_id
    Install.query.delete()
    app = Metadata.query.filter_by(id=instance_id).first_or_404()
    #print app.source_url
    url = "http://jenkins:8080/jenkins/job/Platform_Management/job/Load_Platform_Extension/buildWithParameters?GIT_URL=" + app.source_url + "&AWS_CREDENTIALS=adop-ldap-admin"
    #print url
    #print os.environ
    #print os.environ.get('INITIAL_ADMIN_USER')
    #print os.environ.get('INITIAL_ADMIN_PASSWORD')
    r = requests.post(url, auth=HTTPBasicAuth(os.environ.get('INITIAL_ADMIN_USER'), os.environ.get('INITIAL_ADMIN_PASSWORD')))
    #install_rec = Install(instance_id, app.name, app.source_url)
    install_rec = Install(instance_id, app.name, app.source_url, r.status_code, r.reason)
    db.session.add(install_rec)
    db.session.commit()
    pass

manager.create_api(Extensions, methods=['GET', 'POST', 'DELETE'], preprocessors={'GET_SINGLE': [pre_get_catalog],'GET_MANY': [pre_get_catalog]}, results_per_page=None)
manager.create_api(Metadata, methods=['GET', 'POST', 'DELETE'], results_per_page=None)
manager.create_api(Install, methods=['GET', 'POST', 'DELETE'], preprocessors={'GET_SINGLE': [pre_get_installapp],'GET_MANY': [pre_get_installapp]}, results_per_page=None)

admin.add_view(ModelView(Extensions, db.session))
admin.add_view(ModelView(Metadata, db.session))
admin.add_view(ModelView(Install, db.session))

