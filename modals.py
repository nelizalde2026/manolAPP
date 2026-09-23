import flet as ft
from typing import Callable, Optional


def mostrar_alerta(
    page: ft.Page,
    titulo: str,
    mensaje: str,
    es_exito: bool = True,
    on_close: Optional[Callable[[], None]] = None,
):
    """Muestra un diálogo modal flotante reutilizable compatible con cualquier versión de Flet."""

    def cerrar_alerta(e):
        dlg.open = False
        page.update()
        if on_close:
            on_close()

    color_titulo = "green" if es_exito else "#D32F2F"

    dlg = ft.AlertDialog(
        title=ft.Text(titulo, weight=ft.FontWeight.BOLD, color=color_titulo),
        content=ft.Text(mensaje, size=13),
        actions=[ft.TextButton("¡Entendido! ✨", on_click=cerrar_alerta)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Asignamos y abrimos usando la sintaxis estándar de Flet silenciando al editor
    page.dialog = dlg  # type: ignore
    dlg.open = True  # type: ignore
    page.update()
