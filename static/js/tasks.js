function deleteTask(elemento) {
    var req = new XMLHttpRequest()
    req.onreadystatechange = function(){
        if (req.readyState == 4){
            if (req.status != 200){
                //error handling code here
            }
            else{
				var fila = document.getElementById(elemento.parentElement.parentElement.id);
				fila.parentNode.removeChild(fila);
				 
                var response = JSON.parse(req.responseText)
                document.getElementById("tasks").innerHTML = response.tasks
            }
        }
    }
    req.open('POST', '/ajaxDeleteTask')
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    var postVars = "task="+elemento.parentElement.parentElement.cells[0].innerHTML
    req.send(postVars)
    return false
}

//function detectCell(id, elemento){
//    if (id.split('-')[1] == 'borrar'){
//        document.getElementById(id).style.color = "red";
//    }
//    if (id.split('-')[1] == 'editar'){
//        document.getElementById(id).style.color = "green";
//    }
//}