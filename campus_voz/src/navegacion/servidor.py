
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from navegacion import CampusVoz

app = FastAPI(title="CampusVoz")

sesiones = {}
reportes_compartidos = []

# Solo para desarrollo local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


def obtener_motor(sesion):
    if sesion not in sesiones:
        sesiones[sesion] = CampusVoz(
            reportes=reportes_compartidos
        )
    return sesiones[sesion]


class Comando(BaseModel):
    sesion: str = Field(min_length=1, max_length=80)
    texto: str = Field(min_length=1, max_length=300)


class Ubicacion(BaseModel):
    sesion: str = Field(min_length=1, max_length=80)
    latitud: float
    longitud: float
    precision: float = Field(ge=0, le=100000)


@app.post("/comando")
def comando(datos: Comando):
    motor = obtener_motor(datos.sesion)
    return motor.procesar_comando(datos.texto)


@app.post("/gps")
def gps(datos: Ubicacion):
    motor = obtener_motor(datos.sesion)

    return motor.actualizar_gps(
        datos.latitud,
        datos.longitud,
        datos.precision,
    )


@app.get("/reportes")
def reportes():
    return {"reportes": reportes_compartidos}


@app.get("/")
def inicio():
    return {"estado": "CampusVoz funcionando"}


# Página técnica para probar voz y GPS
VOZ_HTML = r"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>CampusVoz - Prueba de voz</title>
</head>
<body>
    <h1>Prueba de voz CampusVoz</h1>

    <button id="iniciar" type="button">
        Iniciar voz y GPS
    </button>

    <button id="detener" type="button">
        Detener
    </button>

    <p id="estado" role="status" aria-live="polite">
        Sesión detenida.
    </p>

<script>
const Reconocimiento =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

const parametros = new URLSearchParams(location.search);

const sesion = (
    parametros.get("sesion") ||
    crypto.randomUUID()
);

let activo = false;
let ocupado = false;
let escuchando = false;
let microfono = null;
let seguimientoGPS = null;
let avisosPendientes = [];

const estado = document.getElementById("estado");


function informar(texto) {
    console.log(texto);
    estado.textContent = texto;
}


async function enviar(endpoint, datos) {
    const respuesta = await fetch(endpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(datos)
    });

    if (!respuesta.ok) {
        throw new Error("Error del servidor");
    }

    return await respuesta.json();
}


// Reproducir una respuesta hablada
function hablar(texto) {
    return new Promise((resolver) => {
        if (!("speechSynthesis" in window)) {
            resolver();
            return;
        }

        const mensaje = new SpeechSynthesisUtterance(texto);

        mensaje.lang = "es-CL";
        mensaje.rate = 0.9;

        mensaje.onend = resolver;
        mensaje.onerror = resolver;

        speechSynthesis.cancel();
        speechSynthesis.speak(mensaje);
    });
}


// Anunciar advertencias GPS sin hablar encima
// de un comando que está siendo procesado.
async function anunciarPendientes() {
    if (ocupado || !activo || !avisosPendientes.length) {
        return;
    }

    ocupado = true;

    if (microfono && escuchando) {
        microfono.abort();
    }

    while (avisosPendientes.length && activo) {
        const aviso = avisosPendientes.shift();
        informar("Aviso GPS: " + aviso);
        await hablar(aviso);
    }

    ocupado = false;

    if (activo) {
        setTimeout(escuchar, 500);
    }
}


// Enviar la frase reconocida a Python
async function procesarVoz(texto) {
    ocupado = true;
    informar("Escuché: " + texto);

    try {
        const datos = await enviar("/comando", {
            sesion: sesion,
            texto: texto
        });

        informar("CampusVoz: " + datos.respuesta);

        await hablar(datos.respuesta);

        // Navegación de Google Maps en la misma pestaña.
        // La escucha de CampusVoz se interrumpe.
        if (
            datos.accion === "abrir_google_maps" &&
            datos.url
        ) {
            detener();
            window.location.assign(datos.url);
            return;
        }

    } catch (error) {
        informar("Error: " + error.message);
        await hablar(
            "No pude procesar el comando. Intenta nuevamente."
        );
    } finally {
        ocupado = false;

        if (activo && avisosPendientes.length) {
            await anunciarPendientes();
        } else if (activo) {
            setTimeout(escuchar, 500);
        }
    }
}



