import itertools
import flet as ft
import sqlite3
import json
import logging
CP = "#5D8A66"
# --- 1. DÉFINITION DES SOURCES (STRUCTURE DES MENUS) ---
# Ces dictionnaires servent de "moules" pour créer les combinaisons.
basesa1 = {"TEKON(IGNAME BOULLIE)": 0, "ABLO": 0, "DJINKOUME": 0, "COUSCOUS": 0, "TIMBANI": 0, "SPAGHETTI": 0}
proteinesa1 = {"RIEN": 0, "AKPALAN(POISSON FUME)": 0, "DEUEVI(PETIT POISSON)": 0, "APKALAN KANAMI(POISSON FRIT)": 0,
               "AKPAME(PEAU DE BOEUF)": 0, "AGLAN(CRABE)": 0}
saucesa1 = {"TOMATE": 0, "ADEME": 0, "GBOMA": 0, "ARACHIDE": 0}

bases2a1 = {"KOLIKO": 0, "RIZ": 0, "AMANDA(ALLOCO)": 0, "AYIMOLOU": 0}
proteines2a1 = {"RIEN": 0, "POULET": 0, "BOEUF": 0, "MOUTON": 0, "CREVETTE": 0, "APKALAN KANAMI(POISSON FRIT)": 0}
sauces2a1 = {"TOMATE": 0}


# --- 2. CALCUL DES COÛTS UNITAIRES TOGOLAIS ---
lisa={}#------------------------------------------------------------------------------------------------------
#generateur 4-8
#-------------------------------------------------------------------------------------------------------------------------
basesa ={"TEKON(IGNAME BOULLIE)":3,"ABLO":5000,"DJINKOUME":20000,"COUSCOUS":5000,"KOLIKO":1000,"TIMBANI":1500,"RIZ":700,"AMANDA(ALLOCO)":2000,"AYIMOLOU":1000,"SPAGHETTI":500}
proteinesa={"AKPALAN(POISSON FUME)":10,"DEUEVI(PETIT POISSON)":10,"APKALAN KANAMI(POISSON FRIT)":10,"POULET":10,"BOEUF":10,"MOUTON":10,"AKPAME(PEAU DE BOEUF)":10,"AGLAN(CRABE)":10,"CREVETTE":10}
saucesa={"TOMATE":500,}
bases2a ={"FOUFOU IGNAME":1500,"FOUFOU PLANTAIN":1800,"AKOUME(PATE MAIS)":1700,"EMAKUME(PATE MAIS FERMENTE)":1800,"Riz":1000}
proteines2a={"AKPALAN(POISSON FUME)":10,"DEUEVI(PETIT POISSON)":10,"APKALAN KANAMI(POISSON FRIT)":10,"POULET":10,"BOEUF":10,"MOUTON":10,"AKPAME(PEAU DE BOEUF)":10,"AGLAN(CRABE)":10,"CREVETTE":10}
sauces2a={"GBOMA":1500,"TOMATE":100,"GOUSSI":510,"ADEME":810,"FETRI(GOMBO)":410,"KODORO":610,"GNATOU":110,"ARACHIDE":210,"CHOU":310,"FETRI POUPOU(GONBO SEC)":410,"DEKOU(GRAINE)":510,"EBESSESSI":610,}
dicsa={
    "DEGUE":1000,"TAPIOCA ZOGBON":1000,"ATTIEKE POISSON":1000,"SPAGHETTI BLANC":1000,"SALADE":1000
}
lisa.update(dicsa)
combinaisons=list(itertools.product(basesa.keys(),proteinesa.keys(),saucesa.keys()))
combinaisons2=list(itertools.product(bases2a.keys(),proteines2a.keys(),sauces2a.keys()))

def afficfer(combia):
    basesa,proteinesa,saucesa = combia
def afficfer2(combi2a):
    base2a,proteine2a,sauce2a = combi2a

for combia in combinaisons:
    afficfer(combia)
    noma=f"{combia[0]} Sauce {combia[2]} avec {combia[1]}"
    valeura=basesa[combia[0]]+proteinesa[combia[1]]+saucesa[combia[2]]
    lisa[noma]= int(valeura)
