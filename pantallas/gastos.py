import flet as ft
from database import (
    agregar_gasto_avanzado,
    crear_actividad_con_participantes,  # Asegúrate de tener esta función en database.py o cámbiala por la tuya
    marcar_deuda_saldada,
    obtener_actividades,
    obtener_amigas,
)


def crear_vista_gastos(
    page,
    usuario_actual,
    vistas_contenedor,
    COLOR_ROJO_OSCURO,
    COLOR_TEXTO,
    COLOR_ROSA_FUERTE,
    COLOR_ROJO,
    COLOR_BORDE,
    COLOR_FONDO_TARJETA,
):
    lista_actividades_view = ft.ListView(expand=1, spacing=15)
    contenido_gastos = ft.Column(
        spacing=12,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        expand=True,
    )

    # 1. Campos de texto básicos
    txt_nombre_actividad = ft.TextField(
        label="Nombre de la actividad (ej. Escapada a la playa 🏖️)",
        expand=True,
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        color=COLOR_TEXTO,
        bgcolor="white",
        border_radius=8,
    )

    txt_buscador = ft.TextField(
        label="🔍 Buscar actividad...",
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO,
        color=COLOR_TEXTO,
        bgcolor="white",
        border_radius=8,
        on_change=lambda e: actualizar_pantalla_gastos(),
    )

    # Funcionalidad de Invitados Extra y Checkboxes de Creación
    checks_crear_actividad = {}
    columna_checks_creacion = ft.Column(spacing=5)
    invitados_temporales = []

    txt_invitado_extra = ft.TextField(
        label="Añadir invitado extra (ej. Carlos, novio de Ana)",
        expand=True,
        border_color=COLOR_ROSA_FUERTE,
        color=COLOR_TEXTO,
        bgcolor="white",
        border_radius=8,
        text_size=12,
    )

    def actualizar_lista_checks_creacion():
        columna_checks_creacion.controls.clear()
        checks_crear_actividad.clear()

        amigas_oficiales = obtener_amigas()

        columna_checks_creacion.controls.append(
            ft.Text(
                "✨ Selecciona quiénes participan en este plan:",
                weight=ft.FontWeight.BOLD,
                size=13,
                color=COLOR_ROSA_FUERTE,
            )
        )

        todas_las_personas = amigas_oficiales + [
            i for i in invitados_temporales if i not in amigas_oficiales
        ]

        for amiga in todas_las_personas:
            por_defecto = (amiga == usuario_actual["nombre"]) or (
                amiga in invitados_temporales
            )
            chk = ft.Checkbox(label=amiga, value=por_defecto, active_color=COLOR_ROJO)
            checks_crear_actividad[amiga] = chk
            columna_checks_creacion.controls.append(chk)

        try:
            contenedor_formulario_creacion.update()
        except Exception:
            pass

    def agregar_invitado_extra_click(e):
        val = txt_invitado_extra.value
        nombre_extra = val.strip() if val else ""

        if nombre_extra:
            if nombre_extra not in invitados_temporales:
                invitados_temporales.append(nombre_extra)

            txt_invitado_extra.value = ""
            txt_invitado_extra.update()
            actualizar_lista_checks_creacion()

    def crear_actividad_click(e):
        titulo = (
            txt_nombre_actividad.value.strip() if txt_nombre_actividad.value else ""
        )
        seleccionadas = [
            amiga for amiga, chk in checks_crear_actividad.items() if chk.value
        ]

        if titulo and seleccionadas:
            # Si tu base de datos usa crear_actividad simple, cámbialo aquí según prefieras
            exito, msg = crear_actividad_con_participantes(titulo, seleccionadas)
            if exito:
                txt_nombre_actividad.value = ""
                invitados_temporales.clear()
                contenedor_formulario_creacion.visible = False
                actualizar_lista_checks_creacion()
                actualizar_pantalla_gastos()
            page.snack_bar = ft.SnackBar(ft.Text(msg))
            page.snack_bar.open = True
            page.update()
        else:
            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "⚠️ Escribe un título y selecciona al menos a una persona"
                    " participante."
                )
            )
            page.snack_bar.open = True
            page.update()

    # Contenedor desplegable para el formulario de creación
    contenedor_formulario_creacion = ft.Container(
        content=ft.Column(
            [
                ft.Text(
                    "✨ Nueva Actividad o Viaje",
                    weight=ft.FontWeight.BOLD,
                    size=15,
                    color=COLOR_ROJO_OSCURO,
                ),
                txt_nombre_actividad,
                ft.Row(
                    [
                        txt_invitado_extra,
                        ft.Button(
                            text="Añadir Invitado ➕",
                            on_click=agregar_invitado_extra_click,
                            style=ft.ButtonStyle(
                                bgcolor=COLOR_ROSA_FUERTE, color="white"
                            ),
                        ),
                    ]
                ),
                columna_checks_creacion,
                ft.Button(
                    text="Guardar Actividad ✨",
                    on_click=crear_actividad_click,
                    style=ft.ButtonStyle(
                        bgcolor=COLOR_ROJO,
                        color="white",
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                ),
            ]
        ),
        visible=False,  # Oculto por defecto hasta que se pulsa el botón
        bgcolor="white",
        padding=15,
        border_radius=10,
        border=ft.Border(
            top=ft.BorderSide(1, COLOR_BORDE),
            bottom=ft.BorderSide(1, COLOR_BORDE),
            left=ft.BorderSide(1, COLOR_BORDE),
            right=ft.BorderSide(1, COLOR_BORDE),
        ),
    )

    def toggle_formulario_creacion(e):
        contenedor_formulario_creacion.visible = (
            not contenedor_formulario_creacion.visible
        )
        contenedor_formulario_creacion.update()

    def abrir_detalle_actividad(actividad):
        txt_concepto = ft.TextField(
            label="Concepto (ej. Cervezas)",
            expand=2,
            border_color=COLOR_ROSA_FUERTE,
            focused_border_color=COLOR_ROJO,
            cursor_color=COLOR_ROJO,
            color=COLOR_TEXTO,
            bgcolor="white",
            border_radius=8,
        )
        txt_importe = ft.TextField(
            label="Importe (€)",
            expand=1,
            border_color=COLOR_ROSA_FUERTE,
            focused_border_color=COLOR_ROJO,
            cursor_color=COLOR_ROJO,
            color=COLOR_TEXTO,
            bgcolor="white",
            border_radius=8,
        )

        dropdown_categoria = ft.Dropdown(
            label="Categoría",
            value="🍔 Comida",
            options=[
                ft.dropdown.Option("🍔 Comida"),
                ft.dropdown.Option("🚗 Transporte"),
                ft.dropdown.Option("🏠 Alojamiento"),
                ft.dropdown.Option("🎁 Regalos"),
                ft.dropdown.Option("✨ Varios"),
            ],
            border_color=COLOR_ROSA_FUERTE,
            focused_border_color=COLOR_ROJO,
            color=COLOR_TEXTO,
            bgcolor="white",
            border_radius=8,
        )

        amigas_grupo = obtener_amigas()
        checks_participantes = {}
        col_checks = ft.Column(
            [
                ft.Text(
                    "✨ ¿Quién participa en este gasto?",
                    weight=ft.FontWeight.BOLD,
                    size=13,
                    color=COLOR_ROSA_FUERTE,
                )
            ]
        )

        for amiga in amigas_grupo:
            chk = ft.Checkbox(label=amiga, value=True, active_color=COLOR_ROJO)
            checks_participantes[amiga] = chk
            col_checks.controls.append(chk)

        lista_gastos_actividad = ft.ListView(expand=1, spacing=10)
        lbl_balance_resultado = ft.Text("", size=13, color=COLOR_TEXTO)
        contenedor_grafico = ft.Container()
        lista_feed = ft.ListView(expand=1, spacing=5, height=100)
        columna_saldos_botones = ft.Column(spacing=8)

        def recalcular_balances_actividad():
            acts = obtener_actividades()
            act_actualizada = next(
                (a for a in acts if a["id"] == actividad["id"]), actividad
            )

            lista_gastos_actividad.controls.clear()
            lista_feed.controls.clear()
            columna_saldos_botones.controls.clear()

            participantes_act = [
                p["amiga"] for p in act_actualizada.get("participantes_actividad", [])
            ]
            pagos_totales = {amiga: 0.0 for amiga in participantes_act}
            debe_totales = {amiga: 0.0 for amiga in participantes_act}
            totales_por_categoria = {
                "🍔 Comida": 0,
                "🚗 Transporte": 0,
                "🏠 Alojamiento": 0,
                "🎁 Regalos": 0,
                "✨ Varios": 0,
            }

            for g in act_actualizada.get("gastos", []):
                pagador = g["pagado_por"]
                importe = g["importe"]
                cat = g.get("categoria", "✨ Varios")
                totales_por_categoria[cat] = totales_por_categoria.get(cat, 0) + importe

                part_gasto = [pg["amiga"] for pg in g.get("participantes_gasto", [])]
                pagos_totales[pagador] = pagos_totales.get(pagador, 0.0) + importe

                if part_gasto:
                    parte = importe / len(part_gasto)
                    for p in part_gasto:
                        if p not in debe_totales:
                            debe_totales[p] = 0.0
                        debe_totales[p] += parte

                lista_gastos_actividad.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.ListTile(
                                leading=ft.Icon(ft.Icons.RECEIPT, color=COLOR_ROJO),
                                title=ft.Text(
                                    f"{g['concepto']} — {importe} €",
                                    weight=ft.FontWeight.BOLD,
                                    color=COLOR_ROJO_OSCURO,
                                ),
                                subtitle=ft.Text(
                                    f"[{cat}] Pagado por: {pagador} | Participan:"
                                    f" {', '.join(part_gasto)}",
                                    color=COLOR_TEXTO,
                                    size=12,
                                ),
                            ),
                            padding=10,
                        ),
                        bgcolor="white",
                        elevation=1,
                    )
                )

            secciones_grafico = []
            colores_cat = ["#b30819", "#e63946", "#f1faee", "#a8dadc", "#457b9d"]
            i = 0
            for cat, val in totales_por_categoria.items():
                if val > 0:
                    secciones_grafico.append(
                        ft.PieChartSection(
                            val,
                            title=f"{cat.split()[1]} ({val}€)",
                            title_style=ft.TextStyle(
                                size=11,
                                color=ft.Colors.WHITE,
                                weight=ft.FontWeight.BOLD,
                            ),
                            color=colores_cat[i % len(colores_cat)],
                            radius=50,
                        )
                    )
                i += 1

            if secciones_grafico:
                contenedor_grafico.content = ft.Column(
                    [
                        ft.Text(
                            "📊 Distribución de Gastos:",
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_ROJO_OSCURO,
                        ),
                        ft.PieChart(
                            sections=secciones_grafico,
                            sections_space=2,
                            center_space_radius=20,
                            height=130,
                        ),
                    ]
                )
            else:
                contenedor_grafico.content = ft.Text("")

            balances_netos = {
                amiga: pagos_totales.get(amiga, 0.0) - debe_totales.get(amiga, 0.0)
                for amiga in pagos_totales
            }
            deudoras = [
                [amiga, -bal] for amiga, bal in balances_netos.items() if bal < -0.01
            ]
            acreedoras = [
                [amiga, bal] for amiga, bal in balances_netos.items() if bal > 0.01
            ]

            balance_texto = "❤️ Resumen de caja:\n"
            if not act_actualizada.get("gastos"):
                balance_texto = "Aún no hay gastos registrados."
            else:
                for amiga, total in pagos_totales.items():
                    balance_texto += f"• {amiga} ha pagado un total de {total:.2f} €\n"

                balance_texto += "\n💌 Cuentas claras (Quién debe a quién):\n"
                if not deudoras and not acreedoras:
                    balance_texto += "¡Todo saldado perfectamente! ✨"
                else:
                    d_idx, a_idx = 0, 0
                    while d_idx < len(deudoras) and a_idx < len(acreedoras):
                        deudor, cant_debe = deudoras[d_idx]
                        acreedor, cant_tiene = acreedoras[a_idx]
                        monto = min(cant_debe, cant_tiene)

                        balance_texto += f"👉 **{deudor}** le debe **{monto:.2f} €** a **{acreedor}**\n"

                        def hacer_clic_saldar(
                            d_amiga=deudor, a_amiga=acreedor, monto_val=monto
                        ):
                            def ejecutar(e):
                                marcar_deuda_saldada(
                                    actividad["id"], d_amiga, a_amiga, monto_val
                                )
                                recalcular_balances_actividad()

                            return ejecutar

                        columna_saldos_botones.controls.append(
                            ft.Button(
                                text=f"Saldar {monto:.2f}€ de {deudor} a {acreedor} 💸",
                                on_click=hacer_clic_saldar(),
                                bgcolor=COLOR_ROJO,
                                color="white",
                            )
                        )

                        deudoras[d_idx][1] -= monto
                        acreedoras[a_idx][1] -= monto
                        if deudoras[d_idx][1] < 0.01:
                            d_idx += 1
                        if acreedoras[a_idx][1] < 0.01:
                            a_idx += 1

            lbl_balance_resultado.value = balance_texto

            for evento in act_actualizada.get("feed", []):
                lista_feed.controls.append(ft.Text(evento, size=11, color=COLOR_TEXTO))

            page.update()

        def agregar_gasto_click(e):
            try:
                importe_num = float(txt_importe.value.replace(",", "."))
                seleccionadas = [
                    amiga for amiga, chk in checks_participantes.items() if chk.value
                ]

                if txt_concepto.value and importe_num > 0 and seleccionadas:
                    agregar_gasto_avanzado(
                        actividad["id"],
                        txt_concepto.value,
                        usuario_actual["nombre"],
                        importe_num,
                        seleccionadas,
                        dropdown_categoria.value,
                    )
                    txt_concepto.value = ""
                    txt_importe.value = ""
                    recalcular_balances_actividad()
            except ValueError:
                pass

        def copiar_resumen_portapapeles(e):
            page.set_clipboard(lbl_balance_resultado.value)
            page.snack_bar = ft.SnackBar(
                ft.Text("¡Resumen copiado al portapapeles para WhatsApp! 📋✨")
            )
            page.snack_bar.open = True
            page.update()

        recalcular_balances_actividad()

        contenido_gastos.controls = [
            ft.Row(
                [
                    ft.OutlinedButton(
                        text="⬅ Volver",
                        on_click=lambda e: actualizar_pantalla_gastos(),
                        style=ft.ButtonStyle(
                            color=COLOR_ROJO, side=ft.BorderSide(1, COLOR_ROJO)
                        ),
                    ),
                    ft.Text(
                        f"✨ {actividad['titulo']}",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_ROJO_OSCURO,
                    ),
                ]
            ),
            ft.Divider(color=COLOR_BORDE),
            ft.Row([txt_concepto, txt_importe]),
            dropdown_categoria,
            col_checks,
            ft.Button(
                text="Añadir Gasto 💳",
                on_click=agregar_gasto_click,
                style=ft.ButtonStyle(
                    bgcolor=COLOR_ROJO,
                    color="white",
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
            ),
            ft.Divider(color=COLOR_BORDE),
            contenedor_grafico,
            lbl_balance_resultado,
            columna_saldos_botones,
            ft.Button(
                text="Copiar Resumen para WhatsApp 📋",
                on_click=copiar_resumen_portapapeles,
                bgcolor=COLOR_ROSA_FUERTE,
                color="white",
            ),
            ft.Divider(color=COLOR_BORDE),
            ft.Text(
                "🔔 Historial de Actividad:",
                weight=ft.FontWeight.BOLD,
                color=COLOR_ROJO_OSCURO,
                size=12,
            ),
            lista_feed,
            ft.Divider(color=COLOR_BORDE),
            ft.Text(
                "🌷 Historial de Gastos:",
                weight=ft.FontWeight.BOLD,
                color=COLOR_ROJO_OSCURO,
            ),
            lista_gastos_actividad,
        ]
        page.update()

    def actualizar_pantalla_gastos():
        lista_actividades_view.controls.clear()
        actividades_data = obtener_actividades()
        texto_busqueda = txt_buscador.value.lower() if txt_buscador.value else ""

        for act in actividades_data:
            if texto_busqueda and texto_busqueda not in act["titulo"].lower():
                continue

            def crear_clic_abrir(a=act):
                return lambda e: abrir_detalle_actividad(a)

            part_nombres = [p["amiga"] for p in act.get("participantes_actividad", [])]
            card_content = ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CARD_TRAVEL, color=COLOR_ROJO),
                        title=ft.Text(
                            act["titulo"],
                            weight=ft.FontWeight.BOLD,
                            size=16,
                            color=COLOR_ROJO_OSCURO,
                        ),
                        subtitle=ft.Text(
                            f"Gastos: {len(act.get('gastos', []))} | Chicas:"
                            f" {', '.join(part_nombres)}",
                            color=COLOR_TEXTO,
                            size=12,
                        ),
                    ),
                    ft.Button(
                        text="Ver Cuentas y Gráficos 💖",
                        on_click=crear_clic_abrir(),
                        style=ft.ButtonStyle(
                            bgcolor=COLOR_ROSA_FUERTE,
                            color="white",
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                    ),
                ],
                spacing=5,
            )

            lista_actividades_view.controls.append(
                ft.Card(
                    content=ft.Container(content=card_content, padding=15),
                    bgcolor="white",
                    elevation=1,
                )
            )

        contenido_gastos.controls = [
            ft.Row(
                [
                    ft.Icon(ft.Icons.EURO, color=COLOR_ROJO_OSCURO, size=22),
                    ft.Text(
                        "Cuentas Compartidas 🥂",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=COLOR_ROJO_OSCURO,
                    ),
                ],
                spacing=8,
            ),
            ft.Text(
                "Crea una actividad o viaje para llevar los gastos ordenados:",
                color=COLOR_TEXTO,
                size=13,
            ),
            ft.Button(
                text="➕ Crear nueva actividad",
                icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                on_click=toggle_formulario_creacion,
                style=ft.ButtonStyle(bgcolor=COLOR_ROJO, color="white"),
            ),
            contenedor_formulario_creacion,
            txt_buscador,
            ft.Divider(color=COLOR_BORDE),
            ft.Text(
                "❤️ Tus Actividades:",
                size=16,
                weight=ft.FontWeight.BOLD,
                color=COLOR_ROJO_OSCURO,
            ),
            lista_actividades_view,
        ]
        page.update()

    actualizar_lista_checks_creacion()

    tarjeta_central = ft.Container(
        content=contenido_gastos,
        bgcolor=COLOR_FONDO_TARJETA,
        padding=25,
        border_radius=16,
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=12, color="#33000000"),
        width=500,
        expand=True,
    )

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

    actualizar_pantalla_gastos()
    return contenedor_principal, actualizar_pantalla_gastos
