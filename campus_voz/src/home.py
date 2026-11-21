
import flet as ft
import flet_map as ftm
import themes


def build_home(
    page: ft.Page,
    username="",
    on_settings=None,
    on_maps=None,
    on_routes=None,
    route_coordinates=None,
    current_location=None,
    destination=None,
    route_message=None,
):

    # ==================================
    # COORDENADAS DEL CAMPUS
    # ==================================

    campus_center = ftm.MapLatitudeLongitude(
        latitude=-33.0327,
        longitude=-71.5935
    )

    if current_location:
        map_center = ftm.MapLatitudeLongitude(
            latitude=current_location[0],
            longitude=current_location[1]
        )
    else:
        map_center = campus_center

    # ==================================
    # CAPAS DEL MAPA
    # ==================================

    map_layers = [

        ftm.TileLayer(
            url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            user_agent_package_name="campus-access/1.0",
        ),

    ]

    # ==================================
    # DIBUJAR RECORRIDO
    # ==================================

    if route_coordinates:

        puntos_ruta = [
            ftm.MapLatitudeLongitude(
                latitude=lat,
                longitude=lon
            )
            for lat, lon in route_coordinates
        ]

        map_layers.append(
            ftm.PolylineLayer(
                polylines=[
                    ftm.PolylineMarker(
                        coordinates=puntos_ruta,
                        color=themes.PRIMARY,
                        stroke_width=7,
                    )
                ]
            )
        )

    # ==================================
    # MARCADORES
    # ==================================

    marcadores = []

    # Ubicación actual
    if current_location:

        marcadores.append(
            ftm.Marker(
                coordinates=ftm.MapLatitudeLongitude(
                    latitude=current_location[0],
                    longitude=current_location[1],
                ),
                content=ft.Icon(
                    ft.Icons.MY_LOCATION,
                    color=themes.SUCCESS,
                    size=35,
                ),
            )
        )

    # Coordenadas de los destinos
    destinos = {
        "entrada 1": (-33.03427778, -71.59586111),
        "entrada 2": (-33.03669444, -71.59522222),
        "biblioteca": (-33.03497222, -71.59516667),
        "comedor": (-33.03533333, -71.59588889),
    }

    # Marcador del destino
    if destination and destination in destinos:

        lat, lon = destinos[destination]

        marcadores.append(
            ftm.Marker(
                coordinates=ftm.MapLatitudeLongitude(
                    latitude=lat,
                    longitude=lon,
                ),
                content=ft.Icon(
                    ft.Icons.FLAG,
                    color=themes.ERROR,
                    size=35,
                ),
            )
        )

    # Marcador inicial si todavía no hay GPS
    if not marcadores:

        marcadores.append(
            ftm.Marker(
                coordinates=campus_center,
                content=ft.Icon(
                    ft.Icons.LOCATION_ON,
                    color=themes.PRIMARY,
                    size=35,
                ),
            )
        )

    map_layers.append(
        ftm.MarkerLayer(
            markers=marcadores
        )
    )

    map_layers.append(
        ftm.SimpleAttribution(
            text="OpenStreetMap contributors"
        )
    )

    # ==================================
    # MAPA
    # ==================================

    campus_map = ftm.Map(
        expand=True,
        initial_center=map_center,
        initial_zoom=17,
        layers=map_layers,
    )

    # ==================================
    # BOTÓN GOOGLE MAPS
    # ==================================

    maps_button = ft.Button(
        content=ft.Text("Maps"),
        icon=ft.Icons.MAP,
        height=45,
        tooltip="Abrir Google Maps",
        style=ft.ButtonStyle(
            bgcolor=themes.SURFACE,
            color=themes.PRIMARY,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        on_click=on_maps,
    )

    # ==================================
    # BOTÓN DE ALERTAS
    # ==================================

    alert_button = ft.Button(
        content=ft.Text("Añadir alerta"),
        icon=ft.Icons.WARNING_AMBER,
        height=45,
        disabled=True,
        tooltip="Función próximamente",
        style=ft.ButtonStyle(
            bgcolor=themes.SURFACE,
            color=themes.ERROR,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
    )

    # ==================================
    # MENÚ SUPERIOR
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
    # BOTÓN DE MICRÓFONO
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
        on_click=lambda e: print("Activar micrófono"),
    )

    # ==================================
    # ZONA INFERIOR
    # ==================================

    controles_inferiores = [

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

    ]

    if route_message:

        controles_inferiores.append(
            ft.Text(
                route_message,
                size=12,
                color=themes.PRIMARY,
                text_align=ft.TextAlign.CENTER,
            )
        )

    controles_inferiores.extend([

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

    ])

    bottom_section = ft.Container(
        expand=4,
        width=float("inf"),
        bgcolor=themes.BACKGROUND,
        padding=ft.Padding.symmetric(
            horizontal=20,
            vertical=15
        ),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
            controls=controles_inferiores,
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

                ft.Container(
                    expand=7,
                    content=ft.Stack(
                        expand=True,
                        controls=[

                            campus_map,

                            # Botón Maps
                            ft.Container(
                                left=12,
                                top=12,
                                content=maps_button,
                            ),

                            # Botón alertas
                            ft.Container(
                                right=12,
                                top=12,
                                content=alert_button,
                            ),

                        ],
                    ),
                ),

                bottom_section,
            ],
        ),
    )
