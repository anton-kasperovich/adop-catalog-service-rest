# -*- coding: utf-8 -*-
from app import db

class Extensions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url  = db.Column(db.String(255), index=True)
    description  = db.Column(db.String(255), index=True)

    def __init__(self, url='', description=''):
        self.url = url
        self.description = description

    def __repr__(self):
        return '<Extensions%d>' % self.id

class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sdk_version = db.Column(db.String(255))
    name  = db.Column(db.String(255), index=True)
    type = db.Column(db.String(255))
    description = db.Column(db.String(255))
    image = db.Column(db.String(255))
    source_url = db.Column(db.String(255))

    def __init__(self, sdk_version='', name='',type='',description='',image='',source_url=''):
        self.sdk_version = sdk_version
        self.name = name
        self.type = type
        self.description = description
        self.image = image
        self.source_url = source_url

    def __repr__(self):
        return '<Metadata%d>' % self.id

class Install(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    app_id  = db.Column(db.String(255), index=True)
    name  = db.Column(db.String(255), index=True)
    source_url = db.Column(db.String(255))
    status = db.Column(db.String(255))
    error = db.Column(db.String(255))

    def __init__(self, app_id='', name ='', source_url ='', status ='', error=''):
        self.app_id = app_id
        self.name = name
        self.source_url = source_url
        self.status = status
        self.error = error

    def __repr__(self):
        return '<Install%d>' % self.id

