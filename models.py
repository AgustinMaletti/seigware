from app import db

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)

