function deleteTask(id, elemento) {
    document.getElementById(id).style.color = "red";
    var req = new XMLHttpRequest()
    req.onreadystatechange = function(){
        if (req.readyState == 4){
            if (req.status != 200){
                //error handling code here
            }
            else{
                 elemento.parentElement.removeChild(elemento);// se borra del dom si se ha borrado del servidor
                var response = JSON.parse(req.responseText)
                document.getElementById("tasks").innerHTML = response.tasks
            }
        }
    }
    req.open('POST', '/ajax')
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    var postVars = "task="+document.getElementById(id).cells[0].innerHTML
    req.send(postVars)
    return false
}