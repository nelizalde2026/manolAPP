import flet as ft
from database import obtener_amigas, admin_crear_amiga


def crear_vista_admin_usuarios(
    page,
    usuario_actual,
    amigas_grupo,
    COLOR_ROJO_OSCURO,
    COLOR_TEXTO,
    COLOR_ROSA_FUERTE,
    COLOR_ROJO,
    COLOR_BORDE,
    COLOR_FONDO_TARJETA,
):
    # Campos para crear una nueva amiga
    txt_nuevo_user = ft.TextField(
        label="Nombre de usuario",
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        expand=True,
    )
    txt_nuevo_completo = ft.TextField(
        label="Nombre completo",
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        expand=True,
    )
    txt_nuevo_email = ft.TextField(
        label="Email",
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        expand=True,
    )
    txt_nuevo_pass = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        expand=True,
    )
    chk_es_admin = ft.Checkbox(label="¿Es Administradora?", value=False)

    lbl_mensaje = ft.Text("", size=13)
    lista_amigas_columna = ft.Column(spacing=10)

    contenido_admin = ft.Column(expand=True, spacing=15, scroll=ft.ScrollMode.AUTO)

    def registrar_amiga(e):
        user = txt_nuevo_user.value.strip()
        completo = txt_nuevo_completo.value.strip()
        email = txt_nuevo_email.value.strip()
        password = txt_nuevo_pass.value.strip()
        es_admin = chk_es_admin.value

        if not user or not completo or not email or not password:
            lbl_mensaje.color = COLOR_ROJO
            lbl_mensaje.value = "Rellena todos los campos para crear la cuenta."
            page.update()
            return

        from database import supabase

        try:
            supabase.table("amigas").insert(
                {
                    "nombre_usuario": user,
                    "nombre_completo": completo,
                    "email": email,
                    "password": password,
                    "es_admin": es_admin,
                    "foto": "",
                }
            ).execute()

            lbl_mensaje.color = ft.Colors.GREEN_700
            lbl_mensaje.value = f"¡Amiga {user} creada con éxito! ✨"

            # Limpiar campos
            txt_nuevo_user.value = ""
            txt_nuevo_completo.value = ""
            txt_nuevo_email.value = ""
            txt_nuevo_pass.value = ""
            chk_es_admin.value = False

            actualizar_pantalla_admin()
        except Exception as ex:
            lbl_mensaje.color = COLOR_ROJO
            lbl_mensaje.value = f"Error: {str(ex)}"

        page.update()

    def actualizar_pantalla_admin():
        from database import supabase

        try:
            res = supabase.table("amigas").select("*").execute()
            amigas_lista = res.data
        except Exception:
            amigas_lista = []

        tarjetas_amigas = []
        for amiga in amigas_lista:
            es_adm = amiga.get("es_admin", False)
            rol = "👑 Admin" if es_adm else "🌸 Manola"

            tarjetas_amigas.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.PERSON, color=COLOR_ROJO),
                            title=ft.Text(
                                f"{amiga.get('nombre_completo', '')} ({amiga.get('nombre_usuario', '')})",
                                weight=ft.FontWeight.BOLD,
                                color=COLOR_ROJO_OSCURO,
                            ),
                            subtitle=ft.Text(
                                f"{amiga.get('email', '')} • {rol}", color=COLOR_TEXTO
                            ),
                        ),
                        padding=10,
                    ),
                    bgcolor=COLOR_FONDO_TARJETA,
                    elevation=1,
                )
            )

        lista_amigas_columna.controls = tarjetas_amigas

        # Construcción de los elementos internos dentro del panel
        contenido_admin.controls = [
            ft.Row(
                [
                    ft.Image(
                        src="manologo.jpg",
                        width=70,
                        height=70,
                        fit="contain",
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(
                "Panel de Administración de Manolas",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=COLOR_ROJO_OSCURO,
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Text(
                "Crea nuevas cuentas para las amigas del club:",
                color=COLOR_TEXTO,
                size=13,
            ),
            ft.Divider(color=COLOR_BORDE),
            txt_nuevo_user,
            txt_nuevo_completo,
            txt_nuevo_email,
            txt_nuevo_pass,
            chk_es_admin,
            ft.Button(
                "Crear Cuenta de Manola",
                on_click=registrar_amiga,
                style=ft.ButtonStyle(bgcolor=COLOR_ROJO, color=ft.Colors.WHITE),
            ),
            lbl_mensaje,
            ft.Divider(color=COLOR_BORDE),
            ft.Text(
                "Lista de Manolas:",
                weight=ft.FontWeight.BOLD,
                color=COLOR_ROJO_OSCURO,
            ),
            lista_amigas_columna,
        ]
        page.update()

    # Contenedor principal con el fondo granate y la imagen decorativa corporativa
    tarjeta_central = ft.Card(
        content=ft.Container(
            content=contenido_admin,
            padding=20,
            bgcolor=COLOR_FONDO_TARJETA,
            border_radius=10,
        ),
        elevation=4,
        expand=True,
    )

    contenedor = ft.Container(
        content=tarjeta_central,
        bgcolor=COLOR_ROJO_OSCURO,
        image=ft.DecorationImage(
            src="manologo.jpg",
            fit="cover",
            opacity=0.15,  # Sutil transparencia para que luzca elegante con el granate
        ),
        alignment=ft.Alignment(0, 0),
        padding=20,
        expand=True,
    )

    # Forzar la carga inicial de los datos y el diseño
    actualizar_pantalla_admin()

    return contenedor, actualizar_pantalla_admin
