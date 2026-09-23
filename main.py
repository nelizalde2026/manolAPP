# import flet as ft
# from pantallas.admin_usuarios import crear_vista_admin_usuarios
# from pantallas.login import crear_pantalla_login
# from pantallas.quedadas import crear_vista_quedadas
# from pantallas.gastos import crear_vista_gastos
# from pantallas.perfil import crear_vista_perfil


# def main(page: ft.Page):
#     page.title = "ManolAPP"
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.bgcolor = "#FFF0F3"
#     page.vertical_alignment = ft.MainAxisAlignment.START

#     # Comentamos esto por si la imagen no existe en la ruta y bloquea el arranque
#     # page.window.icon = "manologo.jpg"

#     # Paleta de colores oficial adaptada
#     COLOR_ROSA_FUERTE = "#641a18"
#     COLOR_ROJO = "#b30819"
#     COLOR_ROJO_OSCURO = "#641a18"
#     COLOR_FONDO_TARJETA = "#ebe9ea"  # Gris-blanco para la tarjeta de contenido
#     COLOR_BORDE = "#773737"
#     COLOR_TEXTO = "#641918"
#     COLOR_FONDO_EXTERIOR = "#641a18"  # Granate exterior para el fondo

#     usuario_actual = {"nombre": ""}
#     amigas_grupo = []

#     vista_principal = ft.Container(expand=True)

#     # Instanciar las vistas de las pestañas
#     tab_quedadas, actualizar_quedadas = crear_vista_quedadas(
#         page,
#         usuario_actual,
#         COLOR_ROJO_OSCURO,
#         COLOR_TEXTO,
#         COLOR_ROSA_FUERTE,
#         COLOR_ROJO,
#         COLOR_BORDE,
#         COLOR_FONDO_TARJETA,
#     )
#     tab_gastos, actualizar_gastos = crear_vista_gastos(
#         page,
#         usuario_actual,
#         vista_principal,
#         COLOR_ROJO_OSCURO,
#         COLOR_TEXTO,
#         COLOR_ROSA_FUERTE,
#         COLOR_ROJO,
#         COLOR_BORDE,
#         COLOR_FONDO_TARJETA,
#     )
#     tab_perfil, actualizar_perfil = crear_vista_perfil(
#         page,
#         usuario_actual,
#         lambda: reiniciar_sesion(),
#         COLOR_ROJO_OSCURO,
#         COLOR_TEXTO,
#         COLOR_ROSA_FUERTE,
#         COLOR_ROJO,
#         COLOR_BORDE,
#         COLOR_FONDO_TARJETA,
#     )

#     tab_admin, actualizar_admin = crear_vista_admin_usuarios(
#         page,
#         usuario_actual,
#         amigas_grupo,
#         COLOR_ROJO_OSCURO,
#         COLOR_TEXTO,
#         COLOR_ROSA_FUERTE,
#         COLOR_ROJO,
#         COLOR_BORDE,
#         COLOR_FONDO_TARJETA,
#     )

#     def cambiar_pestana(e):
#         indice = e.control.selected_index
#         if indice == 0:
#             vista_principal.content = tab_quedadas
#         elif indice == 1:
#             vista_principal.content = tab_gastos
#         elif indice == 2:
#             vista_principal.content = tab_perfil
#             actualizar_perfil()
#         elif indice == 3 and usuario_actual.get("es_admin", False):
#             vista_principal.content = tab_admin
#             actualizar_admin()
#         page.update()

#     def cargar_pantalla_principal():
#         destinos = [
#             ft.NavigationBarDestination(icon=ft.Icons.EVENT_NOTE, label="Quedadas"),
#             ft.NavigationBarDestination(icon=ft.Icons.RECEIPT_LONG, label="Gastos"),
#             ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Mi Perfil"),
#         ]

#         if usuario_actual.get("es_admin", False):
#             destinos.append(
#                 ft.NavigationBarDestination(
#                     icon=ft.Icons.ADMIN_PANEL_SETTINGS, label="Admin"
#                 )
#             )

#         page.navigation_bar = ft.NavigationBar(
#             destinations=destinos,
#             on_change=cambiar_pestana,
#             bgcolor="#FFF0F3",
#             indicator_color=COLOR_ROSA_FUERTE,
#         )
#         actualizar_quedadas()
#         vista_principal.content = tab_quedadas
#         page.update()

#     def reiniciar_sesion():
#         usuario_actual["nombre"] = ""
#         page.navigation_bar = None
#         vista_principal.content = pantalla_login
#         page.update()

#     pantalla_login = crear_pantalla_login(
#         page,
#         usuario_actual,
#         amigas_grupo,
#         cargar_pantalla_principal,
#         COLOR_ROJO_OSCURO,
#         COLOR_TEXTO,
#         COLOR_ROSA_FUERTE,
#         COLOR_ROJO,
#     )

#     vista_principal.content = pantalla_login
#     page.add(vista_principal)


# # Usar ft.app en lugar de ft.run suele ser más estable en la mayoría de entornos locales
# if __name__ == "__main__":
#     ft.run(main)


