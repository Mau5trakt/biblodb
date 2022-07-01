

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

    let libros_tr = document.getElementById("libros")

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

function aprobar(e){
    console.log(e.target);
    if(e.target.nodeName == "TD"){
        let linea = e.target.parentNode;
        let id = linea.dataset.id;


        let http = new XMLHttpRequest();
        let url = "/aprobar-prestamo";

        let datos = new FormData();
        datos.append("q", id);

        http.open("POST", url);
        http.send(datos);

        http.onreadystatechange = function(){
            if(http.readyState == 4){
                if(http.status == 200){
                    let datos = http.responseText;

                    swal.fire({
                        "title": "Llega",
                        "html": datos,
                        "showConfirmButton:": false,
                    });
                }
            }
        }





    }
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

function solicitar_domicilio(isbn, id_libro){
    console.log(isbn);
    console.log(id_libro);
    let datos  =  new FormData();
    datos.append("isbn", isbn)
    datos.append("id_libro", id_libro)

    let url = "/solicitud_domicilio"; //Poner la ruta en python de prestar

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

function solicitar_sala(isbn, id_libro){
    console.log(isbn);
    console.log(id_libro);
    let datos  =  new FormData();
    datos.append("isbn", isbn)
    datos.append("id_libro", id_libro)

    let url = "/solicitud-sala"; //Poner la ruta en python de prestar

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



function aprobar_prestamo(id_prestamo){
    console.log("Entras?")
    let datos  =  new FormData();
    datos.append("q", id_prestamo)

    let url = "/prestamo-aprobado";

    let http = new XMLHttpRequest();
    http.open("POST", url);

    http.send(datos)

    http.onreadystatechange = function ()  {
        if(this.readyState == 4){
            if(this.status == 200){
                Swal.fire(this.responseText)
                location.reload()
            }
            else if(this.status != 500){
                Swal.fire(this.responseText)
            }
        }
    }
}

function denegar(id_prestamo){
    console.log("Denegar")
    let datos  =  new FormData();
    datos.append("q", id_prestamo)

    let url = "/denegar-prestamo";

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