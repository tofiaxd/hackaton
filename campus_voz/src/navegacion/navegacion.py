
import math
import re
import unicodedata
from urllib.parse import urlencode
import json
import urllib.request
import urllib.error


# Coordenadas reales del campus
PUNTOS = {
    "entrada 1": (-33.03427778, -71.59586111),
    "entrada 2": (-33.03669444, -71.59522222),
    "biblioteca": (-33.03497222, -71.59516667),
    "comedor": (-33.03533333, -71.59588889),
}

ALIAS = {
    "entrada numero uno": "entrada 1",
    "entrada uno": "entrada 1",
    "entrada 1": "entrada 1",
    "entrada numero dos": "entrada 2",
    "entrada dos": "entrada 2",
    "entrada 2": "entrada 2",
    "biblioteca": "biblioteca",
    "comedor": "comedor",
    "casino": "comedor",
}


def normalizar(texto):
    texto = texto.lower().strip()
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"\s+", " ", texto)


def detectar_lugar(texto):
    texto = normalizar(texto)

    for alias in sorted(ALIAS, key=len, reverse=True):
        if re.search(r"\b" + re.escape(alias) + r"\b", texto):
            return ALIAS[alias]

    return None


def distancia_metros(lat1, lon1, lat2, lon2):
    """Distancia aproximada en línea recta."""
    radio = 6371000

    a1 = math.radians(lat1)
    a2 = math.radians(lat2)

    diferencia_lat = math.radians(lat2 - lat1)
    diferencia_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(diferencia_lat / 2) ** 2
        + math.cos(a1) * math.cos(a2)
        * math.sin(diferencia_lon / 2) ** 2
    )

    return 2 * radio * math.asin(min(1, math.sqrt(a)))


def ruta_google(destino):
    """Google Maps utiliza la ubicación actual del dispositivo."""
    if destino not in PUNTOS:
        raise ValueError("Destino desconocido")

    lat, lon = PUNTOS[destino]

    parametros = urlencode({
        "api": "1",
        "destination": f"{lat},{lon}",
        "travelmode": "walking",
        "dir_action": "navigate",
    })

    return "https://www.google.com/maps/dir/?" + parametros


