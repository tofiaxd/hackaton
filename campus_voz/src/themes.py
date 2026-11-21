
import flet as ft

# ==================================
# PALETA DE COLORES - CAMPUS ACCESS
# ==================================

PRIMARY = "#0215C2"       # Verde principal
SECONDARY = "#1E88E5"     # Verde secundario
ACCENT = "#F2B84B"        # Amarillo de acento

BACKGROUND = "#F5F7F2"    # Fondo general
SURFACE = "#FFFFFF"       # Tarjetas y contenedores

TEXT_PRIMARY = "#26332A"  # Texto principal
TEXT_SECONDARY = "#68756B" # Texto secundario

ERROR = "#D9534F"         # Alertas
SUCCESS = "#398653"       # Confirmaciones


# ==================================
# TEMA GLOBAL
# ==================================

APP_THEME = ft.Theme(
    color_scheme=ft.ColorScheme(
        primary=PRIMARY,
        secondary=SECONDARY,
        surface=SURFACE,
        error=ERROR,
    ),
)
