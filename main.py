import flet as ft
import urllib.parse

def main(page: ft.Page):
    page.title = "Ouvrir WhatsApp"

    def ouvrir_whatsapp(e):
        numero = "22871075241"  # numéro sans +
        message = "Bonjour, je vous contacte depuis mon application"

        msg_encoded = urllib.parse.quote(message)

        # Schéma Android (le plus fiable)
        url = f"whatsapp://send?phone={numero}&text={msg_encoded}"

        try:
            page.launch_url(url)
        except Exception:
            # fallback web
            page.launch_url(f"https://wa.me/{numero}?text={msg_encoded}")

    page.add(
        ft.ElevatedButton(
            text="Ouvrir WhatsApp",
            on_click=ouvrir_whatsapp
        )
    )

ft.app(target=main)
