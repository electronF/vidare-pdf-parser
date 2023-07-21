# Built-in modules

# External modules
from sqlalchemy import (
    Column, Integer,
    String, ForeignKey
)

from sqlalchemy.orm import (
    relationship, backref
)

from marshmallow_sqlalchemy import auto_field

#Local modules
from configs import database, marsmallow

from image import Image


class Page(database.Model):
    __tablename__ = "pages"
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    content = Column(String)
    document_id = Column(Integer, ForeignKey("documents.id"))
    
    images = relationship(
        "Image", 
        backref=backref("pages"),
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Image.order)"
    )
    

    def __repr__(self) -> str:
        return """Page(id={}, number={}, content='{}', document_id={}, images='{} images included')""".format(
            self.id,
            self.number, 
            self.content[:10]+ ('...' if self.content else ''), 
            self.document_id,
            len(self.images)
        )


class PageSchema(marsmallow.SQLAlchemySchema):
    class Meta:
        model = Page
        load_instance = True #Optional: deserialize to model instance
    id = auto_field()
    number = auto_field()
    content = auto_field()
    document_id = auto_field()
    images = auto_field()