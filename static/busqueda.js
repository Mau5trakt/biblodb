

function actualizar_listas(consulta){
    let datos = new FormData();
    datos.append("q", consulta);

    let http = new XMLHttpRequest();
    let url = "/libros-resultados";

    http.open("POST", url);
    http.send(datos);

    http.onreadystatechange = function(){
        if(http.readyState == 4 && http.status == 200){

            let respuesta = JSON.parse(http.responseText);
            let lista = document.getElementById("lista_libros");
            lista.innerHTML = "";

            for(let i = 0; i < respuesta.length; i++){
                let elemento = document.createElement("option");
                elemento.textContent = respuesta[i].titulo ;
                elemento.value = respuesta[i].titulo;
                lista.appendChild(elemento);
            }

        }
    }


}

function buscar_libros(formulario){
    console.log("aaaaaaaaaaaaaaaaaaaaaa");
    let datos = new FormData(formulario);

    let http = new XMLHttpRequest();
    let url = "/busqueda";

    http.open("POST", url);
    http.send(datos);

    http.onreadystatechange = function(){
        if(http.readyState == 4 && http.status == 200){
            let contenedor = document.getElementById("listado");
            contenedor.innerHTML = http.responseText;

            let libros_tr = document.getElementById("libros");

            libros_tr.addEventListener("click", info_libro);
            return false;
        }
    }
    return false;
}

function info_libro(e){
    console.log(e.target);
    if(e.target.nodeName == "TD"){
        let linea = e.target.parentNode;
        let id = linea.dataset.id;


        let http = new XMLHttpRequest();
        let url = "/libros-info";

        let datos = new FormData();
        datos.append("q", id);

        http.open("POST", url);
        http.send(datos);

        http.onreadystatechange = function(){
            if(http.readyState == 4){
                if(http.status == 200){
                    let datos = http.responseText;

                    swal.fire({
                        "title": "Información del libro",
                        "html": datos,
                        "showConfirmButton:": false,
                    });
                }
            }
        }





    }
}

function solicitar_domicilio(isbn){
    console.log(isbn);

    let datos  =  new FormData();
    datos.append("isbn", isbn)

    let url = "/solicitud_domicilio";

    let http = new XMLHttpRequest();
    http.open("POST", url);

    http.send(datos)

    http.onreadystatechange = function ()  {
        if(this.readyState == 4){
            if(this.status == 200){
                Swal.fire(this.responseText)
            }
            else if(this.status != 500){
                Swal.fire(this.responseText)
            }
        }
    }
}

