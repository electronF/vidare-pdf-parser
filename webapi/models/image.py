# Built-in modules

# External modules
from sqlalchemy import (
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.sql.sqltypes import NullType


from sqlalchemy.orm import (
    mapped_column
)

from marshmallow_sqlalchemy import auto_field

#Local modules
from configs import database, marsmallow


class Image(database.Model):
    __tablename__ = "images"
    id = mapped_column(Integer, primary_key=True)
    path = mapped_column(String,)
    name = mapped_column(String,)
    page_id = mapped_column(ForeignKey("pages.id"))
    order = mapped_column(Integer)
    

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
        include_fk = True
        load_instance = True #Optional: deserialize to model instance