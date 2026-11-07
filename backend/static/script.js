const tipoAnalisis = document.getElementById("tipo-analisis");
const contenido = document.getElementById("contenido");
const botonAnalizar = document.getElementById("boton-analizar");
const mensaje = document.getElementById("mensaje");

const resultado = document.getElementById("resultado");
const nivelRiesgo = document.getElementById("nivel-riesgo");
const resumenRiesgo = document.getElementById("resumen-riesgo");
const listaIndicios = document.getElementById("lista-indicios");
const seccionIndicios = document.getElementById("seccion-indicios");
const listaRecomendaciones =
    document.getElementById("lista-recomendaciones");

const seccionRecomendaciones =
    document.getElementById("seccion-recomendaciones");

botonAnalizar.addEventListener("click", async function () {
    const tipo = tipoAnalisis.value;
    const texto = contenido.value.trim();

    resultado.hidden = true;
    seccionRecomendaciones.hidden = true;
    listaRecomendaciones.replaceChildren();
    mensaje.textContent = "";

    // Limpiar las clases de los mensajes anteriores.
    mensaje.classList.remove("mensaje-error", "mensaje-progreso");

    if (texto === "") {
        mensaje.textContent =
            "Introduce el contenido que quieres analizar.";

        mensaje.classList.add("mensaje-error");
        contenido.focus();
        return;
    }

    // Comprobar que la URL tiene un formato válido.
    if (tipo === "url") {
        try {
            // Añadir HTTPS si el usuario no indica un protocolo.
            let urlTexto = texto;

            if (!/^https?:\/\//i.test(urlTexto)) {
                urlTexto = "https://" + urlTexto;
            }

            const direccion = new URL(urlTexto);

            if (
                !["http:", "https:"].includes(direccion.protocol) ||
                !direccion.hostname ||
                !direccion.hostname.includes(".")
            ) {
                throw new Error("URL no válida");
            }
        } catch {
            mensaje.textContent =
                "Introduce una dirección web válida.";

            mensaje.classList.add("mensaje-error");
            contenido.focus();
            return;
        }
    }

    botonAnalizar.disabled = true;
    mensaje.textContent = "Analizando contenido...";
    mensaje.classList.add("mensaje-progreso");

    try {
        const respuesta = await fetch("/analizar", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                tipo: tipo,
                contenido: texto
            })
        });

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(
                datos.error || "No se ha podido analizar el contenido."
            );
        }

        // Traducción de los niveles de riesgo.
        const nombresRiesgo = {
            bajo: "Bajo",
            medio: "Medio",
            alto: "Alto"
        };

        // Explicaciones generales para cada nivel.
        const descripciones = {
            bajo:
                "No se han encontrado suficientes señales de riesgo. " +
                "Esto no garantiza que el contenido sea seguro.",

            medio:
                "El contenido presenta señales que conviene revisar " +
                "antes de actuar.",

            alto:
                "Se han identificado señales sospechosas. Verifica " +
                "el remitente antes de responder, abrir enlaces " +
                "o compartir datos."
        };

        const nivel = datos.nivel_riesgo;

        // Mostrar el nivel de riesgo sin puntuaciones numéricas.
        nivelRiesgo.textContent =
            "Nivel de riesgo: " +
            (nombresRiesgo[nivel] || "No determinado");

        // Mostrar una explicación adaptada al resultado de la IA.
        if (nivel === "bajo" && datos.clasificacion_ia) {
            resumenRiesgo.textContent =
                "El modelo no ha identificado suficientes patrones " +
                "sospechosos. Esto no garantiza que el mensaje sea seguro.";
        } else {
            resumenRiesgo.textContent =
                descripciones[nivel] ||
                "No se ha podido determinar el nivel de riesgo.";
        }

        // Aplicar las clases correspondientes al nivel de riesgo.
        resultado.className = "resultado";

        if (["bajo", "medio", "alto"].includes(nivel)) {
            resultado.classList.add(nivel);
        }

        // Limpiar los indicios del análisis anterior.
        listaIndicios.replaceChildren();

        // Comprobar si hay indicios que mostrar.
        const hayIndicios =
            Array.isArray(datos.indicios) &&
            datos.indicios.length > 0;

        // Mostrar los indicios solo si existen (riesgo medio o alto).
        if (hayIndicios) {
            datos.indicios.forEach(function (indicio) {
                const elemento = document.createElement("li");
                elemento.textContent = indicio;
                listaIndicios.appendChild(elemento);
            });

            seccionIndicios.hidden = false;
        } else {
            seccionIndicios.hidden = true;
        }

        // Mostrar las recomendaciones preventivas.
        listaRecomendaciones.replaceChildren();

        if (
            Array.isArray(datos.recomendaciones) &&
            datos.recomendaciones.length > 0
        ) {
            datos.recomendaciones.forEach(function (recomendacion) {
                const elemento = document.createElement("li");
                elemento.textContent = recomendacion;
                listaRecomendaciones.appendChild(elemento);
            });

            seccionRecomendaciones.hidden = false;
        } else {
            seccionRecomendaciones.hidden = true;
        }

        // Mostrar el resultado del análisis.
        resultado.hidden = false;
        mensaje.textContent = "";
        mensaje.classList.remove("mensaje-error", "mensaje-progreso");

    } catch (error) {
        mensaje.textContent =
            error.message ||
            "No se ha podido completar el análisis. " +
            "Comprueba que el servidor funciona e inténtalo de nuevo.";

        mensaje.classList.add("mensaje-error");

    } finally {
        botonAnalizar.disabled = false;
    }
});