import flet as ft
from pantallas.admin_usuarios import crear_vista_admin_usuarios
from pantallas.login import crear_pantalla_login
from pantallas.quedadas import crear_vista_quedadas
from pantallas.gastos import crear_vista_gastos
from pantallas.perfil import crear_vista_perfil


def main(page: ft.Page):
    page.title = "ManolAPP (Modo Pruebas)"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#FFF0F3"
    page.vertical_alignment = ft.MainAxisAlignment.START

    # 1. USUARIO DE PRUEBA (Asignamos datos para saltarnos el login)
    # Cambia 'es_admin': True si quieres probar también la pestaña de Administrador
    usuario_actual = {"nombre": "Manola de Prueba", "es_admin": True}

    # Si tu función obtener_amigas() requiere una lista global, puedes precargarla aquí o dejarla vacía
    amigas_grupo = ["Manola de Prueba", "Amiga 1", "Amiga 2"]

    COLOR_ROSA_FUERTE = "#641a18"
    COLOR_ROJO = "#b30819"
    COLOR_ROJO_OSCURO = "#641a18"
    COLOR_FONDO_TARJETA = "#80ebebeb"
    COLOR_BORDE = "#773737"
    COLOR_TEXTO = "#641918"

    vista_principal = ft.Container(expand=True)

    # Instanciar las vistas de las pestañas
    tab_quedadas, actualizar_quedadas = crear_vista_quedadas(
        page,
        usuario_actual,
        COLOR_ROJO_OSCURO,
        COLOR_TEXTO,
        COLOR_ROSA_FUERTE,
        COLOR_ROJO,
        COLOR_BORDE,
        COLOR_FONDO_TARJETA,
    )
    tab_gastos, actualizar_gastos = crear_vista_gastos(
        page,
        usuario_actual,
        vista_principal,
        COLOR_ROJO_OSCURO,
        COLOR_TEXTO,
        COLOR_ROSA_FUERTE,
        COLOR_ROJO,
        COLOR_BORDE,
        COLOR_FONDO_TARJETA,
    )
    tab_perfil, actualizar_perfil = crear_vista_perfil(
        page,
        usuario_actual,
        lambda: reiniciar_sesion(),
        COLOR_ROJO_OSCURO,
        COLOR_TEXTO,
        COLOR_ROSA_FUERTE,
        COLOR_ROJO,
        COLOR_BORDE,
        COLOR_FONDO_TARJETA,
    )

    tab_admin, actualizar_admin = crear_vista_admin_usuarios(
        page,
        usuario_actual,
        amigas_grupo,
        COLOR_ROJO_OSCURO,
        COLOR_TEXTO,
        COLOR_ROSA_FUERTE,
        COLOR_ROJO,
        COLOR_BORDE,
        COLOR_FONDO_TARJETA,
    )

    def cambiar_pestana(e):
        indice = e.control.selected_index
        if indice == 0:
            vista_principal.content = tab_quedadas
            actualizar_quedadas()
        elif indice == 1:
            vista_principal.content = tab_gastos
            actualizar_gastos()
        elif indice == 2:
            vista_principal.content = tab_perfil
            actualizar_perfil()
        elif indice == 3 and usuario_actual.get("es_admin", False):
            vista_principal.content = tab_admin
            actualizar_admin()
        page.update()

    def cargar_pantalla_principal():
        destinos = [
            ft.NavigationBarDestination(icon=ft.Icons.EVENT_NOTE, label="Quedadas"),
            ft.NavigationBarDestination(icon=ft.Icons.RECEIPT_LONG, label="Gastos"),
            ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Mi Perfil"),
        ]

        if usuario_actual.get("es_admin", False):
            destinos.append(
                ft.NavigationBarDestination(
                    icon=ft.Icons.ADMIN_PANEL_SETTINGS, label="Admin"
                )
            )

        page.navigation_bar = ft.NavigationBar(
            destinations=destinos,
            on_change=cambiar_pestana,
            bgcolor="#FFF0F3",
            indicator_color=COLOR_ROSA_FUERTE,
        )
        actualizar_quedadas()
        vista_principal.content = tab_quedadas
        page.add(vista_principal)
        page.update()

    def reiniciar_sesion():
        # Si en algún momento quieres volver al login manualmente
        usuario_actual["nombre"] = ""
        page.navigation_bar = None
        vista_principal.content = pantalla_login
        page.update()

    # Dejamos creado el login por si acaso se llama a reiniciar_sesion
    pantalla_login = crear_pantalla_login(
        page,
        usuario_actual,
        amigas_grupo,
        cargar_pantalla_principal,
        COLOR_ROJO_OSCURO,
        COLOR_TEXTO,
        COLOR_ROSA_FUERTE,
        COLOR_ROJO,
    )

    # 2. ARRANCAR DIRECTAMENTE EN LA PANTALLA PRINCIPAL
    cargar_pantalla_principal()


if __name__ == "__main__":
    ft.run(main)
