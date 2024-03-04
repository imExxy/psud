from app import db

class RealEstate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    author_type = db.Column(db.String(64))
    link = db.Column(db.String(100))
    city = db.Column(db.String(64))
    deal_type = db.Column(db.String(64))
    accommodation_type = db.Column(db.String(64))
    floor = db.Column(db.Integer)
    floors_count = db.Column(db.Integer)
    rooms_count = db.Column(db.Integer)
    total_meters = db.Column(db.Float)
    price_per_m2 = db.Column(db.Integer)
    price_per_month = db.Column(db.Integer)
    commissions = db.Column(db.Integer)
    district = db.Column(db.String(64))
    street = db.Column(db.String(64))
    house_number = db.Column(db.String(64))
    underground = db.Column(db.String(64))

    def __repr__(self):
      return 'Output: {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(self.author, self.author_type, self.link,
      self.city, self.deal_type, self.accommodation_type, self.floor, self.floors_count, self.rooms_count, self.total_meters,
      self.price_per_m2, self.price_per_month, self.commissions, self.district, self.street, self.house_number, self.underground)