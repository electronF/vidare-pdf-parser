import getFiles from "./hooks/getfiles.js"
import { GET_DOCUMENTS } from "./constants.js"

import UploadedSection from "./modules/uploaded_section.js"
import UploadingSection from "./modules/uploading_section.js"

async function getAndAddDocument(){
    var uploadedSection = new UploadedSection()
    var response = await getFiles(GET_DOCUMENTS)
    if(response['success'] === true)
    {
        uploadedSection.clear()
        for(var document of response['data'])
        {
            uploadedSection.addItem(document)
        }
    }
}

function listenUploadingSectionEvents()
{
    var uploadingSection = (new UploadingSection())
    uploadingSection.listen()
}

function listenUploadedSectionEvents()
{
    $('#refresh-uploaded-items').on('click', async function(){
        await getAndAddDocument()
    })
}

function listenDocumentEvents()
{
    $(document).ready(function(){
        getAndAddDocument()
    })
}

listenUploadedSectionEvents()
listenUploadingSectionEvents()
listenDocumentEvents()