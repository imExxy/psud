from app import db

class Power(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    powerUnit = db.Column(db.String(64))
    power = db.Column(db.Float)

    def __repr__(self):
        return 'Power Stamp: {} {} {} kvt*ch'.format(self.date, self.powerUnit, self.power)

