const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const btnAnalizar = document.getElementById("btnAnalizar");
const resultadosDiv = document.getElementById("resultados");
const frutaSeleccionadaDiv = document.getElementById("frutaSeleccionada");
const pesoInput = document.getElementById("peso");
const btnCalcular = document.getElementById("btnCalcular");
const totalBox = document.getElementById("totalBox");

let frutaActual = null;

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error("Error al acceder a la cámara:", error);
        alert("No se pudo acceder a la cámara.");
    });

btnAnalizar.addEventListener("click", async () => {
    if (!video.videoWidth || !video.videoHeight) {
        alert("La cámara aún no está lista.");
        return;
    }

    const context = canvas.getContext("2d");

    const videoWidth = video.videoWidth;
    const videoHeight = video.videoHeight;

    const cropSize = Math.min(videoWidth, videoHeight) * 0.55;

    const sx = (videoWidth - cropSize) / 2;
    const sy = (videoHeight - cropSize) / 2;

    canvas.width = cropSize;
    canvas.height = cropSize;

    context.drawImage(
        video,
        sx,
        sy,
        cropSize,
        cropSize,
        0,
        0,
        cropSize,
        cropSize
    );

    const imagenBase64 = canvas.toDataURL("image/jpeg");

    resultadosDiv.innerHTML = "<p>Analizando imagen...</p>";

    try {
        const response = await fetch("/predecir", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ imagen: imagenBase64 })
        });

        const data = await response.json();

        if (data.error) {
            resultadosDiv.innerHTML = `<p class="error">${data.error}</p>`;
            return;
        }

        mostrarResultados(data.resultados);

    } catch (error) {
        console.error(error);
        resultadosDiv.innerHTML = "<p class='error'>Ocurrió un error al analizar la imagen.</p>";
    }
});

function mostrarResultados(resultados) {
    resultadosDiv.innerHTML = "";

    resultados.forEach((fruta, index) => {
        const card = document.createElement("div");
        card.classList.add("resultado-card");

        card.innerHTML = `
            <div class="resultado-header">
                <span class="rank">#${index + 1}</span>
                <h3>${capitalizar(fruta.clase)}</h3>
            </div>

            <p><strong>Confianza:</strong> ${fruta.confianza}%</p>
            <p><strong>Precio:</strong> $${fruta.precio} / ${fruta.unidad}</p>

            <button>Seleccionar producto</button>
        `;

        card.querySelector("button").addEventListener("click", () => {
            seleccionarFruta(fruta);
        });

        resultadosDiv.appendChild(card);
    });
}

function seleccionarFruta(fruta) {
    frutaActual = fruta;

    frutaSeleccionadaDiv.innerHTML = `
        <h3>${capitalizar(fruta.clase)}</h3>
        <p><strong>Precio:</strong> $${fruta.precio} / ${fruta.unidad}</p>
        <p><strong>Dato:</strong> ${fruta.descripcion}</p>
    `;

    calcularTotal();
}

btnCalcular.addEventListener("click", calcularTotal);

function calcularTotal() {
    if (!frutaActual) {
        totalBox.innerHTML = "<p>Selecciona una fruta primero.</p>";
        return;
    }

    const peso = parseFloat(pesoInput.value);

    if (isNaN(peso) || peso <= 0) {
        totalBox.innerHTML = "<p>Total: $0.00</p>";
        return;
    }

    const total = peso * frutaActual.precio;

    totalBox.innerHTML = `
        <p><strong>Total:</strong> $${total.toFixed(2)}</p>
        <p>${peso.toFixed(2)} kg de ${capitalizar(frutaActual.clase)}</p>
    `;
}

function capitalizar(texto) {
    return texto.charAt(0).toUpperCase() + texto.slice(1);
}