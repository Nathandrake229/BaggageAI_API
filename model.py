from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime
db = SQLAlchemy()

        
class bag_bnd_box( db.Model):
    __tablename__ = 'bag_bndbox'

    id = db.Column(db.Integer, primary_key = True)
    xmn = db.Column(db.Integer)
    ymn = db.Column(db.Integer)
    xmx = db.Column(db.Integer)
    ymx = db.Column(db.Integer)
    obj_name = db.Column(db.String(100))
    img_name = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    # define your model

    def __init__(self, xmn, ymn, xmx, ymx,obj_name,img_name,date ):
        self.xmn = xmn
        self.ymn = ymn
        self.xmx = xmx
        self.ymx = ymx
        self.obj_name = obj_name
        self.img_name = img_name
        self.date = date

    def __repr__(self):
        return f"<Image {self.img_name}>"