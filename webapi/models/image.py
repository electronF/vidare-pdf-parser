# Built-in modules

# External modules
from sqlalchemy import (
    Column, Integer,
    String, ForeignKey
)

from marshmallow_sqlalchemy import auto_field

#Local modules
from configs import database, marsmallow


class Image(database.Model):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    path = Column(String)
    name = Column(String)
    page_id = Column(Integer, ForeignKey("pages.id"))
    order = Column(Integer)
    

    def __repr__(self) -> str:
        return """Image(id={}, name='{}', path='{}', page={}, order={})""".format(
            self.id,
            self.name, 
            self.path, 
            self.page, 
            self.order
        )


class ImageSchema(marsmallow.SQLAlchemySchema):
    class Meta:
        model = Image
        load_instance = True #Optional: deserialize to model instance
    id = auto_field()
    name = auto_field()
    path = auto_field()
    page_id = auto_field()
    order = auto_field()