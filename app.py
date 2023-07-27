#built-in module
import os

# 3rd party moudles
from flask import render_template, jsonify, request

# Local modules
import configs
import constants
import utils.filemanager as filemanager

from webapi.modelsDTO.document import DocumentDTO
from webapi.controllers.document import DocumentController
from webapi.services.readpdf import PdfParser


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
    
    return render_template("dashboard.html")



# Create a URL route in our application for "/api/document/"
@connex_app.route("/api/document/", methods=['GET'])
def get_documents():
    """
    This function just responds to the browser URL
    localhost:5000/api/document/
    
    Args:
    Returns:
        (JSON): A list of dict as list of files
    """
    return jsonify(DocumentController.read_all())

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
    uploaded_info = ""
    failed_info = ""
    # request.form.get()
    response = {}
    for file_key in  request.files:
        file_obj = request.files[file_key]
        new_name = filemanager.save_file(file_obj, constants.UPLOADED_FILES)
        if new_name != None:
            filename, _ = os.path.splitext(new_name)
            
            #Create folder to save files
            output_dir = os.path.join(constants.UPLOADED_FILES, filename)
            os.makedirs(output_dir)
            
            # Extract information in PDF and save then. The get all the information to use
            parser = PdfParser(os.path.join(constants.UPLOADED_FILES, new_name), output_dir)
            pages = parser.get_content()
            document = DocumentDTO(name=filename, path='', pages=pages)
            response = DocumentController.create(document)
            
            uploaded_info += f'mimetype:{file_obj.mimetype} uploaded_name:{file_obj.filename}, new_name:{new_name}\n'
        else:
            failed_info +=  f'mimetype:{file_obj.mimetype} uploaded_name:{file_obj.filename}\n'
    
    return jsonify(response)


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