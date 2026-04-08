import threading
import flet as ft
import pyrebase
import time

# --- CONFIGURATION FIREBASE ---
config = {
    "apiKey": "AIzaSyCLcq-6e7a02DkJJDKGc24z3psQ09Lk9Cw",
    "authDomain": "cliexe-apk.firebaseapp.com",
    "projectId": "cliexe-apk",
    "storageBucket": "cliexe-apk.firebasestorage.app",
    "databaseURL": "https://cliexe-apk-default-rtdb.firebaseio.com"
}

db = pyrebase.initialize_app(config).database()


# --- DESIGN SYSTEM ---
class Design:
    BG = "#F0F2F5"
    CARD_BG = "#FFFFFF"
    ACCENT_BLUE = "#1A73E8"
    ACCENT_GREEN = "#34A853"
    ACCENT_ORANGE = "#FBBC04"
    ACCENT_RED = "#EA4335"
    TEXT_MAIN = "#202124"
    TEXT_SUB = "#5F6368"
    BORDER = "#DADCE0"


class AdminApp(ft.Column):
    def __init__(self, main_page: ft.Page):
        super().__init__(expand=True)
        self.app_page = main_page
        self.current_data = {"commandes": {}, "annulations": {}, "users": {}}
        self.last_cmd_count = 0
        self.view_content = ft.Column(expand=True, scroll="auto", spacing=20)

        self.nav_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.INSERT_CHART_ROUNDED, label="Analyses"),
                ft.NavigationBarDestination(icon=ft.Icons.PEOPLE_ALT_ROUNDED, label="Clients"),
                ft.NavigationBarDestination(icon=ft.Icons.RESTAURANT_MENU, label="Kits"),
                ft.NavigationBarDestination(icon=ft.Icons.STORE_ROUNDED, label="Marché"),
                ft.NavigationBarDestination(icon=ft.Icons.MONETIZATION_ON_ROUNDED, label="Prêts"),
                ft.NavigationBarDestination(icon=ft.Icons.NOT_INTERESTED_ROUNDED, label="Annul."),
            ],
            on_change=self.handle_nav_change,
            bgcolor=Design.CARD_BG,
        )

        self.controls = [ft.Container(content=self.view_content, padding=20, expand=True)]
        self.sync_and_show(0)

    def trigger_alert(self, title, message):
        def close_dlg(e):
            alert_dlg.open = False
            self.app_page.update()

        alert_dlg = ft.AlertDialog(
            title=ft.Row([ft.Icon(ft.Icons.NEW_RELEASES, color=Design.ACCENT_ORANGE), ft.Text(title)]),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=close_dlg)]
        )
        self.app_page.overlay.append(alert_dlg)
        alert_dlg.open = True
        self.app_page.update()

    def sync_and_show(self, index, silent=False):
        try:
            new_cmds = db.child("commandes").get().val() or {}
            new_annul = db.child("annulations_demandes").get().val() or {}
            new_users = db.child("users").get().val() or {}

            if self.last_cmd_count > 0 and len(new_cmds) > self.last_cmd_count:
                last_key = list(new_cmds.keys())[-1]
                cmd = new_cmds[last_key]
                self.trigger_alert("Nouvelle Commande", f"Client: {cmd.get('nom', cmd.get('info', 'Inconnu'))}\nType: {cmd.get('type')}")

            self.current_data["commandes"] = new_cmds
            self.current_data["annulations"] = new_annul
            self.current_data["users"] = new_users
            self.last_cmd_count = len(new_cmds)

            if not silent:
                self.app_page.snack_bar = ft.SnackBar(
                    content=ft.Text("Données actualisées ✅", size=12),
                    bgcolor=Design.ACCENT_GREEN,
                    duration=1000
                )
                self.app_page.snack_bar.open = True

            self.render_page(index)
        except Exception as e:
            print(f"Erreur Sync: {e}")

    def handle_nav_change(self, e):
        self.render_page(e.control.selected_index)

    def render_page(self, index):
        self.view_content.controls.clear()
        if index == 0: self.draw_advanced_dashboard()
        elif index == 1: self.draw_users_list()
        elif index == 2: self.draw_filtered_list("KIT_CUISINE")
        elif index == 3: self.draw_filtered_list("MARCHÉ")
        elif index == 4: self.draw_filtered_list("DEMANDE_PRET")
        elif index == 5: self.draw_annulations()
        self.app_page.update()

    def draw_advanced_dashboard(self):
        cmds = list(self.current_data["commandes"].values())
        total_ca, count_kits, count_marche, count_prets = 0, 0, 0, 0
        for c in cmds:
            t = c.get("type")
            if t == "KIT_CUISINE": count_kits += 1
            elif t == "MARCHÉ": count_marche += 1
            elif t == "DEMANDE_PRET": count_prets += 1
            price_str = str(c.get("total_paye", "0"))
            val = int("".join(filter(str.isdigit, price_str)) or 0)
            if t != "DEMANDE_PRET": total_ca += val

        panier_moyen = total_ca / (count_kits + count_marche) if (count_kits + count_marche) > 0 else 0
        self.view_content.controls.extend([
            ft.Text("Tableau de Bord", size=28, weight="bold", color=Design.TEXT_MAIN),
            ft.Container(
                content=ft.Column([
                    ft.Text("CHIFFRE D'AFFAIRES TOTAL", color="white70", size=11, weight="bold"),
                    ft.Text(f"{total_ca:,} FCFA".replace(",", " "), color="white", size=32, weight="heavy"),
                    ft.Row([ft.Icon(ft.Icons.AUTO_GRAPH, color="white70", size=16),
                            ft.Text(f"Panier moyen : {int(panier_moyen):,} F", color="white70", size=14)])
                ]),
                gradient=ft.LinearGradient([Design.ACCENT_BLUE, "#0D47A1"]),
                padding=25, border_radius=20,
            ),
            ft.Row([self.simple_stat("Kits", count_kits, Design.ACCENT_GREEN),
                    self.simple_stat("Marché", count_marche, Design.ACCENT_ORANGE)], spacing=10),
            ft.Row([self.simple_stat("Prêts", count_prets, Design.ACCENT_BLUE),
                    self.simple_stat("Annul.", len(self.current_data["annulations"]), Design.ACCENT_RED)], spacing=10),
        ])

    def simple_stat(self, label, val, color):
        return ft.Container(
            expand=True, bgcolor=Design.CARD_BG, padding=15, border_radius=15,
            border=ft.border.all(1, Design.BORDER),
            content=ft.Column([
                ft.Text(label, size=12, color=Design.TEXT_SUB, weight="bold"),
                ft.Text(str(val), size=22, weight="bold", color=color),
            ], spacing=2)
        )

    def draw_filtered_list(self, target_type):
        for k, v in reversed(list(self.current_data["commandes"].items())):
            if v.get("type") == target_type:
                details_container = ft.Column(spacing=5)

                # --- CAS SPÉCIFIQUE : PRÊTS ---
                if target_type == "DEMANDE_PRET":
                    details_container.controls.append(
                        ft.Container(
                            content=ft.Column([
                                ft.Row([ft.Icon(ft.Icons.MONETIZATION_ON, color=Design.ACCENT_BLUE),
                                        ft.Text(f"MONTANT : {v.get('montant', 'N/A')}", weight="bold", size=16)]),
                                ft.Row([ft.Icon(ft.Icons.CALENDAR_TODAY, color=Design.TEXT_SUB),
                                        ft.Text(f"DURÉE : {v.get('duree', 'N/A')}")]),
                            ], spacing=8),
                            padding=10, bgcolor="#F8F9FA", border_radius=10
                        )
                    )

                # --- CAS SPÉCIFIQUE : KITS ET MARCHÉ ---
                else:
                    # Affichage du Nom du Plat (spécifique au Kit Cuisine)
                    if v.get("nom_plat"):
                        details_container.controls.append(
                            ft.Text(v.get("nom_plat").upper(), weight="heavy", color=Design.ACCENT_BLUE, size=16)
                        )
                        details_container.controls.append(ft.Divider(height=1, color=Design.BORDER))

                    # Affichage du contenu du panier
                    panier = v.get("panier", {})
                    if isinstance(panier, list):
                        for item in panier:
                            details_container.controls.append(ft.Text(f"• {item}", size=13))
                    elif isinstance(panier, dict):
                        for n, info in panier.items():
                            qty = info.get('qty', '1')
                            details_container.controls.append(ft.Text(f"• {n} (x{qty})", size=13))

                # --- RENDU DE LA CARTE ---
                self.view_content.controls.append(
                    ft.Container(
                        bgcolor=Design.CARD_BG, padding=20, border_radius=15, border=ft.border.all(1, Design.BORDER),
                        content=ft.Column([
                            ft.Row([
                                ft.Container(
                                    content=ft.Text(target_type, size=10, color="white", weight="bold"),
                                    bgcolor=Design.ACCENT_ORANGE if target_type == "DEMANDE_PRET" else Design.ACCENT_GREEN,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                    border_radius=5
                                ),
                                ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color=Design.ACCENT_RED,
                                              on_click=lambda _, key=k: self.delete_entry("commandes", key))
                            ], alignment="spaceBetween"),

                            ft.Text(v.get("info", "Client"), size=20, weight="bold"),
                            ft.Row(
                                [ft.Icon(ft.Icons.PHONE, size=14), ft.Text(v.get("telephone", "N/A"), weight="bold")]),
                            ft.Text(f"📍 {v.get('ville', '')} - {v.get('quartier', '')}", size=12,
                                    color=Design.TEXT_SUB),

                            ft.Divider(height=20, color=Design.BG),

                            ft.Container(bgcolor="#F8F9FA", padding=15, border_radius=10, content=details_container),

                            ft.Row([
                                ft.Text("TOTAL À ENCAISSER", size=11, weight="bold"),
                                ft.Text(v.get("total_paye", "0 FCFA"), size=18, weight="heavy",
                                        color=Design.ACCENT_GREEN)
                            ], alignment="spaceBetween") if target_type != "DEMANDE_PRET" else ft.Container()
                        ])
                    )
                )

    def draw_users_list(self):
        self.view_content.controls.append(ft.Text("Répertoire Clients", size=28, weight="bold", color=Design.TEXT_MAIN))
        users = self.current_data.get("users", {})
        commandes = self.current_data.get("commandes", {}).values()
        for u_id, u_info in users.items():
            name = u_info.get("nom", "Inconnu")
            tel = u_info.get("tel", "")
            nb = sum(1 for c in commandes if str(c.get("telephone")) == str(tel))
            self.view_content.controls.append(
                ft.Container(
                    bgcolor=Design.CARD_BG, padding=15, border_radius=15, border=ft.border.all(1, Design.BORDER),
                    content=ft.Row([
                        ft.CircleAvatar(content=ft.Text(name[0].upper()), bgcolor=Design.ACCENT_BLUE, color="white"),
                        ft.Column([ft.Text(name, weight="bold"), ft.Text(f"📞 {tel}", size=12)], expand=True),
                        ft.Container(content=ft.Text(str(nb), weight="bold"), padding=10, bgcolor=Design.BG, border_radius=10)
                    ])
                )
            )

    def draw_annulations(self):
        # Titre de la section
        self.view_content.controls.append(
            ft.Text("Demandes d'Annulation", size=28, weight="bold", color=Design.TEXT_MAIN)
        )

        annulations = self.current_data.get("annulations", {})

        if not annulations:
            self.view_content.controls.append(
                ft.Container(
                    content=ft.Text("Aucune demande d'annulation en cours.", color=Design.TEXT_SUB),
                    padding=20, alignment=ft.Alignment(0,0)
                )
            )
            return

        for k, v in reversed(list(annulations.items())):
            self.view_content.controls.append(
                ft.Container(
                    bgcolor=Design.CARD_BG,
                    padding=20,
                    border_radius=15,
                    border=ft.border.all(1, Design.ACCENT_RED),
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text("ANNULATION", size=10, color="white", weight="bold"),
                                bgcolor=Design.ACCENT_RED,
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=5
                            ),
                            ft.Text(v.get("date_action", ""), size=11, color=Design.TEXT_SUB)
                        ], alignment="spaceBetween"),

                        ft.Text(v.get("client", "Anonyme"), size=18, weight="bold"),
                        ft.Text(f"📞 Contact : {v.get('telephone')}", color=Design.ACCENT_BLUE, weight="bold"),
                        ft.Text(f"📍 {v.get('ville', '')}, {v.get('quartier', '')}", size=12),

                        ft.Divider(height=10, color="transparent"),

                        ft.Container(
                            bgcolor="#FFF5F5",
                            padding=15,
                            border_radius=10,
                            content=ft.Column([
                                ft.Text("PRODUIT À ANNULER :", size=10, weight="bold", color=Design.ACCENT_RED),
                                ft.Text(v.get("nom_plat", "Plat inconnu"), size=16, weight="bold"),
                                ft.Text(f"Statut : {v.get('statut', 'Reçue')}", italic=True, size=12),
                            ])
                        ),

                        ft.Row([
                            ft.ElevatedButton(
                                "Traiter & Supprimer",
                                icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                                bgcolor=Design.ACCENT_RED,
                                color="white",
                                on_click=lambda _, key=k: self.delete_entry("annulations_demandes", key)
                            )
                        ], alignment="end")
                    ], spacing=10)
                )
            )

    def delete_entry(self, node, item_id):
        db.child(node).child(item_id).remove()
        self.sync_and_show(self.nav_bar.selected_index)


def main(page: ft.Page):
    page.title = "Cliexe Analytics Pro"
    page.bgcolor = Design.BG
    page.theme_mode = ft.ThemeMode.LIGHT

    app_logic = AdminApp(page)
    header = ft.Container(
        padding=ft.padding.only(20, 40, 20, 10),
        content=ft.Row([
            ft.Text("GESTION PRO", weight="bold", size=22),
            ft.IconButton(ft.Icons.REFRESH, on_click=lambda _: app_logic.sync_and_show(app_logic.nav_bar.selected_index))
        ], alignment="spaceBetween")
    )

    page.navigation_bar = app_logic.nav_bar
    page.add(header, app_logic)

    def auto_refresh():
        while True:
            time.sleep(2)
            try:

                app_logic.sync_and_show(app_logic.nav_bar.selected_index, silent=False)
                page.update()
            except: pass

    thread = threading.Thread(target=auto_refresh, daemon=True)
    thread.start()

ft.app(target=main)

