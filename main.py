import flet as ft

def main(page: ft.Page):
    page.add(ft.Text("✅ FLET ПРАЦЮЄ!", size=35, color="green", weight="bold"))

ft.app(target=main)
