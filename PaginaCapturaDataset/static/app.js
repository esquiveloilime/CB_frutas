const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const claseSelect = document.getElementById("clase");
const btnGuardar = document.getElementById("btnGuardar");
const mensaje = document.getElementById("mensaje");
const preview = document.getElementById("preview");

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(error => {
        console.error(error);
        alert("No se pudo acceder a la cámara.");
    });

btnGuardar.addEventListener("click", async () => {
    if (!video.videoWidth || !video.videoHeight) {
        alert("La cámara aún no está lista.");
        return;
    }

    const context = canvas.getContext("2d");

    const videoWidth = video.videoWidth;
    const videoHeight = video.videoHeight;

    // Recorte cuadrado central, igual que en la app de predicción
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

    const imagenBase64 = canvas.toDataURL("image/jpeg", 0.95);

    preview.src = imagenBase64;

    const clase = claseSelect.value;

    mensaje.textContent = "Guardando foto...";

    const response = await fetch("/guardar_foto", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            clase: clase,
            imagen: imagenBase64
        })
    });

    const data = await response.json();

    if (data.error) {
        mensaje.textContent = data.error;
        return;
    }

    mensaje.textContent = `${data.mensaje}. Total en ${data.clase}: ${data.total_clase}`;
});