class CampusVoz:
    def __init__(self, reportes=None):
        self.ubicacion = None
        self.destino = None
        self.reporte_pendiente = None

        # Lista compartida si la entrega el servidor
        self.reportes = reportes if reportes is not None else []

        self.ultima_respuesta = "Bienvenido a CampusVoz."
        self.avisos_emitidos = set()

    def respuesta(self, mensaje, url=None, accion=None):
        self.ultima_respuesta = mensaje

        return {
            "respuesta": mensaje,
            "url": url,
            "accion": accion,
            "destino": self.destino,
            "ubicacion": self.ubicacion,
            "reportes": list(self.reportes),
        }

    def lugar_cercano(self):
        if not self.ubicacion:
            return None, None

        lat = self.ubicacion["latitud"]
        lon = self.ubicacion["longitud"]

        lugar = min(
            PUNTOS,
            key=lambda nombre: distancia_metros(
                lat, lon, *PUNTOS[nombre]
            )
        )

        distancia = distancia_metros(lat, lon, *PUNTOS[lugar])
        return lugar, round(distancia)

    def actualizar_gps(self, latitud, longitud, precision):
        """Recibe coordenadas nuevas desde el navegador o Flet."""

        if not (-90 <= latitud <= 90 and -180 <= longitud <= 180):
            raise ValueError("Coordenadas inválidas")

        if not math.isfinite(precision) or precision < 0:
            raise ValueError("Precisión GPS inválida")

        self.ubicacion = {
            "latitud": latitud,
            "longitud": longitud,
            "precision": precision,
        }

        # No emitir avisos de proximidad con GPS impreciso.
        if precision > 20:
            return {
                "aviso": None,
                "ubicacion": self.ubicacion,
                "gps_confiable": False,
            }

        aviso = None

        # Posible proximidad al destino
        if self.destino:
            distancia = distancia_metros(
                latitud, longitud, *PUNTOS[self.destino]
            )

            clave = "destino:" + self.destino

            if distancia <= 20 and clave not in self.avisos_emitidos:
                self.avisos_emitidos.add(clave)
                aviso = (
                    f"Según el GPS, podrías estar cerca de "
                    f"{self.destino}. Confirma el acceso "
                    "con una referencia fiable."
                )

        # Aviso por obstáculo cercano registrado
        if aviso is None:
            for indice, reporte in enumerate(self.reportes):
                zona = reporte["zona"]

                if zona not in PUNTOS:
                    continue

                distancia = distancia_metros(
                    latitud, longitud, *PUNTOS[zona]
                )

                clave = f"obstaculo:{indice}"

                if distancia <= 30 and clave not in self.avisos_emitidos:
                    self.avisos_emitidos.add(clave)

                    aviso = (
                        f"Atención: existe un reporte de "
                        f"{reporte['tipo']} cerca de {zona}. "
                        "No se ha verificado su estado. "
                        "Solicita asistencia si es necesario."
                    )
                    break

        return {
            "aviso": aviso,
            "ubicacion": self.ubicacion,
            "gps_confiable": True,
        }

    def iniciar_ruta(self, destino):
        if destino not in PUNTOS:
            return self.respuesta("No conozco ese destino.")

        self.destino = destino
        self.avisos_emitidos.clear()

        mensaje = (
            f"Destino seleccionado: {destino}. "
            "La ruta peatonal está disponible en Google Maps. "
            "Puedes decir abrir mapa."
        )

        if any(r["zona"] == destino for r in self.reportes):
            mensaje += (
                " Atención: hay un obstáculo reportado "
                "en ese sector."
            )

        return self.respuesta(mensaje, ruta_google(destino))

    def confirmar_reporte(self):
        reporte = self.reporte_pendiente

        if not reporte or not reporte.get("zona"):
            return self.respuesta(
                "Debes indicar una zona para el reporte."
            )

        self.reportes.append(reporte.copy())
        self.reporte_pendiente = None

        return self.respuesta(
            f"Reporte registrado: {reporte['tipo']} "
            f"en {reporte['zona']}. "
            "El reporte es una advertencia, "
            "no modifica automáticamente Google Maps."
        )

    def procesar_comando(self, texto):
        comando = normalizar(texto)
        lugar = detectar_lugar(comando)

        if not comando:
            return self.respuesta("Repite, por favor.")

        # Reporte pendiente
        if self.reporte_pendiente:
            if comando in ("cancelar", "no"):
                self.reporte_pendiente = None
                return self.respuesta("Reporte cancelado.")

            if self.reporte_pendiente["zona"] is None:
                if lugar:
                    self.reporte_pendiente["zona"] = lugar
                    return self.respuesta(
                        f"¿Confirmas el reporte en {lugar}? "
                        "Di confirmar o cancelar."
                    )

                return self.respuesta(
                    "¿En qué zona está el problema? "
                    "Puedes decir biblioteca, comedor, "
                    "entrada uno o entrada dos."
                )

            if comando in ("confirmar", "confirmo", "si"):
                return self.confirmar_reporte()

            return self.respuesta("Di confirmar o cancelar.")

        # Ayuda
        if "ayuda" in comando:
            self.destino = None
            return self.respuesta(
                "Navegación de CampusVoz detenida. "
                "Solicita asistencia presencial."
            )

        # Repetición
        if "repetir" in comando:
            return self.respuesta(self.ultima_respuesta)

        # Reportes
        ascensor_averiado = (
            "ascensor" in comando
            and any(
                x in comando for x in (
                    "no funciona", "roto", "averiado",
                    "fuera de servicio"
                )
            )
        )

        if (
            "mojado" in comando
            or ascensor_averiado
            or "obstaculo" in comando
            or "bloqueado" in comando
        ):
            if "mojado" in comando:
                tipo = "pasillo mojado"
            elif ascensor_averiado:
                tipo = "ascensor fuera de servicio"
            else:
                tipo = "obstáculo"

            self.reporte_pendiente = {
                "tipo": tipo,
                "zona": lugar,
            }

            if lugar:
                return self.respuesta(
                    f"¿Confirmas {tipo} en {lugar}? "
                    "Di confirmar o cancelar."
                )

            return self.respuesta(
                "¿En qué zona está el problema?"
            )

        # Abrir Google Maps
        if "abrir mapa" in comando or "abrir google" in comando:
            if not self.destino:
                return self.respuesta(
                    "Primero indica a dónde quieres ir."
                )

            return self.respuesta(
                "Abriendo Google Maps. "
                "CampusVoz dejará de escuchar al cambiar de página.",
                url=ruta_google(self.destino),
                accion="abrir_google_maps",
            )

        # Consultar ubicación GPS
        if (
            "donde estoy" in comando
            or "mi ubicacion" in comando
        ):
            if not self.ubicacion:
                return self.respuesta(
                    "Todavía no tengo tu ubicación GPS."
                )

            precision = self.ubicacion["precision"]

            if precision > 20:
                return self.respuesta(
                    "El GPS tiene una precisión estimada "
                    f"de {round(precision)} metros. "
                    "No puedo identificar un punto fiable."
                )

            cercano, distancia = self.lugar_cercano()

            return self.respuesta(
                f"El punto registrado más cercano es "
                f"{cercano}, aproximadamente a "
                f"{distancia} metros en línea recta. "
                "Eso no confirma que estés en ese lugar."
            )

        # Cancelar navegación
        if "cancelar ruta" in comando:
            self.destino = None
            return self.respuesta("Recorrido cancelado.")

        # Llegada confirmada por voz
        if "llegue" in comando:
            if not self.destino:
                return self.respuesta(
                    "No tienes un destino seleccionado."
                )

            destino = self.destino
            self.destino = None

            return self.respuesta(
                f"Has indicado que llegaste a {destino}. "
                "La llegada no se verificó automáticamente."
            )

        # Seleccionar destino
        if lugar:
            return self.iniciar_ruta(lugar)

        return self.respuesta(
            "No entendí. Puedes decir biblioteca, "
            "comedor, dónde estoy, abrir mapa "
            "o reportar un obstáculo."
        )


