import UploadingItem from "../components/uploading_item.js";
import saveFile from "../hooks/sendfile.js";
import { fileVerificator, fileSize, fileName } from "../utils/function.js";
import { POST_DOCUMENT } from "../constants.js";
import UploadedSection from "./uploaded_section.js";

class UploadingSection {

  allowedTypes = [
            'application/pdf', 
            'application/vnd.oasis.opendocument.text', 
            'application/vnd.ms-powerpoint', 
            'application/vnd.openxmlformats-officedocument.presentationml.presentation'
  ]
  constructor() {
    this.uploadedSection = new UploadedSection();
  }

  async uploadFile(file, path, uploadingItem) {
    var response = await saveFile(file, path, POST_DOCUMENT);
    if (response["success"] === false) {
      alert(response["message"]);
    } else {
      uploadingItem.remove();
      this.uploadedSection.addItem(response);
    }
  }

  fileSaver = (files, paths) => {
    var uploadedItems = $("#uploading-items");
    var count = 0;
    for (var file of files) {
      var message = fileVerificator(file);
      if (message === null) {
        count++;
        var uploadingItem = $(
          new UploadingItem(
            count,
            fileName(file.name),
            `${fileSize(file.size)}`,
            file.type.split("/")[1]
          ).render()
        );
        uploadedItems.append(uploadingItem);
        this.uploadFile(file, paths[count - 1] ?? file.name, uploadingItem);
      } else {
        alert(message);
      }
    }
  };

  #evenListenner() {
    $("div.upload-section .browse-button").on("click", () => {
      var inputFiles = $(`<input 
                type='file' 
                accept='
                    ${this.allowedTypes.join(',')}
                    ' 
                multiple 
            />`);
      inputFiles.click();
      inputFiles[0].onchange = ()=> this.fileSaver(
        inputFiles[0].files,
        inputFiles[0].value.split(";")
      );
    });

    $("#upload-section").on("drop", (event) => {
      event.preventDefault();

      var droppedFiles = event.originalEvent.dataTransfer.files;
      var paths = [];
      var allowedFiles = [];

      for (var file of droppedFiles) {
        if(this.allowedTypes.includes(file.type))
        {
            paths.push(file.name);
            allowedFiles.push(file)
        }
      }
      this.fileSaver(allowedFiles, paths);
    });

    $("#upload-section").on(
      "dragover dragenter dragover dragleave",
      function (event) {
        event.preventDefault();
      }
    );
  }

  listen() {
    this.#evenListenner();
  }
}

export default UploadingSection;
