import flet as ft

def main(page: ft.Page):
    page.title = "App de Amigas 💖"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#FFF0F3"  # Fondo rosita muy clarito y suave
    page.vertical_alignment = ft.MainAxisAlignment.START

    # Nueva Paleta: Rojos y Rosas Fuertes
    COLOR_ROSA_FUERTE = "#FF1493"   # Rosa Fucsia / Deep Pink principal
    COLOR_ROJO = "#DC143C"          # Rojo Crimson vibrante para acentos y botones
    COLOR_ROJO_OSCURO = "#8B0000"   # Rojo oscuro para títulos principales
    COLOR_FONDO_TARJETA = "#FFE4E1" # Rosa pastel muy suave para el fondo de las tarjetas
    COLOR_BORDE = "#FFB6C1"         # Borde rosado de contraste
    COLOR_TEXTO = "#4A2E35"         # Tono oscuro tirando a vino para lectura perfecta

    usuario_actual = {"nombre": ""}
    
    amigas_grupo = ["Nerea", "Lucía", "Ana", "Marta", "Sofía"]

    quedadas_data = [
        {"titulo": "Cena de tapas en el centro", "desc": "Quedamos en la plaza principal e iremos de pinchos.", "asistentes": {}},
    ]

    actividades_gastos = [
        {
            "titulo": "Finde en el monte 🌲",
            "participantes": ["Nerea", "Lucía", "Ana"],
            "gastos": [
                {"concepto": "Gasolina", "pagado_por": "Nerea", "importe": 30.0, "participantes_gasto": ["Nerea", "Lucía", "Ana"]},
                {"concepto": "Compra Supermercado", "pagado_por": "Lucía", "importe": 45.0, "participantes_gasto": ["Nerea", "Lucía", "Ana"]}
            ]
        }
    ]

    vista_principal = ft.Container(expand=True)

    def actualizar_lista_planes():
        pass

    def actualizar_pantalla_gastos():
        pass

    def actualizar_pantalla_perfil():
        pass


    # ==========================================
    # 1. PANTALLA DE INICIO DE SESIÓN
    # ==========================================
    txt_nombre = ft.TextField(
        label="¿Cómo te llamas, guapa?", 
        width=300,
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        cursor_color=COLOR_ROJO
    )
    error_login = ft.Text("", color=COLOR_ROJO, size=13)

    def entrar_app(e):
        nombre = txt_nombre.value.strip()
        if nombre:
            usuario_actual["nombre"] = nombre
            if nombre not in amigas_grupo:
                amigas_grupo.append(nombre)
            cargar_pantalla_principal()
        else:
            error_login.value = "Por favor, introduce tu nombre para entrar."
            page.update()

    pantalla_login = ft.Container(
        content=ft.Column([
            ft.Text("¡Bienvenidas al Club! ❤️", size=26, weight=ft.FontWeight.BOLD, color=COLOR_ROJO_OSCURO),
            ft.Text("Introduce tu nombre para unirte a los planes:", size=14, color=COLOR_TEXTO),
            txt_nombre,
            ft.Button(
                "Entrar a la App ✨", 
                on_click=entrar_app,
                style=ft.ButtonStyle(
                    bgcolor=COLOR_ROJO,
                    color=ft.Colors.WHITE,
                    shape=ft.RoundedRectangleBorder(radius=10)
                )
            ),
            error_login
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
        expand=True,
        padding=20
    )


    # ==========================================
    # 2. PESTAÑA: QUEDADAS
    # ==========================================
    lista_planes_view = ft.ListView(expand=1, spacing=15)

    def actualizar_lista_planes():
        lista_planes_view.controls.clear()
        
        for index, plan in enumerate(quedadas_data):
            asistentes_textos = []
            if plan["asistentes"]:
                for amiga, hora in plan["asistentes"].items():
                    asistentes_textos.append(f"🌹 {amiga} (Llega a las {hora})")
            else:
                asistentes_textos.append("🌹 Nadie apuntado todavía ¡Sé la primera!")

            txt_hora = ft.TextField(
                label="Hora (ej. 21:30)", 
                width=140, 
                value="20:00",
                border_color=COLOR_ROSA_FUERTE,
                text_size=13
            )

            def hacer_apuntarse(p_idx, h_field):
                def callback(e):
                    nombre = usuario_actual["nombre"]
                    hora = h_field.value or "Hora por definir"
                    quedadas_data[p_idx]["asistentes"][nombre] = hora
                    actualizar_lista_planes()
                return callback

            def hacer_desapuntarse(p_idx):
                def callback(e):
                    nombre = usuario_actual["nombre"]
                    if nombre in quedadas_data[p_idx]["asistentes"]:
                        del quedadas_data[p_idx]["asistentes"][nombre]
                        actualizar_lista_planes()
                return callback

            esta_apuntada = usuario_actual["nombre"] in plan["asistentes"]
            if esta_apuntada:
                btn_accion = ft.OutlinedButton(
                    "Desapuntarme ❌", 
                    on_click=hacer_desapuntarse(index),
                    style=ft.ButtonStyle(color=COLOR_ROJO)
                )
            else:
                btn_accion = ft.Row([
                    txt_hora, 
                    ft.Button(
                        "Apuntarme 💕", 
                        on_click=hacer_apuntarse(index, txt_hora),
                        style=ft.ButtonStyle(bgcolor=COLOR_ROSA_FUERTE, color=ft.Colors.WHITE)
                    )
                ], spacing=10)

            card_content = ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.EVENT_AVAILABLE, color=COLOR_ROJO),
                    title=ft.Text(plan["titulo"], weight=ft.FontWeight.BOLD, size=16, color=COLOR_ROJO_OSCURO),
                    subtitle=ft.Text(plan["desc"], color=COLOR_TEXTO),
                ),
                ft.Divider(color=COLOR_BORDE, height=1),
                ft.Text("✨ ¿Quién va y a qué hora?", weight=ft.FontWeight.BOLD, size=13, color=COLOR_ROSA_FUERTE),
                ft.Column([ft.Text(t, color=COLOR_TEXTO, size=13) for t in asistentes_textos], spacing=3),
                btn_accion
            ], spacing=10)

            lista_planes_view.controls.append(
                ft.Card(
                    content=ft.Container(content=card_content, padding=15),
                    bgcolor=COLOR_FONDO_TARJETA,
                    elevation=1
                )
            )
        
        page.update()

    txt_nuevo_titulo = ft.TextField(label="Título del plan", expand=True, border_color=COLOR_ROSA_FUERTE)
    txt_nueva_desc = ft.TextField(label="Descripción / Dónde / Notas", expand=True, border_color=COLOR_ROSA_FUERTE)

    def crear_nuevo_plan(e):
        if txt_nuevo_titulo.value:
            quedadas_data.append({
                "titulo": txt_nuevo_titulo.value,
                "desc": txt_nueva_desc.value or "Sin descripción",
                "asistentes": {}
            })
            txt_nuevo_titulo.value = ""
            txt_nueva_desc.value = ""
            actualizar_lista_planes()

    tab_quedadas = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.FAVORITE, color=COLOR_ROJO, size=16),
                ft.Text(f"Conectada como: {usuario_actual['nombre']}", italic=True, color=COLOR_ROJO_OSCURO, weight=ft.FontWeight.W_500)
            ]),
            ft.Divider(color=COLOR_BORDE),
            ft.Text("🌹 Crear un nuevo plan:", weight=ft.FontWeight.BOLD, color=COLOR_ROJO_OSCURO),
            txt_nuevo_titulo,
            txt_nueva_desc,
            ft.Button(
                "Crear Plan ✨", 
                on_click=crear_nuevo_plan,
                style=ft.ButtonStyle(bgcolor=COLOR_ROJO, color=ft.Colors.WHITE)
            ),
            ft.Divider(color=COLOR_BORDE),
            ft.Text("🌷 Próximas Quedadas:", size=16, weight=ft.FontWeight.BOLD, color=COLOR_ROJO_OSCURO),
            lista_planes_view
        ], expand=True, spacing=12),
        padding=20
    )


    # ==========================================
    # 3. PESTAÑA: GASTOS
    # ==========================================
    lista_actividades_view = ft.ListView(expand=1, spacing=15)
    txt_nombre_actividad = ft.TextField(label="Nombre de la actividad (ej. Cena Cumple)", expand=True, border_color=COLOR_ROSA_FUERTE)

    def crear_actividad(e):
        if txt_nombre_actividad.value:
            actividades_gastos.append({
                "titulo": txt_nombre_actividad.value,
                "participantes": [usuario_actual["nombre"]],
                "gastos": []
            })
            txt_nombre_actividad.value = ""
            actualizar_pantalla_gastos()

    def abrir_detalle_actividad(actividad):
        txt_concepto = ft.TextField(label="Concepto (ej. Regalo)", expand=2, border_color=COLOR_ROSA_FUERTE)
        txt_importe = ft.TextField(label="Importe (€)", expand=1, border_color=COLOR_ROSA_FUERTE)
        
        checks_participantes = {}
        col_checks = ft.Column([ft.Text("✨ ¿Quién participa en este gasto?", weight=ft.FontWeight.BOLD, size=13, color=COLOR_ROSA_FUERTE)])
        
        for amiga in amigas_grupo:
            chk = ft.Checkbox(label=amiga, value=True, active_color=COLOR_ROJO)
            checks_participantes[amiga] = chk
            col_checks.controls.append(chk)

        lista_gastos_actividad = ft.ListView(expand=1, spacing=10)
        lbl_balance_resultado = ft.Text("", size=13, color=COLOR_TEXTO)

        def recalcular_balances_actividad():
            lista_gastos_actividad.controls.clear()
            
            pagos_totales = {}
            debe_totales = {}
            
            for amiga in actividad["participantes"]:
                pagos_totales[amiga] = 0.0
                debe_totales[amiga] = 0.0

            for g in actividad["gastos"]:
                pagador = g["pagado_por"]
                importe = g["importe"]
                participantes_gasto = g["participantes_gasto"]
                
                pagos_totales[pagador] = pagos_totales.get(pagador, 0.0) + importe
                
                if participantes_gasto:
                    parte = importe / len(participantes_gasto)
                    for p in participantes_gasto:
                        debe_totales[p] = debe_totales.get(p, 0.0) + parte

                lista_gastos_actividad.controls.append(
                    ft.Card(
                        content=ft.Container(content=ft.ListTile(
                            leading=ft.Icon(ft.Icons.CARD_GIFTCARD, color=COLOR_ROJO),
                            title=ft.Text(f"{g['concepto']} — {importe} €", weight=ft.FontWeight.BOLD, color=COLOR_ROJO_OSCURO),
                            subtitle=ft.Text(f"Pagado por: {pagador} | Participan: {', '.join(participantes_gasto)}", color=COLOR_TEXTO, size=12)
                        ), padding=10),
                        bgcolor=COLOR_FONDO_TARJETA,
                        elevation=1
                    )
                )

            balances_netos = {}
            for amiga in actividad["participantes"]:
                pago = pagos_totales.get(amiga, 0.0)
                debe = debe_totales.get(amiga, 0.0)
                balances_netos[amiga] = pago - debe

            deudoras = []
            acreedoras = []
            for amiga, bal in balances_netos.items():
                if bal < -0.01:
                    deudoras.append([amiga, -bal])
                elif bal > 0.01:
                    acreedoras.append([amiga, bal])

            balance_texto = "❤️ Resumen de caja:\n"
            if not actividad["gastos"]:
                balance_texto = "Aún no hay gastos registrados en esta actividad."
            else:
                for amiga, total in pagos_totales.items():
                    balance_texto += f"• {amiga} ha pagado un total de {total:.2f} €\n"
                
                balance_texto += "\n💌 Cuentas claras (Quién debe a quién):\n"
                if not deudoras and not acreedoras:
                    balance_texto += "¡Todo saldado perfectamente! ✨"
                else:
                    d_idx = 0
                    a_idx = 0
                    while d_idx < len(deudoras) and a_idx < len(acreedoras):
                        deudor, cant_debe = deudoras[d_idx]
                        acreedor, cant_tiene = acreedoras[a_idx]
                        
                        monto = min(cant_debe, cant_tiene)
                        balance_texto += f"👉 **{deudor}** le debe **{monto:.2f} €** a **{acreedor}**\n"
                        
                        deudoras[d_idx][1] -= monto
                        acreedoras[a_idx][1] -= monto
                        
                        if deudoras[d_idx][1] < 0.01: d_idx += 1
                        if acreedoras[a_idx][1] < 0.01: a_idx += 1

            lbl_balance_resultado.value = balance_texto
            page.update()

        def agregar_gasto_actividad(e):
            try:
                importe_num = float(txt_importe.value.replace(",", "."))
                seleccionadas = [amiga for amiga, chk in checks_participantes.items() if chk.value]
                
                if txt_concepto.value and importe_num > 0 and seleccionadas:
                    for s in seleccionadas:
                        if s not in actividad["participantes"]:
                            actividad["participantes"].append(s)

                    actividad["gastos"].append({
                        "concepto": txt_concepto.value,
                        "pagado_por": usuario_actual["nombre"],
                        "importe": importe_num,
                        "participantes_gasto": seleccionadas
                    })
                    txt_concepto.value = ""
                    txt_importe.value = ""
                    recalcular_balances_actividad()
            except ValueError:
                pass

        recalcular_balances_actividad()

        vista_detalle = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.OutlinedButton("⬅ Volver", on_click=lambda e: actualizar_pantalla_gastos(), style=ft.ButtonStyle(color=COLOR_ROJO)),
                    ft.Text(f"✨ {actividad['titulo']}", size=16, weight=ft.FontWeight.BOLD, color=COLOR_ROJO_OSCURO)
                ]),
                ft.Divider(color=COLOR_BORDE),
                ft.Row([txt_concepto, txt_importe]),
                col_checks,
                ft.Button(
                    f"Añadir Gasto (Paga {usuario_actual['nombre']}) 💳", 
                    on_click=agregar_gasto_actividad,
                    style=ft.ButtonStyle(bgcolor=COLOR_ROJO, color=ft.Colors.WHITE)
                ),
                ft.Divider(color=COLOR_BORDE),
                lbl_balance_resultado,
                ft.Divider(color=COLOR_BORDE),
                ft.Text("🌷 Historial de Gastos:", weight=ft.FontWeight.BOLD, color=COLOR_ROJO_OSCURO),
                lista_gastos_actividad
            ], expand=True, spacing=12),
            padding=20
        )
        
        vista_principal.content = vista_detalle
        page.update()

    def actualizar_pantalla_gastos():
        lista_actividades_view.controls.clear()
        
        for act in actividades_gastos:
            def crear_clic_abrir(a=act):
                return lambda e: abrir_detalle_actividad(a)

            card_content = ft.Column([
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.CARD_TRAVEL, color=COLOR_ROJO),
                    title=ft.Text(act["titulo"], weight=ft.FontWeight.BOLD, size=16, color=COLOR_ROJO_OSCURO),
                    subtitle=ft.Text(f"Gastos: {len(act['gastos'])} | Chicas: {', '.join(act['participantes'])}", color=COLOR_TEXTO, size=12),
                ),
                ft.Button(
                    "Ver Cuentas 💖", 
                    on_click=crear_clic_abrir(),
                    style=ft.ButtonStyle(bgcolor=COLOR_ROSA_FUERTE, color=ft.Colors.WHITE)
                )
            ], spacing=5)

            lista_actividades_view.controls.append(
                ft.Card(
                    content=ft.Container(content=card_content, padding=15),
                    bgcolor=COLOR_FONDO_TARJETA,
                    elevation=1
                )
            )

        tab_gastos_principal = ft.Container(
            content=ft.Column([
                ft.Text("Cuentas Compartidas 🥂", size=18, weight=ft.FontWeight.BOLD, color=COLOR_ROJO_OSCURO),
                ft.Text("Crea una actividad o viaje para llevar los gastos ordenados:", color=COLOR_TEXTO, size=13),
                ft.Row([txt_nombre_actividad, ft.Button("Crear Actividad ✨", on_click=crear_actividad, style=ft.ButtonStyle(bgcolor=COLOR_ROJO, color=ft.Colors.WHITE))]),
                ft.Divider(color=COLOR_BORDE),
                ft.Text("❤️ Tus Actividades:", size=16, weight=ft.FontWeight.BOLD, color=COLOR_ROJO_OSCURO),
                lista_actividades_view
            ], expand=True, spacing=12),
            padding=20
        )
        
        vista_principal.content = tab_gastos_principal
        page.update()


    # ==========================================
    # 4. PESTAÑA: PERFIL DE USUARIO
    # ==========================================
    txt_editar_nombre = ft.TextField(
        label="Tu nombre en el grupo", 
        border_color=COLOR_ROSA_FUERTE,
        focused_border_color=COLOR_ROJO,
        expand=True
    )
    lbl_mensaje_perfil = ft.Text("", color=ft.Colors.GREEN_700, size=13)

    def guardar_perfil(e):
        nuevo_nombre = txt_editar_nombre.value.strip()
        if nuevo_nombre:
            nombre_antiguo = usuario_actual["nombre"]
            if nuevo_nombre != nombre_antiguo:
                if nombre_antiguo in amigas_grupo:
                    amigas_grupo.remove(nombre_antiguo)
                if nuevo_nombre not in amigas_grupo:
                    amigas_grupo.append(nuevo_nombre)

                for plan in quedadas_data:
                    if nombre_antiguo in plan["asistentes"]:
                        hora = plan["asistentes"].pop(nombre_antiguo)
                        plan["asistentes"][nuevo_nombre] = hora

                for act in actividades_gastos:
                    if nombre_antiguo in act["participantes"]:
                        act["participantes"].remove(nombre_antiguo)
                        act["participantes"].append(nuevo_nombre)
                    for g in act["gastos"]:
                        if g["pagado_por"] == nombre_antiguo:
                            g["pagado_por"] = nuevo_nombre
                        if nombre_antiguo in g["participantes_gasto"]:
                            g["participantes_gasto"].remove(nombre_antiguo)
                            g["participantes_gasto"].append(nuevo_nombre)

                usuario_actual["nombre"] = nuevo_nombre

            lbl_mensaje_perfil.value = "¡Perfil actualizado con éxito! ✨"
            actualizar_pantalla_perfil()
            page.update()
        else:
            lbl_mensaje_perfil.value = "El nombre no puede estar vacío."
            page.update()

    def actualizar_pantalla_perfil():
        txt_editar_nombre.value = usuario_actual["nombre"]
        
        planes_apuntada = sum(1 for p in quedadas_data if usuario_actual["nombre"] in p["asistentes"])
        actividades_creadas = sum(1 for a in actividades_gastos if usuario_actual["nombre"] in a["participantes"])

        contenido_perfil.controls = [
            ft.Text("✨ Configuración de tu Perfil", size=18, weight=ft.FontWeight.BOLD, color=COLOR_ROJO_OSCURO),
            ft.Text("Aquí puedes modificar tu nombre visible para el resto de amigas.", color=COLOR_TEXTO, size=13),
            ft.Divider(color=COLOR_BORDE),
            ft.Row([txt_editar_nombre, ft.Button("Guardar Cambios 💖", on_click=guardar_perfil, style=ft.ButtonStyle(bgcolor=COLOR_ROJO, color=ft.Colors.WHITE))]),
            lbl_mensaje_perfil,
            ft.Divider(color=COLOR_BORDE),
            ft.Text("📊 Tus Estadísticas en el Grupo:", weight=ft.FontWeight.BOLD, color=COLOR_ROJO_OSCURO),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.AUTO_AWESOME, color=COLOR_ROJO),
                            title=ft.Text(f"Planes apuntada: {planes_apuntada}", weight=ft.FontWeight.BOLD, color=COLOR_ROJO_OSCURO),
                            subtitle=ft.Text(f"Actividades de gastos asociadas: {actividades_creadas}", color=COLOR_TEXTO)
                        )
                    ]),
                    padding=10
                ),
                bgcolor=COLOR_FONDO_TARJETA,
                elevation=1
            ),
            ft.Container(expand=True),
            ft.OutlinedButton(
                "Cerrar Sesión 🚪", 
                on_click=lambda e: reiniciar_sesion(),
                style=ft.ButtonStyle(color=COLOR_ROJO)
            )
        ]
        page.update()

    def reiniciar_sesion():
        usuario_actual["nombre"] = ""
        txt_nombre.value = ""
        error_login.value = ""
        page.navigation_bar = None
        vista_principal.content = pantalla_login
        page.update()

    contenido_perfil = ft.Column(expand=True, spacing=15)
    tab_perfil = ft.Container(content=contenido_perfil, padding=20, expand=True)


    # ==========================================
    # 5. NAVEGACIÓN Y CAMBIO DE PANTALLAS
    # ==========================================
    def cambiar_pestana(e):
        index = e.control.selected_index
        if index == 0:
            actualizar_lista_planes()
            vista_principal.content = tab_quedadas
        elif index == 1:
            actualizar_pantalla_gastos()
        elif index == 2:
            actualizar_pantalla_perfil()
            vista_principal.content = tab_perfil
        page.update()

    def cargar_pantalla_principal():
        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.EVENT_NOTE, label="Quedadas"),
                ft.NavigationBarDestination(icon=ft.Icons.RECEIPT_LONG, label="Gastos"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Mi Perfil"),
            ],
            on_change=cambiar_pestana,
            bgcolor="#FFF0F3",
            indicator_color=COLOR_ROSA_FUERTE
        )
        actualizar_lista_planes()
        vista_principal.content = tab_quedadas
        page.update()

    vista_principal.content = pantalla_login
    page.add(vista_principal)

ft.run(main)