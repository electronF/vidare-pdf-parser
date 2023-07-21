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
    name = mapped_column(String)
    title = mapped_column(String)
    author = mapped_column(String)
    path = mapped_column(String)
    publication_date = mapped_column(DateTime)
    
    add_at = mapped_column(
                        DateTime, 
                        default=datetime.utcnow, 
                        onupdate=datetime.utcnow
                )
    
    pages = relationship(
        "Document", 
        backref=backref("documents"),
        primaryjoin="and_(foreign(Document.id)==Page.document_id)",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Page.number)"
    )
    
    def __repr__(self) -> str:
        return """Document(id={}, name='{}', title='{}', author='{}', path='{}', publication_date='{}', add_at='{}', pages='{} pages in the document')""".format(
            self.id,
            self.name, 
            self.title, 
            self.author, 
            self.path,
            self.publication_date,
            self.add_at,
            len(self.pages)
        )


class DocumentSchema(marsmallow.SQLAlchemySchema):
    class Meta:
        model = Document
        include_fk = True
        load_instance = True


