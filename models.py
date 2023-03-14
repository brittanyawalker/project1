
from . import db

class Property(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    proptitle = db.Column(db.String(100))
    description = db.Column(db.Text())
    room = db.Column(db.String(10))
    bathroom = db.Column(db.String(10))
    propprice = db.Column(db.String(30))
    proptype = db.Column(db.String(20))
    location = db.Column(db.String(200), unique=False)
    picture = db.Column(db.String())

    def __init__(self, proptitle, description, room, bathroom, propprice, proptype, location, picture):
        self.proptitle = proptitle
        self.description = description
        self.room = room
        self.bathroom = bathroom
        self.propprice = propprice
        self.proptype = proptype
        self.location = location
        self.picture = picture

    def __repr__(self):
        return '<Property %r>' % (self.title)