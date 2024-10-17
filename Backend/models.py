from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)    
    password = db.Column(db.String(200), nullable=False)
    walletAddress = db.Column(db.String(50), nullable=False)
    startdate = db.Column(db.Date, nullable=True) 
    enddate = db.Column(db.Date, nullable=True)    
    cycles = db.Column(db.Integer, nullable=True)   

    def calculate_cycles(self):
        if self.startdate and self.enddate:
            months_diff = (self.enddate.year - self.startdate.year) * 12 + self.enddate.month - self.startdate.month
            self.cycles = months_diff
        elif self.startdate and not self.enddate:
            self.cycles = -1


# user.calculate_cycles()
