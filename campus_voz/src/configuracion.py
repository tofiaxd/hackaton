
import flet as ft
import themes


def build_configuracion(page: ft.Page, on_back=None):

    # Opciones de accesibilidad
    texto_grande = ft.Switch(value=False)
    alto_contraste = ft.Switch(value=False)
    instrucciones_voz = ft.Switch(value=True)
    vibracion = ft.Switch(value=True)

    velocidad_voz = ft.Dropdown(
        value="Normal",
        width=180,
        options=[
            ft.dropdown.Option("Lenta"),
            ft.dropdown.Option("Normal"),
            ft.dropdown.Option("Rápida"),
        ],
    )

    # Tarjeta para agrupar configuraciones
    def config_card(title, description, control, icon):
        return ft.Container(
            padding=15,
            border_radius=12,
            bgcolor=themes.SURFACE,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        expand=True,
                        spacing=12,
                        controls=[
                            ft.Icon(
                                icon,
                                color=themes.PRIMARY,
                                size=25,
                            ),
                            ft.Column(
                                expand=True,
                                spacing=3,
                                controls=[
                                    ft.Text(
                                        title,
                                        weight=ft.FontWeight.BOLD,
                                        color=themes.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        description,
                                        size=12,
                                        color=themes.TEXT_SECONDARY,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    control,
                ],
            ),
        )

    # Volver al inicio
    def go_back(e):
        if on_back:
            on_back()
        else:
            page.go("/")

    return ft.Container(
        expand=True,
        width=float("inf"),
        bgcolor=themes.BACKGROUND,
        padding=20,
        content=ft.Column(
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            spacing=15,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=themes.PRIMARY,
                            on_click=go_back,
                            tooltip="Volver",
                        ),
                        ft.Text(
                            "Configuración",
                            size=25,
                            weight=ft.FontWeight.BOLD,
                            color=themes.TEXT_PRIMARY,
                        ),
                    ],
                ),

                ft.Text(
                    "Personaliza tu experiencia en Campus Access.",
                    color=themes.TEXT_SECONDARY,
                    size=14,
                ),

                ft.Text(
                    "ACCESIBILIDAD VISUAL",
                    weight=ft.FontWeight.BOLD,
                    color=themes.PRIMARY,
                    size=13,
                ),

                config_card(
                    "Texto grande",
                    "Aumentar el tamaño de las letras",
                    texto_grande,
                    ft.Icons.TEXT_FIELDS,
                ),

                config_card(
                    "Alto contraste",
                    "Mejorar la visibilidad de los elementos",
                    alto_contraste,
                    ft.Icons.CONTRAST,
                ),

                ft.Text(
                    "ACCESIBILIDAD AUDITIVA",
                    weight=ft.FontWeight.BOLD,
                    color=themes.PRIMARY,
                    size=13,
                ),

                config_card(
                    "Instrucciones por voz",
                    "Recibir indicaciones habladas",
                    instrucciones_voz,
                    ft.Icons.VOLUME_UP,
                ),

                ft.Container(
                    padding=15,
                    border_radius=12,
                    bgcolor=themes.SURFACE,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=3,
                                controls=[
                                    ft.Text(
                                        "Velocidad de voz",
                                        weight=ft.FontWeight.BOLD,
                                        color=themes.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        "Selecciona la velocidad de lectura",
                                        size=12,
                                        color=themes.TEXT_SECONDARY,
                                    ),
                                ],
                            ),
                            velocidad_voz,
                        ],
                    ),
                ),

                ft.Text(
                    "ALERTAS",
                    weight=ft.FontWeight.BOLD,
                    color=themes.PRIMARY,
                    size=13,
                ),

                config_card(
                    "Vibración",
                    "Recibir alertas mediante vibración",
                    vibracion,
                    ft.Icons.VIBRATION,
                ),

                ft.Text(
                    "Los cambios se aplicarán cuando las funciones "
                    "correspondientes estén disponibles.",
                    size=12,
                    color=themes.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )
