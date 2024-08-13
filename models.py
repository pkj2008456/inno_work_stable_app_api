from db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID  # 使用 UUID 类型

class User(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    images = db.relationship('Image', backref='user', cascade='all, delete-orphan')
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True ,default = "public")
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id'), nullable=False)  # 使用 UUID 类型
    image_url = db.Column(db.String(200), nullable=False)

   
