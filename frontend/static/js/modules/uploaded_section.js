import UploadedItem from "../components/uploaded_item.js";

import getFile from "../hooks/getfile.js";
import deleteFile from "../hooks/deletefile.js";
import { GET_DOCUMENT, DELETE_DOCUMENT } from "../constants.js";


class UploadedSection {
  uploadedItems = $("#uploaded-files");
  addItem(itemDescriptiom) {
    var uploadedItem = $(
      new UploadedItem(
        itemDescriptiom["title"] ?? "",
        itemDescriptiom["path"],
        itemDescriptiom["short_content"],
        itemDescriptiom["type"],
        itemDescriptiom["add_at"], //(new Date()).toISOString()
        itemDescriptiom["cover_image_path"]
      ).render()
    );
    this.uploadedItems.append(uploadedItem);

    var button = uploadedItem.find("button.preview");
    try {
        $(button).on('click', function(){
            alert('preview')
        })
    } catch (error) {}
    
    var button = uploadedItem.find("button.delete");
    try {
        $(button).on('click', async function(){
            var response  = await deleteFile(itemDescriptiom['id'], DELETE_DOCUMENT)
            if(response['success'] === true)
            {
                uploadedItem.remove()
            }
        })
    } catch (error) {}

    
  }

  clear() {
    this.uploadedItems.empty();
  }
}

export default UploadedSection;
