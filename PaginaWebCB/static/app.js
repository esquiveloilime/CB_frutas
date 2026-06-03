const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const btnAnalizar = document.getElementById("btnAnalizar");
const resultadosDiv = document.getElementById("resultados");
const frutaSeleccionadaDiv = document.getElementById("frutaSeleccionada");

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error("Error al acceder a la cámara:", error);
        alert("No se pudo acceder a la cámara.");
    });

btnAnalizar.addEventListener("click", async () => {
    const context = canvas.getContext("2d");

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    const imagenBase64 = canvas.toDataURL("image/jpeg");

    resultadosDiv.innerHTML = "<p>Analizando imagen...</p>";

    const response = await fetch("/predecir", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ imagen: imagenBase64 })
    });

    const data = await response.json();

    resultadosDiv.innerHTML = "";

    data.resultados.forEach(fruta => {
        const card = document.createElement("div");
        card.classList.add("resultado-card");

        card.innerHTML = `
            <h3>${capitalizar(fruta.clase)}</h3>
            <p>Confianza: ${fruta.confianza}%</p>
            <p>Precio: $${fruta.precio} / ${fruta.unidad}</p>
            <button>Seleccionar</button>
        `;

        card.querySelector("button").addEventListener("click", () => {
            mostrarFruta(fruta);
        });

        resultadosDiv.appendChild(card);
    });
});

function mostrarFruta(fruta) {
    frutaSeleccionadaDiv.innerHTML = `
        <h3>${capitalizar(fruta.clase)}</h3>
        <p><strong>Precio:</strong> $${fruta.precio} / ${fruta.unidad}</p>
        <p><strong>Descripción:</strong> ${fruta.descripcion}</p>
    `;
}

function capitalizar(texto) {
    return texto.charAt(0).toUpperCase() + texto.slice(1);
}