for combi2a in combinaisons2:
    afficfer2(combi2a)
    nom2a = f"{combi2a[0]} Sauce {combi2a[2]} avec {combi2a[1]}"
    valeur2a = bases2a[combi2a[0]] + proteines2a[combi2a[1]] + sauces2a[combi2a[2]]
    lisa[nom2a] = int(valeur2a)

#---------------------------------------------------------------------------------------------
#generateur 1-3
#---------------------------------------------------------------------------------------------
lis={}
bases2 ={"TEKON(IGNAME BOULLIE)":3,"ABLO":5000,"DJINKOUME":20000,"COUSCOUS":5000,"KOLIKO":1000,"TIMBANI":1500,"RIZ":700,"AMANDA(ALLOCO)":2000,"AYIMOLOU":1000,"SPAGHETTI":500}
proteines2={"AKPALAN(POISSON FUME)":10,"DEUEVI(PETIT POISSON)":10,"APKALAN KANAMI(POISSON FRIT)":10,"POULET":10,"BOEUF":10,"MOUTON":10,"AKPAME(PEAU DE BOEUF)":10,"AGLAN(CRABE)":10,"CREVETTE":10}
sauces2={"TOMATE":500,}
bases={"FOUFOU IGNAME":1500,"FOUFOU PLANTAIN":1800,"AKOUME(PATE MAIS)":1700,"EMAKUME(PATE MAIS FERMENTE)":1800,"Riz":1000}
proteines={"AKPALAN(POISSON FUME)":10,"DEUEVI(PETIT POISSON)":10,"APKALAN KANAMI(POISSON FRIT)":10,"POULET":10,"BOEUF":10,"MOUTON":10,"AKPAME(PEAU DE BOEUF)":10,"AGLAN(CRABE)":10,"CREVETTE":10}
sauces={"GBOMA":1500,"TOMATE":100,"GOUSSI":510,"ADEME":810,"FETRI(GOMBO)":410,"KODORO":610,"GNATOU":110,"ARACHIDE":210,"CHOU":310,"FETRI POUPOU(GONBO SEC)":410,"DEKOU(GRAINE)":510,"EBESSESSI":610,}
dic={
    "DEGUE":1000,"TAPIOCA ZOGBON":1000,"ATTIEKE POISSON":1000,"SPAGHETTI BLANC":1000,"SALADE":1000
}
lis.update(dic)
combinaisons=list(itertools.product(bases.keys(),proteines.keys(),sauces.keys()))
combinaisons2=list(itertools.product(bases2.keys(),proteines2.keys(),sauces2.keys()))

def afficfer(combi):
    bases,proteines,sauces = combi
def afficfer2(combi2):
    bases2,proteines2,sauces2 = combi2

for combi in combinaisons:
    afficfer(combi)
    nom=f"{combi[0]} Sauce {combi[2]} avec {combi[1]}"
    valeur=bases[combi[0]]+proteines[combi[1]]+sauces[combi[2]]
    lis[nom]=valeur
for combi2 in combinaisons2:
    afficfer2(combi2)
    nom2 = f"{combi2[0]} Sauce {combi2[2]} avec {combi2[1]}"
    valeur2 = bases2[combi2[0]] + proteines2[combi2[1]] + sauces2[combi2[2]]
    lis[nom2] = valeur2
