
import flet as ft
import themes
from BD.conexiones import supabase

def build_login(page: ft.Page, on_login):
    # Campo para ingresar el nombre
    name_field = ft.TextField(
        label="Tu nombre",
        hint_text="Escribe tu nombre aquí",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
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

        try:
            # Buscar el usuario en Supabase
            respuesta = (
                supabase.table("usuarios")
                .select("id, nombre")
                .eq("nombre", name)
                .limit(1)
                .execute()
            )

            # Comprobar si existe
            if not respuesta.data:
                error_text.value = "Usuario no encontrado."
                page.update()
                return

            # Usuario encontrado
            error_text.value = ""
            on_login(respuesta.data[0]["nombre"])

        except Exception as error:
            error_text.value = "Error al conectar con la base de datos."
            print("Error:", error)
            page.update()


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
    width=float("inf"),
    bgcolor=themes.BACKGROUND,
    alignment=ft.Alignment.CENTER,
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
                text_align=ft.TextAlign.CENTER,
            ),

            ft.Text(
                "¡Bienvenido/a!",
                size=22,
                weight=ft.FontWeight.BOLD,
                color=themes.TEXT_PRIMARY,
                text_align=ft.TextAlign.CENTER,
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
