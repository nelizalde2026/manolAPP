import flet as ft
from database import actualizar_perfil_amiga, obtener_quedadas, obtener_actividades
from modals import mostrar_alerta  # Importamos tu módulo centralizado de modales


def crear_vista_perfil(
    page,
    usuario_actual,
    on_logout,
    COLOR_ROJO_OSCURO,
    COLOR_TEXTO,
    COLOR_ROSA_FUERTE,
    COLOR_ROJO,
    COLOR_BORDE,
    COLOR_FONDO_TARJETA,
):
    # Campos de texto mejorados y estilizados con fondo blanco para mayor nitidez
    txt_nombre_usuario = ft.TextField(
        label="Nombre de usuario",
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        color=COLOR_TEXTO,
        bgcolor="white",
        border_radius=8,
    )
    txt_nombre_completo = ft.TextField(
        label="Nombre completo",
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        color=COLOR_TEXTO,
        bgcolor="white",
        border_radius=8,
    )
    txt_email = ft.TextField(
        label="Correo electrónico",
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        color=COLOR_TEXTO,
        bgcolor="white",
        border_radius=8,
    )
    txt_password = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        color=COLOR_TEXTO,
        bgcolor="white",
        border_radius=8,
    )
    txt_foto = ft.TextField(
        label="URL de tu foto de perfil",
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        color=COLOR_TEXTO,
        bgcolor="white",
        border_radius=8,
    )

    # Contenedor interno con scroll para que el contenido fluya ordenadamente
    contenido_perfil = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    def guardar_perfil(e):
        nuevo_usuario = txt_nombre_usuario.value.strip()
        nuevo_completo = txt_nombre_completo.value.strip()
        nuevo_email = txt_email.value.strip()
        nueva_password = txt_password.value.strip()
        nueva_foto = txt_foto.value.strip()

        if (
            not nuevo_usuario
            or not nuevo_completo
            or not nuevo_email
            or not nueva_password
        ):
            mostrar_alerta(
                page=page,
                titulo="¡Atención! ⚠️",
                mensaje="Por favor, rellena todos los campos obligatorios.",
                es_exito=False,
            )
            return

        nombre_antiguo = usuario_actual["nombre"]

        # Llamada a la base de datos
        exito, mensaje = actualizar_perfil_amiga(
            nombre_antiguo,
            nuevo_usuario,
            nuevo_completo,
            nuevo_email,
            nueva_password,
            nueva_foto,
        )

        if exito:
            usuario_actual["nombre"] = nuevo_usuario
            usuario_actual["nombre_completo"] = nuevo_completo
            usuario_actual["email"] = nuevo_email
            usuario_actual["password"] = nueva_password
            usuario_actual["foto"] = nueva_foto

            mostrar_alerta(
                page=page,
                titulo="¡Perfil Actualizado! ✨",
                mensaje=mensaje,
                es_exito=True,
                on_close=actualizar_pantalla_perfil,
            )
        else:
            mostrar_alerta(page=page, titulo="Error", mensaje=mensaje, es_exito=False)

        page.update()

    def actualizar_pantalla_perfil():
        txt_nombre_usuario.value = usuario_actual.get("nombre", "")
        txt_nombre_completo.value = usuario_actual.get("nombre_completo", "")
        txt_email.value = usuario_actual.get("email", "")
        txt_password.value = usuario_actual.get("password", "")
        txt_foto.value = usuario_actual.get("foto", "")

        quedadas = obtener_quedadas()
        actividades = obtener_actividades()

        planes_apuntada = sum(
            1
            for p in quedadas
            if any(
                a["amiga"] == usuario_actual["nombre"] for a in p.get("asistentes", [])
            )
        )
        actividades_creadas = sum(
            1
            for a in actividades
            if any(
                p["amiga"] == usuario_actual["nombre"]
                for p in a.get("participantes_actividad", [])
            )
        )

        contenido_perfil.controls = [
            ft.Row(
                [
                    ft.Icon(ft.Icons.PERSON_OUTLINE, color=COLOR_ROJO_OSCURO, size=22),
                    ft.Text(
                        "Configuración de tu Perfil",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_ROJO_OSCURO,
                    ),
                ],
                spacing=8,
            ),
            ft.Text(
                "Modifica tus datos personales y credenciales:",
                color=COLOR_TEXTO,
                size=12,
            ),
            ft.Divider(color=COLOR_BORDE),
            txt_nombre_usuario,
            txt_nombre_completo,
            txt_email,
            txt_password,
            txt_foto,
            ft.Button(
                "Guardar Cambios 💾",
                on_click=guardar_perfil,
                style=ft.ButtonStyle(
                    bgcolor=COLOR_ROJO,
                    color="white",
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            ),
            ft.Divider(color=COLOR_BORDE),
            ft.Row(
                [
                    ft.Icon(ft.Icons.AUTO_AWESOME, color=COLOR_ROJO_OSCURO, size=20),
                    ft.Text(
                        "Tus Estadísticas en el Grupo:",
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_ROJO_OSCURO,
                    ),
                ],
                spacing=8,
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(
                                    ft.Icons.EVENT_AVAILABLE, color=COLOR_ROJO
                                ),
                                title=ft.Text(
                                    f"Planes apuntada: {planes_apuntada}",
                                    weight=ft.FontWeight.BOLD,
                                    color=COLOR_ROJO_OSCURO,
                                ),
                                subtitle=ft.Text(
                                    f"Actividades de gastos asociadas: {actividades_creadas}",
                                    color=COLOR_TEXTO,
                                    size=12,
                                ),
                            )
                        ],
                        spacing=0,
                    ),
                    padding=8,
                ),
                bgcolor="white",
                elevation=1,
            ),
            ft.Container(height=5),
            ft.OutlinedButton(
                "Cerrar Sesión 🚪",
                on_click=lambda e: on_logout(),
                style=ft.ButtonStyle(
                    color=COLOR_ROJO, side=ft.BorderSide(1, COLOR_ROJO)
                ),
            ),
        ]
        page.update()

    # 1. Tarjeta central gris-blanca donde se organiza todo el contenido de la vista
    tarjeta_central = ft.Container(
        content=contenido_perfil,
        bgcolor=COLOR_FONDO_TARJETA,  # #F0F0F2 (Gris-blanco)
        padding=25,
        border_radius=16,
        # border=ft.Border(
        #     top=ft.BorderSide(1, COLOR_BORDE),
        #     bottom=ft.BorderSide(1, COLOR_BORDE),
        #     left=ft.BorderSide(1, COLOR_BORDE),
        #     right=ft.BorderSide(1, COLOR_BORDE),
        # ),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=12, color="#33000000"),
        width=500,
        expand=True,
    )

    # 2. Contenedor principal con el color granate base y la imagen de fondo manologo.jpg
    contenedor_principal = ft.Container(
        content=tarjeta_central,
        bgcolor=COLOR_ROJO_OSCURO,
        image=ft.DecorationImage(
            src="manologo.jpg",
            fit="cover",
        ),
        alignment=ft.Alignment(0, 0),
        padding=20,
        expand=True,
    )

    return contenedor_principal, actualizar_pantalla_perfil
