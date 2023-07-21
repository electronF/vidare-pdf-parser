# 3rd party moudles
from flask import render_template

# Local modules
import configs

from webapi.controllers.document import Document


# Get the application instance
connex_app = configs.connexion_app


# Create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "inconstruction_page.html"
    """
    # document = Document()
    # print(document.read_all())
    return render_template("index.html")


# # Create a URL route in our application for "/people"
# @connex_app.route("/drivers")
# @connex_app.route("/drivers/<int:driver_id>")
# def people(driver_id=""):
#     """
#     This function just responds to the browser URL
#     localhost:5000/drivers
#     :return:        the rendered template "people.html"
#     """
#     return render_template("people.html", person_id=driver_id)


if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=5000, debug=True)