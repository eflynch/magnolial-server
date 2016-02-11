from magnolial import db

class MagnolialUser(db.Base):
    __tablename__ = 'magnolialuser'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    passhash = db.Column(db.String(255))

    def __init__(self, username, passhash):
        self.username = username
        self.passhash = passhash

    def __repr__(self):
        return '<MagnolialUser %s>' % self.username

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return self.username

    def isAdmin(self):
        return True

class Magnolial(db.Base):
    __tablename__ = 'magnolial'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('magnolialuser.id'))
    user = db.relationship(MagnolialUser)
    filename = db.Column(db.Text)
    content = db.Column(db.Text)

    def __init__(self, user, filename, content):
        self.filename = filename
        self.content = content
        self.user = user

    def toJSON(self):
        return self.content