function escuchar() {

    // Evitar abrir varios micrófonos a la vez
    if (!activo || ocupado || escuchando) {
        return;
    }

    if (!Reconocimiento) {
        informar("Reconocimiento de voz no disponible.");
        activo = false;
        return;
    }

    const rec = new Reconocimiento();
    microfono = rec;

    let huboResultado = false;
    let huboError = false;

    rec.lang = "es-CL";
    rec.continuous = false;
    rec.interimResults = false;
    rec.maxAlternatives = 1;

    // Cuando el usuario dice algo
    rec.onresult = (evento) => {

        huboResultado = true;

        const texto = evento.results[0][0].transcript;

        console.log("Usuario dijo:", texto);

        // Cerrar la escucha antes de responder
        try {
            rec.stop();
        } catch (error) {
            console.log("Micrófono finalizando");
        }

        // Esta función hablará y luego
        // volverá a escuchar
        procesarVoz(texto);
    };

    // Manejar errores sin reiniciar en bucle
    rec.onerror = (evento) => {

        console.log("Error de voz:", evento.error);

        // Un cierre intencional no es un fallo
        if (
            evento.error === "aborted" &&
            (ocupado || !activo)
        ) {
            return;
        }

        huboError = true;
        activo = false;

        if (evento.error === "no-speech") {
            informar(
                "No detecté voz. Pulsa iniciar para reintentar."
            );
        } else if (evento.error === "not-allowed") {
            informar(
                "Permiso de micrófono denegado."
            );
        } else {
            informar(
                "Error del micrófono: " + evento.error
            );
        }
    };

    // Cuando termina la sesión de reconocimiento
    rec.onend = () => {

        escuchando = false;

        if (microfono === rec) {
            microfono = null;
        }

        // Si terminó sin reconocer una frase,
        // no iniciar infinitamente otra sesión.
        if (
            activo &&
            !ocupado &&
            !huboResultado &&
            !huboError
        ) {
            activo = false;

            informar(
                "Escucha finalizada. Pulsa iniciar."
            );
        }
    };

    try {

        rec.start();
        escuchando = true;

        informar("Escuchando...");

    } catch (error) {

        escuchando = false;
        activo = false;

        informar("No pude activar el micrófono.");

        console.error(error);
    }
}


// Enviar coordenadas actualizadas a Python
async function actualizarUbicacion(posicion) {
    const gps = posicion.coords;

    try {
        const datos = await enviar("/gps", {
            sesion: sesion,
            latitud: gps.latitude,
            longitud: gps.longitude,
            precision: gps.accuracy
        });

        console.log(
            "GPS:",
            gps.latitude,
            gps.longitude,
            "Precisión:",
            gps.accuracy,
            "metros"
        );

        if (datos.aviso) {
            avisosPendientes.push(datos.aviso);
            await anunciarPendientes();
        }

    } catch (error) {
        console.error("GPS:", error);
    }
}


// Iniciar desde una acción del usuario
function iniciar() {
    if (activo) return;

    activo = true;
    avisosPendientes = [];

    // Solicitar ubicación actual y cambios posteriores
    if ("geolocation" in navigator) {
        seguimientoGPS = navigator.geolocation.watchPosition(
            actualizarUbicacion,
            (error) => {
                informar("GPS no disponible: " + error.message);
            },
            {
                enableHighAccuracy: true,
                maximumAge: 0,
                timeout: 15000
            }
        );
    } else {
        informar("El navegador no admite GPS.");
    }

    // Arrancar el micrófono con el clic inicial
    escuchar();
}


function detener() {
    activo = false;
    avisosPendientes = [];

    if (microfono) {
        microfono.abort();
        microfono = null;
    }

    escuchando = false;

    if (seguimientoGPS !== null) {
        navigator.geolocation.clearWatch(seguimientoGPS);
        seguimientoGPS = null;
    }

    window.speechSynthesis?.cancel();
    informar("Sesión detenida.");
}


document.getElementById("iniciar")
    .addEventListener("click", iniciar);

document.getElementById("detener")
    .addEventListener("click", detener);
</script>
</body>
</html>
"""


@app.get("/voz", response_class=HTMLResponse)
def prueba_voz():
    return HTMLResponse(VOZ_HTML)
