# Built-in modules
from datetime import datetime

# External modules
from sqlalchemy import (
    Integer,
    String, 
    DateTime
)

from sqlalchemy.orm import (
    mapped_column,
    relationship, 
    backref
)

from marshmallow_sqlalchemy import auto_field

#Local modules
from configs import database, marsmallow

from webapi.models.page import Page


class Document(database.Model):
    __tablename__ = "documents"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)
    title = mapped_column(String, default='')
    short_content = mapped_column(String)
    author = mapped_column(String, default=None)
    path = mapped_column(String, nullable=False)
    type = mapped_column(String, default='pdf')
    cover_image_path = mapped_column(String, nullable=True)
    publication_date = mapped_column(DateTime)
    add_at = mapped_column(
                        DateTime, 
                        default=datetime.utcnow, 
                        onupdate=datetime.utcnow
                )
    
    pages = relationship(
        "Page", 
        backref=backref("documents"),
        # primaryjoin="and_(foreign(Document.id)==Page.document_id)",/
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Page.number)"
    )
    
    def __repr__(self) -> str:
        return """Document(id={}, name='{}', title='{}', short_content='{}' author='{}', path='{}', type='{}' cover_image_path='{}' publication_date='{}', add_at='{}', pages='{} pages in the document')""".format(
            self.id,
            self.name, 
            self.title, 
            self.short_content,
            self.author, 
            self.path,
            self.type,
            self.cover_image_path,
            self.publication_date,
            self.add_at,
            len([] if self.pages==None else self.pages)
        )


class DocumentSchema(marsmallow.SQLAlchemySchema):
    class Meta:
        model = Document
        load_instance = True
    id = auto_field()
    name = auto_field()
    title = auto_field()
    short_content = auto_field()
    author = auto_field()
    path = auto_field()
    type = auto_field()
    cover_image_path = auto_field()
    publication_date = auto_field()
    add_at = auto_field()
    pages = auto_field()