#----------------------------------------------------------------
#generer
liss={}
bases2s ={"TEKON(IGNAME BOULLIE)":3,"ABLO":5000,"DJINKOUME":20000,"COUSCOUS":5000,"KOLIKO":1000,"TIMBANI":1500,"RIZ":700,"AMANDA(ALLOCO)":2000,"AYIMOLOU":1000,"SPAGHETTI":500}
proteines2s={"AKPALAN(POISSON FUME)":10,"DEUEVI(PETIT POISSON)":10,"APKALAN KANAMI(POISSON FRIT)":10,"POULET":10,"BOEUF":10,"MOUTON":10,"AKPAME(PEAU DE BOEUF)":10,"AGLAN(CRABE)":10,"CREVETTE":10}
sauces2s={"TOMATE":500,}
basess ={"FOUFOU IGNAME":1500,"FOUFOU PLANTAIN":1800,"AKOUME(PATE MAIS)":1700,"EMAKUME(PATE MAIS FERMENTE)":1800,"Riz":1000}
proteiness={"AKPALAN(POISSON FUME)":10,"DEUEVI(PETIT POISSON)":10,"APKALAN KANAMI(POISSON FRIT)":10,"POULET":10,"BOEUF":10,"MOUTON":10,"AKPAME(PEAU DE BOEUF)":10,"AGLAN(CRABE)":10,"CREVETTE":10}
saucess={"GBOMA":1500,"TOMATE":100,"GOUSSI":510,"ADEME":810,"FETRI(GOMBO)":410,"KODORO":610,"GNATOU":110,"ARACHIDE":210,"CHOU":310,"FETRI POUPOU(GONBO SEC)":410,"DEKOU(GRAINE)":510,"EBESSESSI":610,}
dics={
    "DEGUE":1000,"TAPIOCA ZOGBON":1000,"ATTIEKE POISSON":1000,"SPAGHETTI BLANC":1000,"SALADE":1000
}
liss.update(dic)
combinaisonss=list(itertools.product(basess.keys(),proteiness.keys(),saucess.keys()))
combinaisons2s=list(itertools.product(bases2s.keys(),proteines2s.keys(),sauces2s.keys()))

def afficfers(combis):
    basess,proteiness,saucess = combis
def afficfer2s(combi2s):
    bases2s,proteines2s,sauces2s = combi2s

for combis in combinaisonss:
    afficfers(combis)
    noms=f"{combis[0]} Sauce {combis[2]} avec {combis[1]}"
    valeurs=basess[combis[0]]+proteiness[combis[1]]+saucess[combi[2]]
    liss[noms]=valeurs
for combi2s in combinaisons2s:
    afficfer2s(combi2s)
    nom2s = f"{combi2s[0]} Sauce {combi2s[2]} avec {combi2s[1]}"
    valeur2s = bases2s[combi2s[0]] + proteines2s[combi2s[1]] + sauces2s[combi2s[2]]
    liss[nom2s] = valeur2s
#---------------------------------------------------------------------

PLATS_PETIT_COMITE = lis
PLATS_FAMILLE = lisa
PLATS_GRANDE_TABLE = liss


def initialiser_db():
    conn = sqlite3.connect('fidelite.db')
    cursor = conn.cursor()
    # Crée la table si elle n'existe pas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT UNIQUE,
            points INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    return conn


def get_active_dict(nb):
    """Sélectionne dynamiquement le dictionnaire selon le nombre de convives."""
    if nb <= 2: return PLATS_PETIT_COMITE, "Solo/Duo"
    if 3 <= nb <= 6: return PLATS_FAMILLE, "Familiale"
    return PLATS_GRANDE_TABLE, "Grand Groupe"


class ActionButton(ft.ElevatedButton):
    def __init__(self, text, icon, color, bgcolor, expand=False, on_click=None, disabled=False):
        super().__init__()
        self.bgcolor = bgcolor
        self.color = color
        self.expand = expand
        self.on_click = on_click
        self.disabled = disabled  # <--- Cette ligne est cruciale
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        self.content = ft.Row(
            [ft.Icon(icon, size=18), ft.Text(text, size=14, weight="bold")],
            alignment="center",
            spacing=8
        )


def init_db_commandes():
    # Cette fonction crée le fichier et la table si ils n'existent pas
    conn = sqlite3.connect("commandes.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commandes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_commande TEXT,
            nom_plat TEXT,
            prix_total INTEGER,
            ingredients TEXT
        )
    ''')
    conn.commit()
    conn.close()


def init_db():
    try:
        conn = sqlite3.connect("repas_db.sqlite")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS planning 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      date_str TEXT, repas TEXT, cout REAL, timestamp TEXT)''')
        conn.commit()
        conn.close()
    except Exception as e:
       logging.error(f"Erreur SQL Init: {e}")


# --- APPEL CRUCIAL AU DÉMARRAGE ---
init_db_commandes()


