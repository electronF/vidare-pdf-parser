async function deleteFile(id, endpoint) {
    const ctrl = new AbortController(); // timeout
    setTimeout(() => ctrl.abort(), 500000);
  
    try {
      let response = await fetch(endpoint+'/'+id, {
        method: "DELETE",
        signal: ctrl.signal,
        "Content-type": "application/json; charset=UTF-8",
      });
      return await response.json();
    } catch (e) {
      return {
        success: false,
        message: `An error occured while getting the file: ${e}`,
      };
    }
  }
  
  export default deleteFile;