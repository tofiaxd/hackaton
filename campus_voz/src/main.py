import flet as ft
from home import build_home
from login import build_login
import themes


def main(page: ft.Page):

    # Mantiene una vista tipo teléfono al abrir la aplicación.
    page.window.width = 390
    page.window.height = 830
    page.window.resizable = True

    page.window.center()

    page.title = "Campus Access"
    page.theme_mode = ft.ThemeMode.LIGHT

    page.theme = themes.APP_THEME
    page.padding = 0
    page.bgcolor = themes.BACKGROUND

    def show_home(name):
        page.clean()
        page.add(build_home(page, name))
        page.update()

    page.add(build_login(page, show_home))


if __name__ == "__main__":
    ft.run(main)


def hola(): # Recuerdo de amigo Linux ayudando
    print("hola mundo")

    #jhon linux