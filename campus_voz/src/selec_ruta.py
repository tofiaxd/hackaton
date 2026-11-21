
import flet as ft
import themes

from navegacion.navegacion import CampusVoz


def build_seleccion_rutas(page: ft.Page, on_back=None):

    # Instancia de la lógica de navegación
    navegacion = CampusVoz()

    # Destino seleccionado
    destino_seleccionado = {"valor": None}

    # Texto de estado
    estado = ft.Text(
        "Selecciona uno de los destinos disponibles.",
        size=15,
        color=themes.TEXT_SECONDARY,
        text_align=ft.TextAlign.CENTER,
    )

    # Botón para verificar
    verificar_button = ft.Button(
        content=ft.Text("Verificar destino"),
        icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
        width=300,
        height=55,
        disabled=True,
        style=ft.ButtonStyle(
            bgcolor=themes.PRIMARY,
            color=themes.SURFACE,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    # Seleccionar un destino
    def seleccionar_destino(destino, nombre):

        destino_seleccionado["valor"] = destino

        estado.value = f"Destino seleccionado: {nombre}"
        estado.color = themes.PRIMARY

        verificar_button.disabled = False

        page.update()

    # Crear botones de destinos
    def crear_boton_destino(nombre, destino, icono):

        return ft.Button(
            content=ft.Text(
                nombre,
                size=17,
                weight=ft.FontWeight.BOLD,
            ),
            icon=icono,
            expand=True,
            height=85,
            style=ft.ButtonStyle(
                bgcolor=themes.SURFACE,
                color=themes.TEXT_PRIMARY,
                shape=ft.RoundedRectangleBorder(radius=12),
            ),
            on_click=lambda e: seleccionar_destino(
                destino, nombre
            ),
        )

    # Verificar y abrir la ruta
    async def verificar_ruta(e):

        destino = destino_seleccionado["valor"]

        if not destino:
            estado.value = "Primero selecciona un destino."
            page.update()
            return

        resultado = navegacion.iniciar_ruta(destino)

        estado.value = resultado["respuesta"]
        estado.color = themes.PRIMARY

        page.update()

        if resultado["url"]:
            await page.launch_url(resultado["url"])

    verificar_button.on_click = verificar_ruta

    # Botones de destinos
    biblioteca = crear_boton_destino(
        "Biblioteca",
        "biblioteca",
        ft.Icons.LOCAL_LIBRARY,
    )

    entrada1 = crear_boton_destino(
        "Entrada 1",
        "entrada 1",
        ft.Icons.DOOR_FRONT_DOOR,
    )

    entrada2 = crear_boton_destino(
        "Entrada 2",
        "entrada 2",
        ft.Icons.DOOR_FRONT_DOOR,
    )

    casino = crear_boton_destino(
        "Casino",
        "comedor",
        ft.Icons.RESTAURANT,
    )

    # Pantalla
    return ft.SafeArea(
        expand=True,
        content=ft.Container(
            expand=True,
            bgcolor=themes.BACKGROUND,
            padding=20,
            content=ft.Column(
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[

                    # Encabezado
                    ft.Row(
                        alignment=ft.MainAxisAlignment.START,
                        controls=[
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK,
                                tooltip="Volver",
                                icon_color=themes.TEXT_PRIMARY,
                                on_click=lambda e: (
                                    on_back() if on_back else None
                                ),
                            ),
                        ],
                    ),

                    ft.Icon(
                        ft.Icons.ROUTE,
                        size=55,
                        color=themes.PRIMARY,
                    ),

                    ft.Text(
                        "¿A dónde vamos?",
                        size=27,
                        weight=ft.FontWeight.BOLD,
                        color=themes.TEXT_PRIMARY,
                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Text(
                        "Selecciona el lugar al que deseas llegar.",
                        size=15,
                        color=themes.TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER,
                    ),

                    # Destinos en dos filas
                    ft.Row(
                        spacing=12,
                        controls=[
                            biblioteca,
                            entrada1,
                        ],
                    ),

                    ft.Row(
                        spacing=12,
                        controls=[
                            entrada2,
                            casino,
                        ],
                    ),

                    ft.Container(height=10),

                    # Estado de selección
                    estado,

                    ft.Container(expand=True),

                    # Confirmar destino
                    verificar_button,

                    ft.Text(
                        "La ruta se abrirá en Google Maps.",
                        size=12,
                        color=themes.TEXT_SECONDARY,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        ),
    )
