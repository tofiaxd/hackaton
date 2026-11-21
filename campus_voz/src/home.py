
import flet as ft
import flet_map as ftm
import themes


def build_home(
    page: ft.Page,
    username="",
    on_settings=None,
    on_maps=None,
    on_routes=None,
    on_add_alert=None,
    route_coordinates=None,
    current_location=None,
    destination=None,
    route_message=None,
    reportes=None,
):

    if reportes is None:
        reportes = []

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

    map_layers = [
        ftm.TileLayer(
            url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
            user_agent_package_name="campus-access/1.0",
        ),
    ]

    # DIBUJAR RUTA PEATONAL
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

    destinos = {
        "entrada 1": (-33.03427778, -71.59586111),
        "entrada 2": (-33.03669444, -71.59522222),
        "biblioteca": (-33.03497222, -71.59516667),
        "comedor": (-33.03533333, -71.59588889),
    }

    # MARCADORES DEL MAPA
    marcadores = []

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

    # MARCADORES DE ALERTAS YA REGISTRADAS
    for reporte in reportes:
        zona = reporte.get("zona")

        if zona in destinos:
            lat, lon = destinos[zona]

            marcadores.append(
                ftm.Marker(
                    coordinates=ftm.MapLatitudeLongitude(
                        latitude=lat,
                        longitude=lon,
                    ),
                    content=ft.Icon(
                        ft.Icons.WARNING_AMBER,
                        color=themes.ACCENT,
                        size=35,
                    ),
                )
            )

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

    capa_marcadores = ftm.MarkerLayer(markers=marcadores)
    map_layers.append(capa_marcadores)

    map_layers.append(
        ftm.SimpleAttribution(
            text="OpenStreetMap contributors"
        )
    )

    campus_map = ftm.Map(
        expand=True,
        initial_center=map_center,
        initial_zoom=17,
        layers=map_layers,
    )

    # CONTADOR DE ALERTAS
    contador_alertas = ft.Text(
        f"Alertas registradas: {len(reportes)}",
        size=12,
        color=themes.TEXT_SECONDARY,
        text_align=ft.TextAlign.CENTER,
    )

    # FORMULARIO PARA CREAR UNA ALERTA
    def abrir_dialogo_alerta(e=None):

        tipo_alerta = ft.Dropdown(
            label="Tipo de problema",
            width=300,
            options=[
                ft.DropdownOption(
                    key="pasillo mojado",
                    text="Pasillo mojado",
                ),
                ft.DropdownOption(
                    key="ascensor fuera de servicio",
                    text="Ascensor fuera de servicio",
                ),
                ft.DropdownOption(
                    key="obstáculo",
                    text="Obstáculo en el camino",
                ),
            ],
        )

        zona_alerta = ft.Dropdown(
            label="¿Dónde ocurre?",
            width=300,
            options=[
                ft.DropdownOption(
                    key="biblioteca",
                    text="Biblioteca",
                ),
                ft.DropdownOption(
                    key="comedor",
                    text="Casino",
                ),
                ft.DropdownOption(
                    key="entrada 1",
                    text="Entrada 1",
                ),
                ft.DropdownOption(
                    key="entrada 2",
                    text="Entrada 2",
                ),
            ],
        )

        mensaje = ft.Text(
            "",
            color=themes.ERROR,
            size=13,
        )

        def guardar_alerta(ev):
            if not tipo_alerta.value or not zona_alerta.value:
                mensaje.value = "Selecciona el tipo de problema y su ubicación."
                page.update()
                return

            if on_add_alert:
                resultado = on_add_alert(
                    tipo_alerta.value,
                    zona_alerta.value,
                )

                if not resultado:
                    mensaje.value = "No se pudo registrar la alerta."
                    page.update()
                    return

            # Agregar marcador al mapa
            if zona_alerta.value in destinos:
                lat, lon = destinos[zona_alerta.value]

                marcadores.append(
                    ftm.Marker(
                        coordinates=ftm.MapLatitudeLongitude(
                            latitude=lat,
                            longitude=lon,
                        ),
                        content=ft.Icon(
                            ft.Icons.WARNING_AMBER,
                            color=themes.ACCENT,
                            size=35,
                        ),
                    )
                )

                capa_marcadores.markers = marcadores
                capa_marcadores.update()

            contador_alertas.value = (
                f"Alertas registradas: {len(reportes)}"
            )

            page.pop_dialog()
            page.update()

        dialogo = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "Añadir alerta",
                color=themes.TEXT_PRIMARY,
                weight=ft.FontWeight.BOLD,
            ),
            content=ft.Column(
                tight=True,
                width=320,
                controls=[
                    ft.Text(
                        "Ayúdanos a informar sobre problemas "
                        "que puedan afectar el desplazamiento.",
                        color=themes.TEXT_SECONDARY,
                        size=14,
                    ),
                    tipo_alerta,
                    zona_alerta,
                    mensaje,
                ],
            ),
            actions=[
                ft.TextButton(
                    content="Cancelar",
                    on_click=lambda ev: page.pop_dialog(),
                ),
                ft.Button(
                    content="Registrar alerta",
                    on_click=guardar_alerta,
                    style=ft.ButtonStyle(
                        bgcolor=themes.PRIMARY,
                        color=themes.SURFACE,
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.show_dialog(dialogo)

    # BOTÓN GOOGLE MAPS
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

    # BOTÓN AÑADIR ALERTA
    alert_button = ft.Button(
        content=ft.Text("Añadir alerta"),
        icon=ft.Icons.WARNING_AMBER,
        height=45,
        tooltip="Informar sobre un problema",
        style=ft.ButtonStyle(
            bgcolor=themes.SURFACE,
            color=themes.ERROR,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        on_click=abrir_dialogo_alerta,
    )

    menu = ft.PopupMenuButton(
        icon=ft.Icons.MENU,
        tooltip="Abrir menú",
        items=[
            ft.PopupMenuItem(content=ft.Text("Configuración")),
            ft.PopupMenuItem(content=ft.Text("Acerca de Campus Access")),
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

    # MICRÓFONO
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
        contador_alertas,

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

                            ft.Container(
                                left=12,
                                top=12,
                                content=maps_button,
                            ),

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
