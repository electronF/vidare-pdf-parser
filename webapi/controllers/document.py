# Built-in modules
from typing import Dict, List, Union, Any

# External modules
from flask import make_response, abort

#Local modules
from configs import database

from webapi.models.document import Document, DocumentSchema 
from webapi.models.page import Page, PageSchema
from webapi.models.image import Image, ImageSchema


class Document:
    '''
        This class provide functions to get, edit, update and delete a document.
    '''
    
    
    def read_all(self)->(Union[List[Dict[str, Any]], None]):
        """
        This function responds to a request for /api/document
        with the complete lists of documents.
        
        Args:\n
        Returns:
            (List[Dict] | None): json string of list of documents
        """
        # Create the list of documents
        documents = database.session.query(Document).order_by(Document.add_at).all()

        # Serialize the data for the response
        document_schema = DocumentSchema(many=True)
        data = document_schema.dump(documents)
        return data


    def read_one(self, document_id:int)->(Union[Dict[str, Any], None]):
        """
        This function responds to a request for /api/document/{id}
        with one matching document from the list of documents.
        
        Args:
            document_id(int): The id of the needed document.
        Returns:
            (Dict[str, object] | None): The document and its assets.
        """
        # Build the initial query
        document = (
            Document.query.filter(Document.id == document_id)
            .outerjoin(Page)
            .one_or_none()
        )

        # Did we find a document?
        if document is not None:

            # Serialize the data for the response
            document_schema = DocumentSchema()
            data = document_schema.dump(document)
            return data

        # Otherwise, nope, didn't find that document
        else:
            abort(404, f"Document not found for Id: {document_id}")


    def create(self, document:Dict[str, Union[int, str, List[Dict]]]):
        """
        This function save a new document in the list of documents
        
        Args:
            document (Dict[str, int | str | Dict]): The document and its assets. 
        Returns:
            (Dict | None): 201 on success and the update document object, 
                406 if document is already exists.
        """
        name = document.get("name", None).lower()
        title = document.get("title", None)

        existing_document = (
            Document.query.filter(Document.name == name)
            .filter(Document.title == title)
            .one_or_none()
        )

        # Does the document could be inserted?
        if existing_document is None:

            # Create a document instance using the schema
            schema = DocumentSchema()
            new_document = schema.load(document, session=database.session)

            # Add the document to the database
            database.session.add(new_document)
            database.session.commit()

            # Serialize and return the newly created document in the response
            data = schema.dump(document)

            return make_response(data, 201)

        # Otherwise, nope, document exists already
        else:
            abort(409, f"Document {name} with title {title} exists already")


    def update(self, document_id:int, document:Dict[str, Union[int, str, Dict]]):
        """
        This function updates an existing document in the list of documents.
        
        Args:
            document_id(int):   The id of the document to update
            document(Dict[str, int | str | Dict]): 
                The document with the information to update
        Returns:
            (Dict | None): 201 on success and the update document object,
                404 if is not found.
        """
        # Get the document requested 
        existing_document = Document.query.filter(
            Document.id == document_id
        ).one_or_none()

        # Update the document if it exists?
        if existing_document is not None:
            schema = DocumentSchema()
            update = schema.load(document, session=database.session)

            # Set the id to the document to update
            update.id = existing_document.id

            # merge the new object with the old one and save to the database
            database.session.merge(update)
            database.session.commit()

            # return updated document in the response
            data = schema.dump(update)

            return make_response(data, 200)

        # Otherwise, nope, didn't find that document
        else:
            abort(404, f"Document not found for Id: {document_id}")


    def delete(self, document_id:int):
        """
            This function deletes a document in the list of documents
            
            Args:
                document_id(int):  The id of the document to delete
            Returns:
                (Dict): 200 on successful delete, 404 if not found
        """
        # Get the document requested
        document = Document.query.filter(Document.id == document_id).one_or_none()

        # Delete the document if its exists
        if document is not None:
            database.session.delete(document)
            database.session.commit()
            return make_response(f"Document with Id {document_id} has been deleted", 200)

        # Otherwise, nope, didn't find that document
        else:
            abort(404, f"Document not found for Id: {document_id}")
            