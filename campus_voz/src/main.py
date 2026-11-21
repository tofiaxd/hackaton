
import asyncio
import flet as ft
import flet_geolocator as ftg

from home import build_home
from login import build_login
from configuracion import build_configuracion
from selec_ruta import build_seleccion_rutas

from navegacion.navegacion import (
    CampusVoz,
    obtener_ruta_peatonal,
)

import themes


def main(page: ft.Page):

    # ==================================
    # CONFIGURACION GENERAL
    # ==================================

    page.window.width = 390
    page.window.height = 830
    page.window.resizable = True

    page.title = "Campus Access"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = themes.APP_THEME
    page.padding = 0
    page.bgcolor = themes.BACKGROUND

    username = ""

    # ==================================
    # ALERTAS
    # ==================================

    reportes = []
    gestor_alertas = CampusVoz(reportes=reportes)

    def guardar_alerta(tipo, zona):

        gestor_alertas.reporte_pendiente = {
            "tipo": tipo,
            "zona": zona,
        }

        gestor_alertas.confirmar_reporte()

        if reportes:
            print("Alerta registrada:", reportes[-1])

        return True

    # ==================================
    # GOOGLE MAPS
    # ==================================

    async def abrir_google_maps(url):

        if url:
            await ft.UrlLauncher().launch_url(url)

    # ==================================
    # CALCULAR RUTA
    # ==================================

    async def calcular_ruta(destino, maps_url):

        page.clean()

        page.add(
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                bgcolor=themes.BACKGROUND,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.ProgressRing(
                            color=themes.PRIMARY
                        ),

                        ft.Text(
                            "Calculando tu recorrido...",
                            color=themes.TEXT_PRIMARY,
                            size=16,
                        ),
                    ],
                ),
            )
        )

        page.update()

        try:

            geo = ftg.Geolocator()
            permiso = await geo.request_permission()

            if permiso in (
                ftg.GeolocatorPermissionStatus.DENIED,
                ftg.GeolocatorPermissionStatus.DENIED_FOREVER,
            ):

                raise RuntimeError(
                    "No se concedió permiso para utilizar el GPS."
                )

            posicion = await geo.get_current_position()

            latitud = posicion.latitude
            longitud = posicion.longitude
            precision = posicion.accuracy

            if precision is not None and precision > 150:

                raise RuntimeError(
                    f"La precisión del GPS es de {round(precision)} metros. "
                    "Intenta obtener una ubicación más precisa."
                )

            ubicacion = (latitud, longitud)

            coordenadas = await asyncio.to_thread(
                obtener_ruta_peatonal,
                latitud,
                longitud,
                destino,
            )

            show_home(
                route_coordinates=coordenadas,
                current_location=ubicacion,
                maps_url=maps_url,
                destination=destino,
                route_message=f"Recorrido hacia {destino}",
            )

        except Exception as error:

            print("Error al calcular ruta:", error)

            show_home(
                maps_url=maps_url,
                destination=destino,
                route_message=f"No se pudo calcular la ruta: {error}",
            )

    # ==================================
    # RECONOCIMIENTO DE VOZ
    # ==================================

    async def procesar_voz(texto):

        print("Comando reconocido:", texto)

        try:

            resultado = gestor_alertas.procesar_comando(texto)

            respuesta = resultado.get(
                "respuesta",
                "No pude interpretar el comando."
            )

            destino = resultado.get("destino")
            url = resultado.get("url")
            accion = resultado.get("accion")

            print("Respuesta de Campus Access:", respuesta)

            # ABRIR GOOGLE MAPS
            if accion == "abrir_google_maps" and url:

                await abrir_google_maps(url)

            # CALCULAR RUTA AL DESTINO RECONOCIDO
            elif destino and url:

                await calcular_ruta(destino, url)

            return respuesta

        except Exception as error:

            print("Error al procesar el comando:", error)

            return "No pude procesar esa instrucción."

    # ==================================
    # PANTALLA PRINCIPAL
    # ==================================

    def show_home(
        name=None,
        route_coordinates=None,
        current_location=None,
        maps_url=None,
        destination=None,
        route_message=None
    ):

        nonlocal username

        if name is not None:
            username = name

        page.clean()

        async def maps_click(e):
            await abrir_google_maps(maps_url)

        page.add(
            build_home(
                page,
                username,
                on_settings=show_configuracion,
                on_routes=show_rutas,
                on_maps=maps_click if maps_url else None,
                on_add_alert=guardar_alerta,
                on_voice_command=procesar_voz,
                route_coordinates=route_coordinates,
                current_location=current_location,
                destination=destination,
                route_message=route_message,
                reportes=reportes,
            )
        )

        page.update()

    # ==================================
    # CONFIGURACION
    # ==================================

    def show_configuracion(e=None):

        page.clean()

        page.add(
            build_configuracion(
                page,
                on_back=lambda: show_home()
            )
        )

        page.update()

    # ==================================
    # SELECCION DE RUTAS
    # ==================================

    def show_rutas(e=None):

        page.clean()

        page.add(
            build_seleccion_rutas(
                page,
                on_back=lambda: show_home(),
                on_select=calcular_ruta,
            )
        )

        page.update()

    # ==================================
    # INICIAR APLICACION
    # ==================================

    page.add(
        build_login(page, show_home)
    )


if __name__ == "__main__":
    ft.run(main)
