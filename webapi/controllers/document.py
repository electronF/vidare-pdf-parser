# Built-in modules
import os
from typing import Dict, List, Union, Any

# External modules
from flask import make_response, abort, jsonify

#Local modules
from configs import database, connexion_app
from constants import COVER_IMAGES_PATH, UPLOADED_DOCUMENTS_PATH

from webapi.models.document import Document, DocumentSchema 
from webapi.models.page import Page, PageSchema
from webapi.models.image import Image, ImageSchema
from webapi.modelsDTO.document import DocumentDTO

from webapi.services.delete_file import FileRemover


class DocumentController:
    '''
        This class provide functions to get, edit, update and delete a document.
    '''
    
    @classmethod
    def read_all(cls)->(Union[List[Dict[str, Any]], None]):
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

    @classmethod
    def read_all_obj(cls)->(Union[List[Dict[str, Any]], None]):
        """
        This function responds to a request for /api/document
        with the complete lists of documents.
        
        Args:\n
        Returns:
            (List[Dict] | None): json string of list of documents
        """
        # Create the list of documents
        documents = database.session.query(Document).order_by(Document.add_at).all()

        return documents

    @classmethod
    def read_one(cls, document_id:int)->(Union[Dict[str, Any], None]):
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
            return make_response( {'success':True, 'message':f"Document not found for Id: {document_id}"}, 404)

    @classmethod
    def create(cls, document:DocumentDTO):
        """
        This function save a new document in the list of documents
        
        Args:
            document(DocumentDTO): The document and its assets. 
            
        Returns:
            (Dict | None): 201 on success and the update document object, 
                406 if document is already exists.
        """
        title = ''
        for page in document.pages:
            temp_title = page['text'].strip()
            if len(title) > 5:
                title = temp_title[:100]
                break
        
        content = ''
        for page in document.pages:
            text = page['text'].strip()
            if len(text) > 50:
                content = page['text'][:500]
                break
        
        db_model_document = Document(
            name = document.name,
            title = title,
            type = document.type,
            short_content = content,
            cover_image_path = document.cover_image_path,
            author = '',
            path = document.path,
            publication_date = None,
        )
        
        for page in document.pages:
            page_obj = Page(
                number = page['number'],
                content = page['text'],
                path = page['path']
            )
            
            for image in page['images']:
                page_obj.images.append(
                    Image(
                    path = image['path'],
                    name = image['name'],
                    order = image['order']
                    )
                )
            db_model_document.pages.append(page_obj)
            
        # Does the document could be inserted?
        try:
            # Add the document to the database
            database.session.add(db_model_document)
            database.session.commit()
            
            # Uncomment the two nexts lines of code if the id of insterted data
            # is not automatically add to the instance
            
            # database.session.flush()
            # database.session.refresh(db_model_document)
            
            # Create a document instance using the schema
            schema = DocumentSchema()
            # new_document = schema.load(db_model_document, session=database.session)

            # Serialize and return the newly created document in the response
            data = schema.dump(db_model_document)
            data['code'] = 201
            data['success'] = True
            return  data
        
        except Exception as error:
            # Otherwise, nope, document exists already
            # abort(409, f"Document {document.name} exists already")
            connexion_app.logger.error(error)
            return {
                'success': False,
                'message': 'Something happens wrong on server', 
                'code': 409
            }

    @classmethod
    def update(cls, document_id:int, document:Dict[str, Union[int, str, Dict]]):
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
            return make_response(f"Document not found for Id: {document_id}", 404)

    @classmethod
    def delete(cls, document_id:int):
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
            
            # document_path = os.path.join(UPLOADED_DOCUMENTS_PATH, '{}.{}'.format(document.name, document.type))
            removed_message = FileRemover.remove_file_and_folder(UPLOADED_DOCUMENTS_PATH, document.name)
            must_be_delete = removed_message == None
            error_message = '' if removed_message==None else removed_message
            if document.cover_image_path != None and document.cover_image_path.split() != '':
                cover_image_path  = os.path.join(COVER_IMAGES_PATH, document.cover_image_path)
                removed_message = FileRemover.remove_file(cover_image_path)
                must_be_delete = must_be_delete and removed_message == None
                error_message = error_message + ('' if removed_message==None else ('\n'+removed_message))
            
            if must_be_delete:    
                database.session.delete(document)
                database.session.commit()
                return {
                        'success': True,
                        'message':f"Document with Id {document_id} has been deleted",
                        'code': 201
                    } 
            else:
                return {
                        'success': False,
                        'message':f"Something happend wrong on server. {error_message}",
                        'code': 500
                    } 
        else:
            return {
                    'success':False, 
                    'message':f"Document not found for Id: {document_id}", 
                    'code': 404
                }
            