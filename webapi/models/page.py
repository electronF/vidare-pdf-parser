# Built-in modules

# External modules
from sqlalchemy import (
    Integer,
    String, 
    ForeignKey
)

from sqlalchemy.orm import (
    mapped_column,
    relationship, 
    backref
)

from marshmallow_sqlalchemy import auto_field

#Local modules
from configs import database, marsmallow

from webapi.models.image import Image


class Page(database.Model):
    __tablename__ = "pages"
    id = mapped_column(Integer, primary_key=True)
    number = mapped_column(Integer)
    content = mapped_column(String)
    path = mapped_column(String)
    document_id = mapped_column(ForeignKey("documents.id"))
    
    images = relationship(
        "Image", 
        backref=backref("pages"),
        primaryjoin="and_(foreign(Page.id)==Image.page_id)",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Image.order)"
    )
    

    def __repr__(self) -> str:
        return """Page(id={}, number={}, content='{}', path='{}', document_id={}, images='{} images included')""".format(
            self.id,
            self.number, 
            self.content[:10]+ ('...' if self.content else ''), 
            self.path,
            self.document_id,
            len(self.images)
        )


class PageSchema(marsmallow.SQLAlchemySchema):
    class Meta:
        model = Page
        include_fk = True
        load_instance = True
    