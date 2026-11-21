
import flet as ft
import flet_geolocator as ftg


async def main(page: ft.Page):

    page.title = "Prueba GPS - Campus Access"
    page.padding = 20

    geo = ftg.Geolocator()

    resultado = ft.Text(
        "Presiona el botón para comprobar tu ubicación.",
        size=16,
    )

    async def comprobar_gps(e):

        resultado.value = "Solicitando permiso y ubicación..."
        page.update()

        try:
            permiso = await geo.request_permission()

            if permiso not in (
                ftg.GeolocatorPermissionStatus.WHILE_IN_USE,
                ftg.GeolocatorPermissionStatus.ALWAYS,
            ):
                resultado.value = f"Permiso GPS: {permiso}"
                page.update()
                return

            posicion = await geo.get_current_position()

            resultado.value = (
                f"GPS funcionando\n\n"
                f"Latitud: {posicion.latitude}\n"
                f"Longitud: {posicion.longitude}\n"
                f"Precisión: {posicion.accuracy} metros"
            )

        except Exception as error:
            resultado.value = f"No se pudo obtener GPS:\n{error}"

        page.update()

    page.add(
        ft.Column(
            controls=[
                ft.Text("Diagnóstico de ubicación", size=24),
                ft.Button(
                    content=ft.Text("Comprobar GPS"),
                    icon=ft.Icons.MY_LOCATION,
                    on_click=comprobar_gps,
                ),
                resultado,
            ],
            spacing=20,
        )
    )


ft.run(main)
