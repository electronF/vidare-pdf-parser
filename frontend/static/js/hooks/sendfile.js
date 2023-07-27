
async function saveFile(file, path, endpoint) 
{
    let formData = new FormData();
    formData.append("file", file);
    formData.append('path', path)

    const ctrl = new AbortController()    // timeout
    setTimeout(() => ctrl.abort(), 500000);
    
    try {
       let r = await fetch(
         new URL(endpoint), 
         {
            method: "POST", 
            body: formData, 
            signal: ctrl.signal,
            "Content-type": "multipart/form-data; charset=UTF-8"
        }); 
       console.log('HTTP response code:',r.status); 
    } catch(e) {
       console.log('Huston we have problem...:', e);
    }
}

export default saveFile