if __name__ == "__main__":
    nav = CampusVoz()

    print(nav.procesar_comando("biblioteca"))
    print(nav.procesar_comando("dónde estoy"))

    print(nav.actualizar_gps(
        -33.03427778, -71.59586111, 8.0
    ))

    print(nav.procesar_comando("dónde estoy"))
    print(nav.procesar_comando("abrir mapa"))


# ==================================
# DECODIFICAR RECORRIDO DE VALHALLA
# ==================================

def decodificar_polyline(encoded, precision=6):
    """Convierte una polyline6 en coordenadas de latitud y longitud."""

    coordenadas = []
    indice = 0
    latitud = 0
    longitud = 0
    factor = 10 ** precision

    while indice < len(encoded):

        resultado = 0
        desplazamiento = 0

        while True:
            byte = ord(encoded[indice]) - 63
            indice += 1

            resultado |= (byte & 0x1F) << desplazamiento
            desplazamiento += 5

            if byte < 0x20:
                break

        delta = (
            ~(resultado >> 1)
            if resultado & 1
            else resultado >> 1
        )

        latitud += delta

        resultado = 0
        desplazamiento = 0

        while True:
            byte = ord(encoded[indice]) - 63
            indice += 1

            resultado |= (byte & 0x1F) << desplazamiento
            desplazamiento += 5

            if byte < 0x20:
                break

        delta = (
            ~(resultado >> 1)
            if resultado & 1
            else resultado >> 1
        )

        longitud += delta

        coordenadas.append((
            latitud / factor,
            longitud / factor
        ))

    return coordenadas


# ==================================
# OBTENER RUTA PEATONAL
# ==================================

def obtener_ruta_peatonal(
    latitud_origen,
    longitud_origen,
    destino
):
    """Solicita a Valhalla una ruta peatonal."""

    if destino not in PUNTOS:
        raise ValueError("Destino desconocido.")

    latitud_destino, longitud_destino = PUNTOS[destino]

    datos = {
        "locations": [
            {
                "lat": latitud_origen,
                "lon": longitud_origen,
            },
            {
                "lat": latitud_destino,
                "lon": longitud_destino,
            },
        ],
        "costing": "pedestrian",
        "units": "kilometers",
        "language": "es-ES",
        "shape_format": "polyline6",
        "directions_type": "none",
    }

    cuerpo = json.dumps(datos).encode("utf-8")

    solicitud = urllib.request.Request(
        "https://valhalla1.openstreetmap.de/route",
        data=cuerpo,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "CampusAccess/1.0",
            "X-Client-Id": "campus-access-hackathon",
        },
        method="POST",
    )

    try:

        with urllib.request.urlopen(
            solicitud,
            timeout=25
        ) as respuesta:

            resultado = json.loads(
                respuesta.read().decode("utf-8")
            )

    except urllib.error.HTTPError as error:

        raise RuntimeError(
            f"El servidor de rutas respondió con error: {error.code}"
        )

    except urllib.error.URLError as error:

        raise RuntimeError(
            f"No se pudo conectar con el servidor de rutas: {error.reason}"
        )

    try:

        geometria = resultado["trip"]["legs"][0]["shape"]

    except (KeyError, IndexError, TypeError):

        raise RuntimeError(
            "El servidor no pudo encontrar un recorrido entre estos puntos."
        )

    coordenadas = decodificar_polyline(geometria)

    if len(coordenadas) < 2:
        raise RuntimeError(
            "El recorrido recibido está incompleto."
        )

    return coordenadas
