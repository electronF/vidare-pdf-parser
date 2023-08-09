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

async function saveFileWithCallback(
  file,
  path,
  endpoint,
  responseFunction,
  progressFunction
) {
  let formData = new FormData();
  formData.append("file", file);
  formData.append("path", path);

  const ctrl = new AbortController(); // timeout
  setTimeout(() => ctrl.abort(), 500000);

  let request = new XMLHttpRequest();
  request.open("POST", endpoint);

  // upload progress event
  request.upload.addEventListener("progress", function (e) {
    // upload progress as percentage
    let percent_completed = (e.loaded / e.total) * 100;
    // console.log(percent_completed);
    progressFunction(percent_completed);
  });

  // request finished event
  request.addEventListener("load", function (e) {
    // console.log(e);
    // HTTP status message (200, 404 etc)
    // console.log(request.status);

    // request.response holds response from the server
    // console.log(JSON.parse(request.response));

    progressFunction(100.00)
    responseFunction(JSON.parse(request.response))
  });

  // send POST request to server
  request.send(formData);
}

export { saveFile, saveFileWithCallback };
