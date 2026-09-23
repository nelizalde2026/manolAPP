import flet as ft
from database import obtener_amigas


def crear_pantalla_login(
    page,
    usuario_actual,
    amigas_grupo,
    on_login_success,
    COLOR_ROJO_OSCURO,
    COLOR_TEXTO,
    COLOR_ROSA_FUERTE,
    COLOR_ROJO,
):
    txt_usuario = ft.TextField(
        label="Nombre de usuario",
        width=300,
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
    )

    txt_password = ft.TextField(
        label="Contraseña",
        width=300,
        password=True,
        can_reveal_password=True,
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
    )

    error_login = ft.Text("", color=COLOR_ROJO, size=13)

    def entrar_app(e):
        usuario = txt_usuario.value.strip()
        password = txt_password.value.strip()

        if not usuario or not password:
            error_login.value = "Introduce tu usuario y contraseña."
            page.update()
            return

        from database import supabase

        res = (
            supabase.table("amigas").select("*").eq("nombre_usuario", usuario).execute()
        )

        if res.data:
            datos_usuario = res.data[0]
            if datos_usuario.get("password") == password:
                usuario_actual["nombre"] = datos_usuario["nombre_usuario"]
                usuario_actual["nombre_completo"] = datos_usuario["nombre_completo"]
                usuario_actual["email"] = datos_usuario["email"]
                usuario_actual["foto"] = datos_usuario.get("foto", "")
                usuario_actual["es_admin"] = datos_usuario.get("es_admin", False)

                amigas_actuales = obtener_amigas()
                amigas_grupo.clear()
                amigas_grupo.extend(amigas_actuales)

                on_login_success()
            else:
                error_login.value = "Contraseña incorrecta ❌"
                page.update()
        else:
            error_login.value = (
                "El usuario no existe. Pídele al admin que te cree una cuenta."
            )
            page.update()

    # Tarjeta central gris-blanca elegante
    tarjeta_login = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "manolaAPP",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=COLOR_ROJO_OSCURO,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Inicia sesión con tus datos:",
                    size=13,
                    color=COLOR_TEXTO,
                ),
                txt_usuario,
                txt_password,
                ft.Button(
                    "Entrar",
                    on_click=entrar_app,
                    style=ft.ButtonStyle(
                        bgcolor=COLOR_ROJO,
                        color="white",  # Usamos string plano en lugar de ft.colors
                        shape=ft.RoundedRectangleBorder(radius=10),
                    ),
                    width=300,
                ),
                error_login,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        bgcolor="#F4F4F6",  # Tono gris-blanco suave
        padding=40,
        border_radius=16,
        border=ft.Border(
            top=ft.BorderSide(1, "#641a18"),
            bottom=ft.BorderSide(1, "641a18"),
            left=ft.BorderSide(1, "#641a18"),
            right=ft.BorderSide(1, "#641a18"),
        ),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color="#22000000",  # Sombra sutil usando código hexadecimal con transparencia
        ),
    )

    # Contenedor principal con la imagen de fondo y la tarjeta centrada
    return ft.Container(
        content=tarjeta_login,
        image=ft.DecorationImage(
            src="manologo.jpg",
            fit="cover",  # Usamos el string directamente en lugar de un enum
        ),
        alignment=ft.Alignment(0, 0),
        expand=True,
    )
