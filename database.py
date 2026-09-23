import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# Configura tus credenciales de Supabase aquí o mediante variables de entorno
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FUNCIONES DE BASE DE DATOS ---


def obtener_amigas():
    res = supabase.table("amigas").select("nombre").execute()
    return [row["nombre"] for row in res.data]


def registrar_o_verificar_amiga(nombre):
    # Verifica si existe, si no, la inserta
    res = supabase.table("amigas").select("*").eq("nombre", nombre).execute()
    if not res.data:
        supabase.table("amigas").insert({"nombre": nombre}).execute()


def actualizar_nombre_amiga(nombre_antiguo, nombre_nuevo):
    supabase.table("amigas").update({"nombre": nombre_nuevo}).eq(
        "nombre", nombre_antiguo
    ).execute()


# Quedadas
def obtener_quedadas():
    res = supabase.table("quedadas").select("*, asistentes(amiga, hora)").execute()
    return res.data


def crear_quedada(titulo, desc):
    res = supabase.table("quedadas").insert({"titulo": titulo, "desc": desc}).execute()
    return res.data


def apuntarse_quedada(quedada_id, amiga, hora):
    supabase.table("asistentes").upsert(
        {"quedada_id": quedada_id, "amiga": amiga, "hora": hora},
        on_conflict="quedada_id,amiga",
    ).execute()


def desapuntarse_quedada(quedada_id, amiga):
    supabase.table("asistentes").delete().eq("quedada_id", quedada_id).eq(
        "amiga", amiga
    ).execute()


# Gastos y Actividades
def obtener_actividades():
    res = (
        supabase.table("actividades")
        .select(
            "*, participantes_actividad(amiga), gastos(*, participantes_gasto(amiga))"
        )
        .execute()
    )
    return res.data


def crear_actividad(titulo, creadora):
    res = supabase.table("actividades").insert({"titulo": titulo}).execute()
    if res.data:
        act_id = res.data[0]["id"]
        # Añadir creadora por defecto como participante
        supabase.table("participantes_actividad").insert(
            {"actividad_id": act_id, "amiga": creadora}
        ).execute()


def crear_actividad_con_participantes(titulo, lista_participantes):
    try:
        # 1. Crear la actividad
        res = supabase.table("actividades").insert({"titulo": titulo}).execute()
        if res.data:
            act_id = res.data[0]["id"]

            # 2. Insertar todos los participantes seleccionados o añadidos
            for amiga in lista_participantes:
                supabase.table("participantes_actividad").insert(
                    {"actividad_id": act_id, "amiga": amiga}
                ).execute()

            return True, "¡Actividad creada con éxito! ✨"
        return False, "No se pudo crear la actividad"
    except Exception as e:
        return False, f"Error al crear la actividad: {str(e)}"


def agregar_gasto(actividad_id, concepto, pagado_por, importe, participantes):
    # Insertar gasto
    g_res = (
        supabase.table("gastos")
        .insert(
            {
                "actividad_id": actividad_id,
                "concepto": concepto,
                "pagado_por": pagado_por,
                "importe": importe,
            }
        )
        .execute()
    )

    if g_res.data:
        gasto_id = g_res.data[0]["id"]
        # Insertar participantes del gasto
        for p in participantes:
            supabase.table("participantes_gasto").insert(
                {"gasto_id": gasto_id, "amiga": p}
            ).execute()

            # Asegurar que esté en participantes de la actividad
            supabase.table("participantes_actividad").upsert(
                {"actividad_id": actividad_id, "amiga": p},
                on_conflict="actividad_id,amiga",
            ).execute()


def autenticar_o_registrar_amiga(nombre_usuario, nombre_completo, password, foto=""):
    res = (
        supabase.table("amigas")
        .select("*")
        .eq("nombre_usuario", nombre_usuario)
        .execute()
    )
    if res.data:
        # La usuaria ya existe, comprobamos contraseña
        usuario = res.data[0]
        if usuario.get("password") == password:
            return True, "Login correcto"
        else:
            return False, "Contraseña incorrecta ❌"
    else:
        # No existe, la registramos por primera vez
        supabase.table("amigas").insert(
            {
                "nombre_usuario": nombre_usuario,
                "nombre_completo": nombre_completo,
                "password": password,
                "foto": foto,
            }
        ).execute()
        return True, "¡Registrada con éxito! ✨"


def obtener_amigas():
    res = supabase.table("amigas").select("nombre_usuario").execute()
    # Devolvemos una lista con los nombres de usuario
    return [a["nombre_usuario"] for a in res.data]


def admin_crear_amiga(nombre_usuario, nombre_completo, email, password, foto=""):
    try:
        supabase.table("amigas").insert(
            {
                "nombre_usuario": nombre_usuario,
                "nombre_completo": nombre_completo,
                "email": email,
                "password": password,
                "foto": foto,
            }
        ).execute()
        return True, "Amiga creada con éxito por el Admin ✨"
    except Exception as e:
        return False, f"Error al crear: {str(e)}"


def actualizar_perfil_amiga(
    nombre_actual, nuevo_usuario, nombre_completo, email, password, foto
):
    try:
        supabase.table("amigas").update(
            {
                "nombre_usuario": nuevo_usuario,
                "nombre_completo": nombre_completo,
                "email": email,
                "password": password,
                "foto": foto,
            }
        ).eq("nombre_usuario", nombre_actual).execute()
        return True, "¡Perfil actualizado con éxito! ✨"
    except Exception as e:
        return False, f"Error al actualizar: {str(e)}"


# --- FUNCIONES PARA SONDEOS Y CALENDARIO DE QUEDADAS ---


