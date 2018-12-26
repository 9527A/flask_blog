from app import db
ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_username=db.Column(db.String(60), index=True, unique=True)
    db_passworld = db.Column(db.String(120), index=True)
    db_email = db.Column(db.String(120))
    db_phone = db.Column(db.String(20))
    db_intro = db.Column(db.String(600)) 
    # role = db.Column(db.SmallInteger, default=ROLE_USER)

    def __repr__(self):
        return '<User %r>' % self.nickname

class comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    db_username = db.Column(db.String(60))
    db_title = db.Column(db.String(100))
    db_comments = db.Column(db.String(600))
    