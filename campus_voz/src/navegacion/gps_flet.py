
import flet as ft
import flet_geolocator as ftg
import httpx


class GPSFlet:

    def __init__(self, page, sesion, on_aviso=None):
        self.page = page
        self.sesion = sesion
        self.on_aviso = on_aviso

        self.geo = ftg.Geolocator(
            configuration=ftg.GeolocatorWebConfiguration(
                accuracy=ftg.GeolocatorPositionAccuracy.HIGH,
                maximum_age=ft.Duration(seconds=0),
                time_limit=ft.Duration(seconds=15),
            ),
            on_position_change=self.actualizar,
            on_error=lambda e: print("Error GPS:", e.data),
        )

        # Agregar el servicio sin modificar el diseño
        self.page.services.append(self.geo)

    async def enviar_ubicacion(self, posicion):
        datos = {
            "sesion": self.sesion,
            "latitud": posicion.latitude,
            "longitud": posicion.longitude,
            "precision": posicion.accuracy,
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                respuesta = await client.post(
                    "http://127.0.0.1:8000/gps",
                    json=datos,
                )
                respuesta.raise_for_status()
                resultado = respuesta.json()

            print("GPS actualizado:", datos)

            if resultado.get("aviso"):
                print("Aviso GPS:", resultado["aviso"])

                if self.on_aviso:
                    self.on_aviso(resultado["aviso"])

        except Exception as error:
            print("Error al enviar GPS:", error)

    async def actualizar(self, evento):
        await self.enviar_ubicacion(evento.position)

    async def iniciar(self, evento=None):
        try:
            await self.geo.request_permission()
            posicion = await self.geo.get_current_position()

            if posicion:
                await self.enviar_ubicacion(posicion)

        except Exception as error:
            print("No se pudo iniciar el GPS:", error)
