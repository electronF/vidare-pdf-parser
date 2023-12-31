#built-in module
import os

# 3rd party moudles
from flask import (
    render_template, 
    jsonify, 
    request,
    make_response
)

# Local modules
import configs
import constants
import utils.filemanager as filemanager

from webapi.modelsDTO.document import DocumentDTO
from webapi.controllers.document import DocumentController
from webapi.services.readpdf import PDFParser
from webapi.services.pdfconverter import PDF2ImageConverter
from webapi.services.file_verificator import FileVerificator


# Get the application instance
connex_app = configs.connexion_app
connex_app.app_context().push()


@connex_app.before_first_request
def init():
    from webapi.models.document import Document
    from webapi.models.page import Page
    from webapi.models.image import Image
    configs.database.create_all()

# Create a URL route in our application for "/"
@connex_app.route('/', defaults={'path': ''})
@connex_app.route('/<path:path>')
def home(path:str):
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "inconstruction_page.html"
    """
    documents = DocumentController.read_all()
    return render_template("dashboard.html", documents=documents)



# Create a URL route in our application for "/api/document/"
@connex_app.route("/api/document/", methods=['GET'])
def get_documents():
    """
    This function just responds to the browser URL
    localhost:5000/api/document/ to get the list of 
    documents
    
    Args:
    Returns:
        (JSON): A list of dict as list of document
    """
    try:
        return make_response(
            jsonify({
                'success': True,
                'data':DocumentController.read_all()
            }),
            201
        )
    except Exception as error:
        connex_app.logger('info', error)
        return make_response (
            jsonify({
                'success': False,
                'message': 'something happen wrong on server'
            }),
            500
        )


# Create a URL route in our application for "/api/document/"
@connex_app.route("/api/document/", methods=['POST'])
def create_document():
    """
        This function just responds to the browser URL
        localhost:5000/api/document/<file:dict>
        Args:
            file(JSON): A file description
        Returns:
            Uploading percentage
    """
    uploaded_info = []
    failed_info = []
    
    if (
        request.files.get('file', None) != None 
        and request.form.get('path', None) != None
        and FileVerificator.is_file_in_allowed_type(request.files['file'].filename)
        ):
        file_obj = request.files['file']
        file_path = request.form.get('path')
        new_name = filemanager.save_file(
            file_obj, 
            constants.UPLOADED_DOCUMENTS_PATH)
        
        if new_name != None:
            filename, _ = os.path.splitext(new_name)
            
            #Create folder to save files
            output_dir = os.path.join(constants.UPLOADED_DOCUMENTS_PATH, filename)
            os.makedirs(output_dir)
            
            # Extract information in PDF and save then. The get all the information to use
            parser = PDFParser(
                os.path.join(constants.UPLOADED_DOCUMENTS_PATH, new_name), 
                output_dir)
            
            pages = parser.get_content()
            # first_page_path = parser.split_first_page()
            
            cover_image_path = PDF2ImageConverter(
                        os.path.join(constants.UPLOADED_DOCUMENTS_PATH, new_name), 
                        constants.COVER_IMAGES_PATH
                    ).convert_first_page()
            
            response = DocumentController.create(
                DocumentDTO(
                    name=filename,
                    path=file_path,
                    pages=pages,
                    type=FileVerificator.get_type(new_name).upper(),
                    cover_image_path=cover_image_path
                )
            )
            
            code = response.pop('code', 201)
            return make_response(jsonify(response), code)
        else:
            connex_app.logger.error(
                'Filename error', 
                'The filename is None or no file name has been found'
            )
            return make_response(
                jsonify({
                    'success':False,  
                    'message':'Something happens wrong on saver with filename.'
                }),
                500,
            )
    elif (FileVerificator.is_file_in_allowed_type(request.files['file'].filename)):
        return make_response(
            jsonify({
                'success':False,  
                'message':'The file type is not allwed.'
            }),
            401
        )
    #Add file size checker here
    
    else:
        return make_response(
            jsonify({
                'success':False,  
                'message':'Something happens wrong on saver with filename.'
            }),
            500
        )

# Create a URL route in our application for "/api/document/"
@connex_app.route("/api/document/<int:document_id>", methods=['DELETE'])
def document(document_id:int):
    """
    This function just responds to the browser URL
    localhost:5000/document/image/<image:str>
    
    Args:
        image_id(str): The id of the image to get
    Returns:
        (JSON): The success indicator and the image as base64
    """
    response = DocumentController.delete(document_id)
    code = response.pop('code')
    connex_app.logger.info('error', str(response))
    return make_response(jsonify(response), code)


# Create a URL route in our application for "/api/document/"
# @connex_app.route("/api/document/", methods=['GET'])
# def document():
#     """
#     This function just responds to the browser URL
#     localhost:5000/drivers
#     :return:        the rendered template "people.html"
#     """
#     return render_template("people.html", person_id=driver_id)



if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=5000, debug=True)