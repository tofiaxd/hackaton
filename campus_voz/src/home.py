
import flet as ft
import flet_map as ftm
import themes


def build_home(page: ft.Page, username="", on_settings=None, on_routes=None):

    # ==================================
    # MAPA
    # ==================================

    campus_center = ftm.MapLatitudeLongitude(
        latitude=-33.0327,
        longitude=-71.5935
    )

    campus_map = ftm.Map(
        expand=True,
        initial_center=campus_center,
        initial_zoom=17,
        layers=[
            ftm.TileLayer(
                url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                user_agent_package_name="campus-access/1.0",
            ),
            ftm.MarkerLayer(
                markers=[
                    ftm.Marker(
                        coordinates=campus_center,
                        content=ft.Icon(
                            ft.Icons.LOCATION_ON,
                            color=themes.PRIMARY,
                            size=35,
                        ),
                    )
                ]
            ),
            ftm.SimpleAttribution(
                text="OpenStreetMap contributors"
            ),
        ],
    )

    # ==================================
    # MENU SUPERIOR
    # ==================================

    menu = ft.PopupMenuButton(
        icon=ft.Icons.MENU,
        tooltip="Abrir menú",
        items=[
            ft.PopupMenuItem(
                content=ft.Text("Configuración")
            ),
            ft.PopupMenuItem(
                content=ft.Text("Acerca de Campus Access")
            ),
        ],
    )

    page.appbar = ft.AppBar(
        leading=menu,
        leading_width=55,
        title=ft.Text(
            f"Hola, {username}!",
            weight=ft.FontWeight.BOLD,
            size=20,
            color=themes.TEXT_PRIMARY,
        ),
        center_title=False,
        bgcolor=themes.SURFACE,
        actions=[
            ft.IconButton(
            icon=ft.Icons.SETTINGS_OUTLINED,
            tooltip="Configuración",
            icon_color=themes.TEXT_PRIMARY,
            on_click=on_settings,
            ),
        ],
    )

    # ==================================
    # BOTON DE MICROFONO
    # ==================================

    microphone_button = ft.IconButton(
        icon=ft.Icons.MIC,
        icon_size=75,
        icon_color=themes.SURFACE,
        tooltip="Activar reconocimiento de voz",
        style=ft.ButtonStyle(
            bgcolor=themes.PRIMARY,
            shape=ft.CircleBorder(),
        ),
        width=170,
        height=170,
        on_click=lambda e: print("Activar micrófono"), ##
    )

    # ==================================
    # ZONA INFERIOR
    # ==================================

    bottom_section = ft.Container(
    expand=4,
    width=float("inf"),
    bgcolor=themes.BACKGROUND,
    padding=ft.Padding.symmetric(horizontal=20, vertical=15),
    content=ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        controls=[
            ft.Text(
                "¿Dónde vamos hoy?",
                size=25,
                weight=ft.FontWeight.BOLD,
                color=themes.TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Button(
                content=ft.Text(
                    "Seleccionar destino",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                icon=ft.Icons.ROUTE,
                width=300,
                height=50,
                style=ft.ButtonStyle(
                    bgcolor=themes.SURFACE,
                    color=themes.PRIMARY,
                    shape=ft.RoundedRectangleBorder(radius=12),
                ),
                on_click=on_routes,
                ),

            # Fila que centra el botón horizontalmente
            ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[microphone_button],
            ),

            ft.Text(
                "Toca el micrófono para hablar",
                size=14,
                color=themes.TEXT_SECONDARY,
                text_align=ft.TextAlign.CENTER,
            ),
        ],
    ),
)

    # ==================================
    # ESTRUCTURA PRINCIPAL
    # ==================================

    return ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[

                # Mapa: aproximadamente 65%
                ft.Container(
                    expand=7,
                    content=campus_map,
                ),

                # Zona del micrófono: aproximadamente 35%
                bottom_section,
            ],
        ),
    )
