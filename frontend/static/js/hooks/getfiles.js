async function getFiles(endpoint) 
{
    const ctrl = new AbortController()    // timeout
    setTimeout(() => ctrl.abort(), 500000);
    
    try {
       let r = await fetch(
         new URL(endpoint), 
         {
            method: "GET", 
            signal: ctrl.signal,
            "Content-type": "application/json; charset=UTF-8"
        }); 
       console.log('HTTP response code:',r.status); 
    } catch(e) {
       console.log('Huston we have problem...:', e);
    }
}