
import flet as ft
import themes


def build_login(page: ft.Page, on_login):
    # Campo para ingresar el nombre
    name_field = ft.TextField(
        label="Tu nombre",
        hint_text="Escribe tu nombre aquí",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        border_radius=12,
        border_color=themes.SECONDARY,
        focused_border_color=themes.PRIMARY,
        width=320,
    )

    # Mensaje de error
    error_text = ft.Text(
        "",
        color=themes.ERROR,
        size=13,
    )

    # Acción del botón
    def login_click(e):
        name = name_field.value.strip() if name_field.value else ""

        if not name:
            error_text.value = "Por favor, ingresa tu nombre."
            page.update()
            return

        error_text.value = ""
        on_login(name)

    # Botón para ingresar
    login_button = ft.Button(
    content=ft.Text("Ingresar"),
    icon=ft.Icons.ARROW_FORWARD,
    width=320,
    height=50,
    style=ft.ButtonStyle(
        bgcolor=themes.PRIMARY,
        color=themes.SURFACE,
        shape=ft.RoundedRectangleBorder(radius=12),
    ),
    on_click=login_click,
)

    return ft.Container(
        expand=True,
        bgcolor=themes.BACKGROUND,
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Icon(
                    ft.Icons.ACCESSIBILITY_NEW,
                    size=75,
                    color=themes.PRIMARY,
                ),

                ft.Text(
                    "Campus Access",
                    size=30,
                    weight=ft.FontWeight.BOLD,
                    color=themes.TEXT_PRIMARY,
                ),

                ft.Text(
                    "¡Bienvenido/a!",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=themes.TEXT_PRIMARY,
                ),

                ft.Text(
                    "Para comenzar, dinos cómo te llamas.",
                    size=14,
                    color=themes.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),

                name_field,
                error_text,
                login_button,
            ],
        ),
    )
