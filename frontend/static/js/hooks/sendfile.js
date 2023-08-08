
async function saveFile(file, path, endpoint) {
  let formData = new FormData();
  formData.append("file", file);
  formData.append("path", path);

  const ctrl = new AbortController(); // timeout
  setTimeout(() => ctrl.abort(), 500000);

  try {
    let response = await fetch(endpoint, {
      method: "POST",
      body: formData,
      signal: ctrl.signal,
      // "Content-type": "multipart/form-data; charset=UTF-8"
    });
    return await response.json();
  } catch (e) {
    return {
      success: false,
      message: `An error occured while uploading the file ${path}. ${e}`,
    };
  }
}

export default saveFile;