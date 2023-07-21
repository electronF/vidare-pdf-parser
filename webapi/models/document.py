# Built-in modules
from datetime import datetime

# External modules
from sqlalchemy import (
    Column, Integer,
    String, DateTime
)

from sqlalchemy.orm import (
    relationship, backref
)

from marshmallow_sqlalchemy import auto_field

#Local modules
from configs import database, marsmallow

from page import Page


class Document(database.Model):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    title = Column(String)
    author = Column(String)
    publication_date = Column(DateTime)
    add_at = Column(
                        DateTime, 
                        default=datetime.utcnow, 
                        onupdate=datetime.utcnow
                )
    
    pages = relationship(
        "Document", 
        backref=backref("documents"),
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Page.number)"
    )
    
    def __repr__(self) -> str:
        return """Document(id={}, name='{}', title='{}', author='{}', publication_date='{}', add_at='{}', pages='{} pages in the document')""".format(
            self.id,
            self.name, 
            self.title, 
            self.author, 
            self.publication_date,
            self.add_at,
            len(self.pages)
        )


class DocumentSchema(marsmallow.SQLAlchemySchema):
    class Meta:
        model = Document
        load_instance = True #Optional: deserialize to model instance
    id = auto_field()
    name = auto_field()
    title = auto_field()
    author = auto_field()
    publication_date = auto_field()
    add_at = auto_field()
    pages = auto_field()