def crear_quedada_con_tipo(titulo, descripcion, fecha_fija, tipo_plan, creadora):
    try:
        supabase.table("quedadas").insert(
            {
                "titulo": titulo,
                "descripcion": descripcion,
                "fecha": fecha_fija,
                "tipo_plan": tipo_plan,  # 'fijo' o 'sondeo'
                "creadora": creadora,
            }
        ).execute()
        return True, "¡Plan creado con éxito! 💖"
    except Exception as e:
        return False, f"Error al crear el plan: {str(e)}"


def guardar_disponibilidad(id_quedada, amiga, fecha, disponible, hora_llegada=""):
    try:
        # Comprobamos si ya votó este día para actualizarlo o insertarlo nuevo
        existente = (
            supabase.table("disponibilidad_quedadas")
            .select("id")
            .eq("id_quedada", id_quedada)
            .eq("amiga", amiga)
            .eq("fecha", fecha)
            .execute()
        )

        if existente.data:
            # Actualizamos el registro existente
            reg_id = existente.data[0]["id"]
            supabase.table("disponibilidad_quedadas").update(
                {"disponible": disponible, "hora_llegada": hora_llegada}
            ).eq("id", reg_id).execute()
        else:
            # Insertamos nuevo registro
            supabase.table("disponibilidad_quedadas").insert(
                {
                    "id_quedada": id_quedada,
                    "amiga": amiga,
                    "fecha": fecha,
                    "disponible": disponible,
                    "hora_llegada": hora_llegada,
                }
            ).execute()

        return True
    except Exception as e:
        print("Error al guardar disponibilidad:", e)
        return False


def obtener_disponibilidad_quedada(id_quedada):
    try:
        res = (
            supabase.table("disponibilidad_quedadas")
            .select("*")
            .eq("id_quedada", id_quedada)
            .execute()
        )
        return res.data
    except Exception as e:
        print("Error al obtener disponibilidad:", e)
        return []


def eliminar_quedada(id_quedada):
    try:
        # Borrar primero las disponibilidades asociadas a este plan
        supabase.table("disponibilidad_quedadas").delete().eq(
            "id_quedada", id_quedada
        ).execute()
        # Borrar el plan principal
        supabase.table("quedadas").delete().eq("id", id_quedada).execute()
        return True, "¡Plan eliminado con éxito! 🗑️"
    except Exception as e:
        return False, f"Error al eliminar el plan: {str(e)}"


def apuntarse_plan_fijo(id_quedada, amiga, fecha_plan, hora_llegada=""):
    try:
        # Comprobamos si ya está apuntada para actualizar o insertar
        existente = (
            supabase.table("disponibilidad_quedadas")
            .select("id")
            .eq("id_quedada", id_quedada)
            .eq("amiga", amiga)
            .eq("fecha", fecha_plan)
            .execute()
        )

        if existente.data:
            reg_id = existente.data[0]["id"]
            supabase.table("disponibilidad_quedadas").update(
                {"disponible": True, "hora_llegada": hora_llegada}
            ).eq("id", reg_id).execute()
        else:
            supabase.table("disponibilidad_quedadas").insert(
                {
                    "id_quedada": id_quedada,
                    "amiga": amiga,
                    "fecha": fecha_plan,
                    "disponible": True,
                    "hora_llegada": hora_llegada,
                }
            ).execute()

        return True, "¡Te has apuntado con éxito! 💖"
    except Exception as e:
        return False, f"Error al apuntarse: {str(e)}"


import datetime

# (Supone que ya tienes tus funciones anteriores de actividades y gastos)

import datetime


def agregar_gasto_avanzado(
    actividad_id, concepto, pagado_por, importe, participantes, categoria
):
    try:
        # 1. Insertar el gasto incluyendo la categoría
        g_res = (
            supabase.table("gastos")
            .insert(
                {
                    "actividad_id": actividad_id,
                    "concepto": concepto,
                    "pagado_por": pagado_por,
                    "importe": importe,
                    "categoria": categoria,
                }
            )
            .execute()
        )

        if g_res.data:
            gasto_id = g_res.data[0]["id"]

            # 2. Insertar los participantes de este gasto específico
            for p in participantes:
                supabase.table("participantes_gasto").insert(
                    {"gasto_id": gasto_id, "amiga": p}
                ).execute()

                # Asegurar que esté apuntada en los participantes generales de la actividad
                supabase.table("participantes_actividad").upsert(
                    {"actividad_id": actividad_id, "amiga": p},
                    on_conflict="actividad_id,amiga",
                ).execute()

        return True
    except Exception as e:
        print("Error al agregar gasto avanzado:", e)
        return False


def marcar_deuda_saldada(actividad_id, deudor, acreedor, monto):
    try:
        # Como estamos en Supabase, podemos registrar el pago saldado como un gasto especial
        # o un concepto negativo, o simplemente agregarlo como un gasto de liquidación.
        # Por ejemplo, registramos un gasto de tipo liquidación:
        supabase.table("gastos").insert(
            {
                "actividad_id": actividad_id,
                "concepto": f"💸 Pago de {deudor} a {acreedor} (Saldado)",
                "pagado_por": deudor,
                "importe": monto,
                "categoria": "✨ Varios",
            }
        ).execute()

        # Y metemos a la acreedora como única participante para que compense el balance
        g_res = (
            supabase.table("gastos")
            .select("id")
            .eq("actividad_id", actividad_id)
            .order("id", desc=True)
            .limit(1)
            .execute()
        )

        if g_res.data:
            gasto_id = g_res.data[0]["id"]
            supabase.table("participantes_gasto").insert(
                {"gasto_id": gasto_id, "amiga": acreedor}
            ).execute()

        return True
    except Exception as e:
        print("Error al marcar deuda como saldada:", e)
        return False