def safe_close_and_redirect(page, dialogue, target_view_func):
    # 1. On ferme visuellement le dialogue
    dialogue.open = False
    # 2. On vide tous les overlays (fenêtres flottantes) de la mémoire
    page.overlay.remove(dialogue)
    # 3. On force la mise à jour immédiate pour enlever le blocage
    page.update()
    # 4. On lance la redirection vers la page principale
    target_view_func()


class MarketTile(ft.Container):
    def __init__(self, item, on_update_cart, initial_qty=0):
        # Initialisation du parent SANS créer de méthode init() personnalisée
        super().__init__()

        self.item = item
        self.on_update_cart = on_update_cart
        self.qty = initial_qty

        # Design professionnel
        self.padding = 15
        self.bgcolor = "white"
        self.border_radius = 15
        self.shadow = ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, "black"))

        self.qty_text = ft.Text(str(self.qty), weight="bold", size=16)

        # Construction de l'interface
        self.content = ft.Row([
            ft.Column([
                ft.Text(item["n"], weight="bold", size=16, color="#1B5E20"),
                ft.Text(f"{item['p']} F / {item['u']}", color="grey", size=12),
            ], expand=True, spacing=2),

            ft.Row([
                ft.IconButton(
                    ft.Icons.REMOVE_CIRCLE_OUTLINE,
                    icon_color="red",
                    on_click=self.minus
                ),
                self.qty_text,
                ft.IconButton(
                    ft.Icons.ADD_CIRCLE_OUTLINE,
                    icon_color="green",
                    on_click=self.plus
                ),
            ], spacing=5)
        ], alignment="spaceBetween")

    def plus(self, e):
        self.qty += 1
        self.qty_text.value = str(self.qty)
        self.on_update_cart(self.item["n"], self.qty, self.item["p"])
        self.update()

    def minus(self, e):
        if self.qty > 0:
            self.qty -= 1
            self.qty_text.value = str(self.qty)
            self.on_update_cart(self.item["n"], self.qty, self.item["p"])
            self.update()


# =============================================================================
# 2. GESTION DE LA PERSISTANCE (SQLITE)
# =============================================================================


# =============================================================================
# 3. COMPOSANTS UI RÉUTILISABLES
# =============================================================================
class ActionButton(ft.ElevatedButton):
    def __init__(self, text, icon, color, bgcolor, expand=False, on_click=None, disabled=False):
        # On passe directement les propriétés au parent pour éviter les erreurs
        super().__init__(
            bgcolor=bgcolor,
            color=color,
            expand=expand,
            on_click=on_click,
            disabled=disabled,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
        )
        # On définit le contenu visuel (Icône + Texte)
        self.content = ft.Row(
            [ft.Icon(icon, size=18), ft.Text(text, size=14, weight="bold")],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8
        )


def create_section_header(title, date_text):
    return ft.Container(
        content=ft.Row([
            ft.Text(title, color="white", weight="bold", size=16),
            ft.Row([
                ft.Icon(ft.Icons.CALENDAR_TODAY, color="white", size=14),
                ft.Text(date_text, color="white", size=12)
            ], spacing=5)
        ], alignment="spaceBetween"),
        bgcolor=CP,
        padding=15,
        border_radius=ft.border_radius.only(top_left=15, bottom_right=15),
        margin=ft.margin.only(top=10, bottom=15)
    )


def est_commande(plat_name, shipping_date):
    """Vérifie si CE plat est commandé pour CETTE date précise"""
    try:
        conn = sqlite3.connect("commandes.db")
        c = conn.cursor()
        # On cherche le nom ET la date exacte de livraison
        c.execute("SELECT 1 FROM commandes WHERE nom_plat = ? AND date_commande = ?",
                  (plat_name, shipping_date))
        existe = c.fetchone() is not None
        conn.close()
        return existe
    except:
        return False


# 4. CŒUR DE L'APPLICATION
# =============================================================================
def users():
    SESSION_FILE = "session_utilisateur.txt"
    """Récupère les infos de l'utilisateur stockées localement"""
    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            # On charge le dictionnaire stocké par json.dumps
            return json.loads(f.read())
    except:
        return {"nom": "Client Inconnu", "tel": "Non spécifié"}
