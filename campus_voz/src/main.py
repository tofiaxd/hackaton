import flet as ft
from home import build_home
from login import build_login
from configuracion import build_configuracion
import themes


def main(page: ft.Page):

    page.window.width = 390
    page.window.height = 830
    page.window.resizable = True

    page.title = "Campus Access"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = themes.APP_THEME
    page.padding = 0
    page.bgcolor = themes.BACKGROUND

    username = ""

    def show_home(name=None):
        nonlocal username

        if name is not None:
            username = name

        page.clean()

        page.add(
            build_home(
                page,
                username,
                on_settings=show_configuracion
            )
        )

        page.update()

    def show_configuracion(e=None):

        page.clean()

        page.add(
            build_configuracion(
                page,
                on_back=lambda: show_home()
            )
        )

        page.update()

    page.add(build_login(page, show_home))


if __name__ == "__main__":
    ft.run(main)

def hola(): # Recuerdo de amigo Linux ayudando
    print("hola mundo")

    #jhon linux