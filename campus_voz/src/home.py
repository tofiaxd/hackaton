
import flet as ft
import flet_map as ftm
import themes


def build_home(page: ft.Page):

    # Centro aproximado de la USM Casa Central
    campus_center = ftm.MapLatitudeLongitude(
        latitude=-33.0327,
        longitude=-71.5935
    )

    # Mapa interactivo
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
                            color=ft.Colors.RED,
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

    # Menú hamburguesa
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

    # Barra superior
    page.appbar = ft.AppBar(
        leading=menu,
        leading_width=55,
        title=ft.Text(
            "Campus Access",
            weight=ft.FontWeight.BOLD,
            size=20,
        ),
        center_title=False,
        bgcolor=themes.PRIMARY,
        color=ft.Colors.WHITE,
        actions=[
            ft.IconButton(
                icon=ft.Icons.SETTINGS_OUTLINED,
                tooltip="Configuración",
            ),
        ],
    )

    # Botón inferior
    navigation_button = ft.Button(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.NAVIGATION, size=25),
                ft.Text(
                    "¿A dónde quieres ir?",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=12,
        ),
        expand=True,
        height=65,
        style=ft.ButtonStyle(
            bgcolor=themes.PRIMARY,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=15),
        ),
        on_click=lambda e: print("Abrir selección de destino"),
    )

    # Estructura principal
    return ft.SafeArea(
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[

                # Mapa
                ft.Container(
                    expand=True,
                    content=campus_map,
                ),

                # Botón inferior
                ft.Container(
                    padding=ft.Padding.symmetric(
                        horizontal=18,
                        vertical=14,
                    ),
                    bgcolor=ft.Colors.WHITE,
                    content=navigation_button,
                ),
            ],
        ),
    )
