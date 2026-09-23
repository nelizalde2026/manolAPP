from datetime import datetime, timedelta
import flet as ft
from database import (
    apuntarse_plan_fijo,
    crear_quedada_con_tipo,
    eliminar_quedada,
    guardar_disponibilidad,
    obtener_disponibilidad_quedada,
    obtener_quedadas,
)


def crear_vista_quedadas(
    page,
    usuario_actual,
    COLOR_ROJO_OSCURO,
    COLOR_TEXTO,
    COLOR_ROSA_FUERTE,
    COLOR_ROJO,
    COLOR_BORDE,
    COLOR_FONDO_TARJETA,
):
    # Contenedor interno con scroll para que el contenido fluya ordenadamente
    contenido_principal = ft.Column(
        spacing=15,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    # 1. PRIMERO: Definir los elementos de texto y mensajes para que existan
    lbl_mensaje = ft.Text("", size=13)
    lbl_rango_seleccionado = ft.Text(
        "Ningún rango seleccionado", size=12, italic=True, color=COLOR_TEXTO
    )
    lista_quedadas_col = ft.Column(spacing=15)

    # 2. SEGUNDO: Campos de texto estilizados con fondo blanco para mayor nitidez
    txt_titulo = ft.TextField(
        label="Título del Plan",
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        color=COLOR_TEXTO,
        bgcolor="white",
        border_radius=8,
    )
    txt_desc = ft.TextField(
        label="Descripción o detalles",
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        color=COLOR_TEXTO,
        bgcolor="white",
        border_radius=8,
        multiline=True,
    )
    txt_fecha_fija = ft.TextField(
        label="Fecha y hora (Ej: Viernes a las 20:00)",
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        color=COLOR_TEXTO,
        bgcolor="white",
        border_radius=8,
    )

    # Botones y elementos del sondeo con estética unificada
    btn_sel_inicio = ft.Button(
        "📅 Seleccionar Fecha Inicio",
        icon=ft.Icons.CALENDAR_MONTH,
        color="white",
        bgcolor=COLOR_ROSA_FUERTE,
        style=ft.ButtonStyle(bgcolor=COLOR_ROSA_FUERTE, color="white"),
    )
    btn_sel_fin = ft.Button(
        "📅 Seleccionar Fecha Fin",
        icon=ft.Icons.CALENDAR_MONTH,
        color="white",
        bgcolor=COLOR_ROSA_FUERTE,
        style=ft.ButtonStyle(bgcolor=COLOR_ROSA_FUERTE, color="white"),
    )

    date_picker_inicio = ft.DatePicker(
        first_date=datetime.now(),
        last_date=datetime.now() + timedelta(days=365),
    )
    date_picker_fin = ft.DatePicker(
        first_date=datetime.now(),
        last_date=datetime.now() + timedelta(days=365),
    )

    page.overlay.extend([date_picker_inicio, date_picker_fin])

    btn_sel_inicio.on_click = lambda _: page.show_dialog(date_picker_inicio)
    btn_sel_fin.on_click = lambda _: page.show_dialog(date_picker_fin)

    def actualizar_texto_rango():
        ini = (
            date_picker_inicio.value.strftime("%Y-%m-%d")
            if date_picker_inicio.value
            else ""
        )
        fin = (
            date_picker_fin.value.strftime("%Y-%m-%d") if date_picker_fin.value else ""
        )
        if ini and fin:
            lbl_rango_seleccionado.value = f"Rango activo: {ini} al {fin}"
        elif ini:
            lbl_rango_seleccionado.value = (
                f"Rango activo: desde {ini} (falta elegir fin)"
            )
        elif fin:
            lbl_rango_seleccionado.value = (
                f"Rango activo: hasta {fin} (falta elegir inicio)"
            )
        else:
            lbl_rango_seleccionado.value = "Ningún rango seleccionado"

    def on_inicio_change(e):
        if date_picker_inicio.value:
            f_str = date_picker_inicio.value.strftime("%Y-%m-%d")
            btn_sel_inicio.text = f"Inicio: {f_str}"
            btn_sel_inicio.style = ft.ButtonStyle(bgcolor=COLOR_ROJO, color="white")
            actualizar_texto_rango()
        page.update()

    def on_fin_change(e):
        if date_picker_fin.value:
            f_str = date_picker_fin.value.strftime("%Y-%m-%d")
            btn_sel_fin.text = f"Fin: {f_str}"
            btn_sel_fin.style = ft.ButtonStyle(bgcolor=COLOR_ROJO, color="white")
            actualizar_texto_rango()
        page.update()

    date_picker_inicio.on_change = on_inicio_change
    date_picker_fin.on_change = on_fin_change

    contenedor_fechas_sondeo = ft.Column(
        [ft.Row([btn_sel_inicio, btn_sel_fin], spacing=10), lbl_rango_seleccionado],
        spacing=5,
    )

    contenedor_dinamico_fecha = ft.Container()

    def cambiar_tipo_plan(e):
        es_sondeo = radio_tipo_plan.value == "sondeo"
        if es_sondeo:
            contenedor_dinamico_fecha.content = contenedor_fechas_sondeo
        else:
            contenedor_dinamico_fecha.content = txt_fecha_fija
        contenedor_dinamico_fecha.update()

    radio_tipo_plan = ft.RadioGroup(
        content=ft.Row(
            [
                ft.Radio(
                    value="fijo", label="📅 Fecha y hora fija", active_color=COLOR_ROJO
                ),
                ft.Radio(
                    value="sondeo",
                    label="📊 Sondeo (Calendario)",
                    active_color=COLOR_ROJO,
                ),
            ]
        ),
        value="fijo",
        on_change=cambiar_tipo_plan,
    )

    contenedor_dinamico_fecha = ft.Container(content=txt_fecha_fija)

    def guardar_nuevo_plan(e):
        titulo = txt_titulo.value.strip()
        desc = txt_desc.value.strip()
        tipo = radio_tipo_plan.value

        if tipo == "sondeo":
            if not date_picker_inicio.value or not date_picker_fin.value:
                lbl_mensaje.color = COLOR_ROJO
                lbl_mensaje.value = (
                    "Debes seleccionar las fechas de inicio y fin en el calendario."
                )
                page.update()
                return

            f_inicio = date_picker_inicio.value.strftime("%Y-%m-%d")
            f_fin = date_picker_fin.value.strftime("%Y-%m-%d")
            fecha_texto = f"{f_inicio} al {f_fin}"
        else:
            fecha_texto = txt_fecha_fija.value.strip()

        if not titulo or not fecha_texto:
            lbl_mensaje.color = COLOR_ROJO
            lbl_mensaje.value = "El título y las fechas son obligatorios."
            page.update()
            return

        exito, msg = crear_quedada_con_tipo(
            titulo=titulo,
            descripcion=desc,
            fecha_fija=fecha_texto,
            tipo_plan=tipo,
            creadora=usuario_actual.get("nombre", "Anónima"),
        )

        if exito:
            lbl_mensaje.color = "green"
            lbl_mensaje.value = msg
            txt_titulo.value = ""
            txt_desc.value = ""
            txt_fecha_fija.value = ""
            date_picker_inicio.value = None
            date_picker_fin.value = None
            btn_sel_inicio.text = "📅 Seleccionar Fecha Inicio"
            btn_sel_inicio.style = ft.ButtonStyle(
                bgcolor=COLOR_ROSA_FUERTE, color="white"
            )
            btn_sel_fin.text = "📅 Seleccionar Fecha Fin"
            btn_sel_fin.style = ft.ButtonStyle(bgcolor=COLOR_ROSA_FUERTE, color="white")
            lbl_rango_seleccionado.value = "Ningún rango seleccionado"

            radio_tipo_plan.value = "fijo"
            contenedor_dinamico_fecha.content = txt_fecha_fija

            actualizar_pantalla()
        else:
            lbl_mensaje.color = COLOR_ROJO
            lbl_mensaje.value = msg

        page.update()

    def abrir_detalle_sondeo(quedada):
        id_q = quedada["id"]
        titulo_q = quedada["titulo"]
        rango_texto = quedada.get("fecha", "")

        dias_a_votar = []
        try:
            partes = rango_texto.split(" al ")
            if len(partes) == 2:
                f_ini = datetime.strptime(partes[0].strip(), "%Y-%m-%d")
                f_fin = datetime.strptime(partes[1].strip(), "%Y-%m-%d")

                delta = f_fin - f_ini
                dias_a_votar = [
                    f_ini + timedelta(days=i) for i in range(delta.days + 1)
                ]
        except Exception:
            pass

        if not dias_a_votar:
            hoy = datetime.now()
            dias_a_votar = [hoy + timedelta(days=i) for i in range(7)]

        disp_actuales = obtener_disponibilidad_quedada(id_q)

        controles_votacion: list[ft.Control] = []
        switches_dias = {}

        for dia in dias_a_votar:
            fecha_str = dia.strftime("%Y-%m-%d")
            nombre_dia = dia.strftime("%d/%m (%A)")

            voto_previo = next(
                (
                    d
                    for d in disp_actuales
                    if str(d.get("amiga", "")).strip()
                    == str(usuario_actual["nombre"]).strip()
                    and str(d.get("fecha", ""))[:10] == fecha_str
                ),
                None,
            )

            val_inicial = False
            if voto_previo:
                val = voto_previo.get("disponible")
                val_inicial = val is True or val == "true" or val == 1

            sw = ft.Switch(value=val_inicial, active_color=COLOR_ROJO)
            switches_dias[fecha_str] = sw

            controles_votacion.append(
                ft.Row(
                    [
                        ft.Text(
                            nombre_dia,
                            width=130,
                            color=COLOR_TEXTO,
                            weight=ft.FontWeight.W_500,
                        ),
                        sw,
                        ft.Text("Sí puedo ✨", size=12, color=COLOR_ROJO_OSCURO),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )

        def guardar_mis_votos(e):
            for fecha_str, sw in switches_dias.items():
                guardar_disponibilidad(
                    id_quedada=id_q,
                    amiga=usuario_actual["nombre"],
                    fecha=fecha_str,
                    disponible=sw.value,
                )

            lbl_mensaje.color = "green"
            lbl_mensaje.value = "¡Tus disponibilidades se han guardado con éxito! 💖"
            actualizar_pantalla()
            page.update()

        resumen_colores: list[ft.Control] = []
        disp_actuales_refresacadas = obtener_disponibilidad_quedada(id_q)

        votos_por_fecha = {}
        for d in disp_actuales_refresacadas:
            disp = d.get("disponible")
            if disp is True or disp == "true" or disp == 1:
                f = str(d.get("fecha", ""))[:10]
                if f not in votos_por_fecha:
                    votos_por_fecha[f] = []
                nombre_amiga = str(d.get("amiga", "")).strip()
                if nombre_amiga and nombre_amiga not in votos_por_fecha[f]:
                    votos_por_fecha[f].append(nombre_amiga)

        for dia in dias_a_votar:
            fecha_str = dia.strftime("%Y-%m-%d")
            nombre_dia = dia.strftime("%d/%m (%A)")
            amigas_que_pueden = votos_por_fecha.get(fecha_str, [])

            chips_amigas: list[ft.Control] = (
                [
                    ft.Container(
                        content=ft.Text(amiga, size=11, color="white"),
                        bgcolor=COLOR_ROSA_FUERTE,
                        padding=8,
                        border_radius=10,
                    )
                    for amiga in amigas_que_pueden
                ]
                if amigas_que_pueden
                else [ft.Text("Nadie apuntado aún", size=11, italic=True, color="grey")]
            )

            resumen_colores.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    nombre_dia,
                                    weight=ft.FontWeight.BOLD,
                                    color=COLOR_ROJO_OSCURO,
                                ),
                                ft.Row(chips_amigas, wrap=True, spacing=5),
                            ],
                            spacing=5,
                        ),
                        padding=10,
                    ),
                    bgcolor="white",
                    elevation=1,
                )
            )

        elementos_estadistica: list[ft.Control] = [
            ft.Row(
                [
                    ft.Icon(ft.Icons.AUTO_GRAPH, color=COLOR_ROSA_FUERTE, size=20),
                    ft.Text(
                        "Resumen del Sondeo",
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_ROJO_OSCURO,
                    ),
                ],
                spacing=8,
            )
        ]

        if votos_por_fecha:
            max_amigas = 0
            for f_str, lista_amigas in votos_por_fecha.items():
                if len(lista_amigas) > max_amigas:
                    max_amigas = len(lista_amigas)

            if max_amigas > 0:
                mejores_fechas_str = [
                    f
                    for f, amigas in votos_por_fecha.items()
                    if len(amigas) == max_amigas
                ]

                elementos_estadistica.append(
                    ft.Text(
                        f"🏆 Coincidencia máxima ({max_amigas} personas):",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_TEXTO,
                    )
                )

                for f_str in mejores_fechas_str:
                    dt_obj = datetime.strptime(f_str, "%Y-%m-%d")
                    fecha_fmt = dt_obj.strftime("%d/%m/%Y (%A)")
                    amigas_que_pueden = votos_por_fecha.get(f_str, [])
                    nombres = ", ".join(amigas_que_pueden)

                    elementos_estadistica.append(
                        ft.Text(
                            f"• {fecha_fmt} ➔ {nombres}", size=12, color=COLOR_TEXTO
                        )
                    )
            else:
                elementos_estadistica.append(
                    ft.Text(
                        "📊 Todavía no hay votos suficientes para calcular la mejor fecha.",
                        size=13,
                        color=COLOR_TEXTO,
                    )
                )
        else:
            elementos_estadistica.append(
                ft.Text(
                    "📊 Todavía no hay votos suficientes para calcular la mejor fecha.",
                    size=13,
                    color=COLOR_TEXTO,
                )
            )

        card_estadistica = ft.Container(
            content=ft.Column(elementos_estadistica, spacing=6),
            bgcolor="white",
            border=ft.Border(
                top=ft.BorderSide(1, COLOR_BORDE),
                bottom=ft.BorderSide(1, COLOR_BORDE),
                left=ft.BorderSide(1, COLOR_BORDE),
                right=ft.BorderSide(1, COLOR_BORDE),
            ),
            border_radius=8,
            padding=12,
        )

        contenido_principal.controls = [
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=COLOR_ROJO,
                        on_click=lambda e: actualizar_pantalla(),
                    ),
                    ft.Text(
                        f"📊 Sondeo: {titulo_q}",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_ROJO_OSCURO,
                    ),
                ]
            ),
            ft.Text(
                "Marca los días que te vienen bien para este plan:",
                color=COLOR_TEXTO,
                size=13,
            ),
            card_estadistica,
            ft.Divider(color=COLOR_BORDE),
            ft.Column(controles_votacion, spacing=8),
            ft.Button(
                "Guardar Mis Disponibilidades 💖",
                on_click=guardar_mis_votos,
                style=ft.ButtonStyle(bgcolor=COLOR_ROJO, color="white"),
            ),
            ft.Divider(color=COLOR_BORDE),
            ft.Text(
                "🗓️ Calendario de Grupo (¿Quién puede qué día?):",
                weight=ft.FontWeight.BOLD,
                color=COLOR_ROJO_OSCURO,
            ),
            ft.Column(resumen_colores, spacing=8),
        ]
        page.update()

    def actualizar_pantalla():
        quedadas = obtener_quedadas()

        tarjetas: list[ft.Control] = []
        for q in quedadas:
            tipo = q.get("tipo_plan", "fijo")
            es_sondeo = tipo == "sondeo"
            id_q = q["id"]
            fecha_plan = q.get("fecha", "Sin fecha")

            sub_texto = (
                f"📅 Fecha: {fecha_plan} (Creado por: {q.get('creadora', 'Anónima')})"
                if not es_sondeo
                else f"📊 Sondeo (Creado por: {q.get('creadora', 'Anónima')})"
            )

            controles_tarjeta: list[ft.Control] = [
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.EVENT, color=COLOR_ROJO),
                    title=ft.Text(
                        q.get("titulo", ""),
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_ROJO_OSCURO,
                    ),
                    subtitle=ft.Text(
                        f"{q.get('descripcion', '')}\n{sub_texto}", color=COLOR_TEXTO
                    ),
                )
            ]

            elementos_fila = []

            if es_sondeo:
                boton_sondeo = ft.Button(
                    "Ver / Votar Disponibilidad 🗓️",
                    on_click=lambda e, quedada=q: abrir_detalle_sondeo(quedada),
                    style=ft.ButtonStyle(bgcolor=COLOR_ROSA_FUERTE, color="white"),
                )
                elementos_fila.append(boton_sondeo)
            else:
                # Comprobamos si la usuaria actual ya está apuntada a este plan fijo
                asistentes_fijos = obtener_disponibilidad_quedada(id_q)
                mi_registro = next(
                    (
                        a
                        for a in asistentes_fijos
                        if str(a.get("amiga", "")).strip()
                        == str(usuario_actual["nombre"]).strip()
                        and (a.get("disponible") is True or a.get("disponible") == 1)
                    ),
                    None,
                )

                if mi_registro:
                    # CASO A: Ya está apuntada -> Permite editar la hora con un diseño limpio
                    hora_registrada = mi_registro.get("hora_llegada", "Sin hora")

                    txt_editar_hora = ft.TextField(
                        value=mi_registro.get("hora_llegada", ""),
                        label="Hora",
                        text_size=12,
                        height=38,
                        width=120,
                        content_padding=5,
                        border_color=COLOR_ROSA_FUERTE,
                        focused_border_color=COLOR_ROJO,
                        cursor_color=COLOR_ROJO,
                        color=COLOR_TEXTO,
                        bgcolor="white",
                        border_radius=8,
                    )

                    def actualizar_mi_hora(
                        e, q_id=id_q, f_plan=fecha_plan, txt=txt_editar_hora
                    ):
                        exito, msg = apuntarse_plan_fijo(
                            id_quedada=q_id,
                            amiga=usuario_actual["nombre"],
                            fecha_plan=f_plan,
                            hora_llegada=txt.value.strip(),
                        )
                        lbl_mensaje.color = "green" if exito else COLOR_ROJO
                        lbl_mensaje.value = (
                            "¡Hora actualizada con éxito! 🕒" if exito else msg
                        )
                        actualizar_pantalla()
                        page.update()

                    btn_actualizar = ft.Button(
                        "Actualizar hora 🔄",
                        on_click=actualizar_mi_hora,
                        style=ft.ButtonStyle(
                            bgcolor=COLOR_ROSA_FUERTE,
                            color="white",
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    )

                    controles_tarjeta.append(
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(
                                                ft.Icons.CHECK_CIRCLE,
                                                color="green",
                                                size=16,
                                            ),
                                            ft.Text(
                                                f"Estás apuntada (Llegada: {hora_registrada})",
                                                size=12,
                                                weight=ft.FontWeight.BOLD,
                                                color=COLOR_ROJO_OSCURO,
                                            ),
                                        ],
                                        spacing=6,
                                    ),
                                    ft.Row(
                                        [txt_editar_hora, btn_actualizar], spacing=8
                                    ),
                                ],
                                spacing=6,
                            ),
                            bgcolor="#F9F9FB",
                            padding=10,
                            border_radius=8,
                            border=ft.Border(
                                top=ft.BorderSide(1, COLOR_BORDE),
                                bottom=ft.BorderSide(1, COLOR_BORDE),
                                left=ft.BorderSide(1, COLOR_BORDE),
                                right=ft.BorderSide(1, COLOR_BORDE),
                            ),
                        )
                    )
                else:
                    # CASO B: No está apuntada -> Muestra el campo y botón para unirse
                    txt_hora = ft.TextField(
                        label="Hora llegada (ej: 21:00)",
                        text_size=12,
                        height=40,
                        content_padding=5,
                        border_color=COLOR_ROSA_FUERTE,
                        focused_border_color=COLOR_ROJO,
                        cursor_color=COLOR_ROJO,
                        color=COLOR_TEXTO,
                        bgcolor="white",
                        border_radius=8,
                        expand=True,
                    )

                    def confirmar_apunte_fijo(
                        e, q_id=id_q, f_plan=fecha_plan, txt=txt_hora
                    ):
                        exito, msg = apuntarse_plan_fijo(
                            id_quedada=q_id,
                            amiga=usuario_actual["nombre"],
                            fecha_plan=f_plan,
                            hora_llegada=txt.value.strip(),
                        )
                        lbl_mensaje.color = "green" if exito else COLOR_ROJO
                        lbl_mensaje.value = msg
                        actualizar_pantalla()
                        page.update()

                    btn_apuntar = ft.Button(
                        "Apuntarme 💖",
                        on_click=confirmar_apunte_fijo,
                        style=ft.ButtonStyle(
                            bgcolor=COLOR_ROJO,
                            color="white",
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    )

                    controles_tarjeta.append(
                        ft.Container(
                            content=ft.Row([txt_hora, btn_apuntar], spacing=10),
                            padding=8,
                        )
                    )

                nombres_asistentes = [
                    (
                        f"{a.get('amiga')} ({a.get('hora_llegada')})"
                        if a.get("hora_llegada")
                        else a.get("amiga")
                    )
                    for a in asistentes_fijos
                    if a.get("disponible") is True or a.get("disponible") == 1
                ]
                if nombres_asistentes:
                    chips_asistentes: list[ft.Control] = [
                        ft.Container(
                            content=ft.Text(nombre, size=11, color="white"),
                            bgcolor=COLOR_ROSA_FUERTE,
                            padding=6,
                            border_radius=8,
                        )
                        for nombre in nombres_asistentes
                    ]
                    controles_tarjeta.append(
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        "Asistentes confirmadas:",
                                        size=11,
                                        weight=ft.FontWeight.BOLD,
                                        color=COLOR_ROJO_OSCURO,
                                    ),
                                    ft.Row(chips_asistentes, wrap=True, spacing=5),
                                ],
                                spacing=3,
                            ),
                            padding=8,
                        )
                    )

            es_creadora = (
                q.get("creadora") == usuario_actual.get("nombre")
            ) or usuario_actual.get("es_admin", False)

            if es_creadora:

                def borrar_plan(e, id_q=id_q):
                    exito, msg = eliminar_quedada(id_q)
                    lbl_mensaje.color = "green" if exito else COLOR_ROJO
                    lbl_mensaje.value = msg
                    actualizar_pantalla()
                    page.update()

                btn_eliminar = ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color="red",
                    tooltip="Eliminar este plan",
                    on_click=borrar_plan,
                )
                elementos_fila.append(btn_eliminar)

            if elementos_fila:
                controles_tarjeta.append(
                    ft.Container(
                        content=ft.Row(
                            elementos_fila, alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        padding=10,
                    )
                )

            tarjetas.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(controles_tarjeta), padding=5
                    ),
                    bgcolor="white",
                    elevation=1,
                )
            )

        lista_quedadas_col.controls = tarjetas

        contenido_principal.controls = [
            ft.Row(
                [
                    ft.Icon(ft.Icons.EVENT, color=COLOR_ROJO_OSCURO, size=22),
                    ft.Text(
                        "✨ Organiza un Nuevo Plan",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_ROJO_OSCURO,
                    ),
                ],
                spacing=8,
            ),
            ft.Text(
                "Crea una quedada fija o un sondeo de fechas:",
                color=COLOR_TEXTO,
                size=12,
            ),
            ft.Divider(color=COLOR_BORDE),
            txt_titulo,
            txt_desc,
            radio_tipo_plan,
            contenedor_dinamico_fecha,
            ft.Button(
                "Crear Plan 🚀",
                on_click=guardar_nuevo_plan,
                style=ft.ButtonStyle(
                    bgcolor=COLOR_ROJO,
                    color="white",
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            ),
            lbl_mensaje,
            ft.Divider(color=COLOR_BORDE),
            ft.Text(
                "📋 Quedadas y Sondeos Activos:",
                weight=ft.FontWeight.BOLD,
                color=COLOR_ROJO_OSCURO,
            ),
            lista_quedadas_col,
        ]
        page.update()

    actualizar_pantalla()
    # 1. Tarjeta central gris-blanca donde se organiza todo el contenido de la vista
    tarjeta_central = ft.Container(
        content=contenido_principal,
        bgcolor=COLOR_FONDO_TARJETA,  # #F0F0F2 (Gris-blanco)
        padding=25,
        border_radius=16,
        border=ft.Border(
            top=ft.BorderSide(1, COLOR_BORDE),
            bottom=ft.BorderSide(1, COLOR_BORDE),
            left=ft.BorderSide(1, COLOR_BORDE),
            right=ft.BorderSide(1, COLOR_BORDE),
        ),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=12, color="#33000000"),
        width=600,
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

    return contenedor_principal, actualizar_pantalla
