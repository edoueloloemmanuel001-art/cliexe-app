import time
import sys
import flet as ft
import random
from datetime import datetime, timedelta
import sqlite3
import logging
import json
import requests
import pyrebase
import os

CONFIG_FILE = ".app_config.json"
config = {
    "apiKey": "AIzaSyCLcq-6e7a02DkJJDKGc24z3psQ09Lk9Cw",
    "authDomain": "cliexe-apk.firebaseapp.com",
    "projectId": "cliexe-apk",
    "storageBucket": "cliexe-apk.firebasestorage.app",
    "messagingSenderId": "444886785936",
    "appId": "1:444886785936:web:8b0f997d8da3e085161d15",
    "databaseURL": "https://cliexe-apk-default-rtdb.firebaseio.com"
}

# Initialisation globale
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
CP = "#5D8A66"  # Vert Primaire
CS = "#4A6D52"  # Vert Secondaire
CA = "#D1E0D5"  # Vert Accent (pour les puces/chips)
CBG = "#F8F9FA"  # Fond de page
CC = "#FFFFFF"  # Fond de carte
CT1 = "#2D2D2D"  # Texte Titre
CT2 = "#757575"  # Texte Sous-titre
CERR = "#D32F2F"  # Rouge Erreur

DELIVERY_TODAY = 500
DELIVERY_TOMORROW = 300
# --- CONFIGURATION VISUELLE ---
JOURS_FR = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
MOIS_FR = ["Janv.", "Févr.", "Mars", "Avril", "Mai", "Juin", "Juil.", "Août", "Sept.", "Oct.", "Nov.", "Déc."]
import itertools
lisa1={}
bases2a1 ={"TEKON(IGNAME BOULLIE)":["igname","sel"],"ABLO":["farine de mais","farine de riz","sucre","sel","levure boulanger"],"DJINKOUME":["farine mais"],"COUSCOUS":["couscou","huil","sel"],"KOLIKO":["igname","huil","sel"],"TIMBANI":["haricos","sel"],"RIZ":["riz","sel"],"AMANDA(ALLOCO)":["bananes plantain","huil","sel"],"AYIMOLOU":["haricot","riz","potasse"],"SPAGHETTI":["spaghetti","sel"]}
proteines2a1={"RIEN ":[""],"AKPALAN(POISSON FUME)":["AKPALAN(POISSON FUME)"],"DEUEVI(PETIT POISSON)":["DEUEVI(PETIT POISSON)"],"APKALAN KANAMI(POISSON FRIT)":["APKALAN KANAMI(POISSON FRIT)"],"POULET":["VIANDE DE POULET"],"BOEUF":["VIANDE DE BOEUF"],"MOUTON":["VIANDE DE MOUTON"],"AKPAME(PEAU DE BOEUF)":["AKPAME(PEAU DE BOEUF)"],"AGLAN(CRABE)":["AGLAN(CRABE)"],"CREVETTE":["CREVETTE"]}
sauces2a1={"TOMATE":["TOMATE FRAIS","TOMATE CONCENTRE","HUIL VEGETAL","OIGNON","CUBE","SEL","AIL","PIMENT FRAIS","PIMENT EN POUDRE","POTASE",],}
basesa1 ={"FOUFOU IGNAME":["igname","sel"],"FOUFOU PLANTAIN":["bananas plantains","sel"],"AKOUME(PATE MAIS)":["Farine de mais"],"EMAKUME(PATE MAIS FERMENTE)":["Farine de mais","pate de mais fermenter"],"Riz":["riz","sel"]}
proteinesa1={"RIEN ":[""],"AKPALAN(POISSON FUME)":["AKPALAN(POISSON FUME)"],"DEUEVI(PETIT POISSON)":["DEUEVI(PETIT POISSON)"],"APKALAN KANAMI(POISSON FRIT)":["APKALAN KANAMI(POISSON FRIT)"],"POULET":["VIANDE DE POULET"],"BOEUF":["VIANDE DE BOEUF"],"MOUTON":["VIANDE DE MOUTON"],"AKPAME(PEAU DE BOEUF)":["AKPAME(PEAU DE BOEUF)"],"AGLAN(CRABE)":["AGLAN(CRABE)"],"CREVETTE":["CREVETTE"]}
saucesa1={"GBOMA":["oignon","gingembre"," ail","Tomate frais","piment frais","tomate concentre","huil rouge","sel","feuille de gboma","cube"],"TOMATE":["TOMATE FRAIS","TOMATE CONCENTRE","HUIL VEGETAL","OIGNON","CUBE","SEL","AIL","PIMENT FRAIS","PIMENT EN POUDRE","POTASE",],"GOUSSI":["sel","oignon","Graine de courge","tomate frais","piment frais","Tomate concentre","cube"],"ADEME":["feuilles ademe","gingembre","oignon","piment frais","huile rouge","sel","potasse","poisson fermente","cube"],"FETRI(GOMBO)":["gombo","tomate frais","oignon","piment frais","sel","gingembre","cube"],"KODORO":["oignon","gingembre","ail","piment frais","sel"," Afiti","Feuille de baobab","cube"],"GNATOU":["Feuille de gnatou","Huil rouge","pate d´arachide","piment frais","oignon","cube","sel","afiti","ail"],"ARACHIDE":["oignon","ail","gingembre","pate d´arachide","tomate frais", "piment frais","sel","tomate concentre","cube"],"CHOU":["TOMATE FRAIS","TOMATE CONCENTRE","HUIL VEGETAL","OIGNON","CUBE","SEL","AIL","PIMENT FRAIS","PIMENT EN POUDRE","POTASE", "choux"],"FETRI POUPOU(GONBO SEC)":["gombo sec","tomate frais","oignon","piment frais","piment en poudre","sel","gingembre","cube"],"DEKOU(GRAINE)":["gingembre","oignon","ail","Sel","tomate frais","oignon","piment frais","Noi de palme","cube"],"EBESSESSI":["piment frais","oignon","tomate","sel","gingembre","cube"],}
dica1={
    "DEGUE":["lait","couscous","sucre","glace","arachide"],"TAPIOCA ZOGBON":["tapioca","sel","sucre","lait en poudre"],"ATTIEKE POISSON":["poisson frais","attieke","oignon","ail","piment frai","huile d´arachide","sel"],"SPAGHETTI BLANC":["spagheti sel"],"SALADE":["Laitue","Tomate","oignon","Beterave","Carotte","Concombre","Mayonnaise","cube","sardine","oeuf","spagheti","huil","vinaigre","pain"],"HARICO HUIL ROUGE":["harico","sel","potasse","oignon","ail","huil rouge","Gari"],"HARICO HUIL ARACHIDE":["harico","sel","potasse","oignon","ail","huil d´arachide","Gari"]
}
lisa1.update(dica1)
import itertools

# --- VOS DONNÉES ---
# (Je regroupe directement les dictionnaires pour la clarté)

import itertools

import itertools

# --- 1. SOURCES DES DONNÉES ---

dict_final = {}

# A. Génération des combinaisons composées (15 bases * 12 sauces * 10 protéines = 1800)
combinaisons = list(itertools.product(basesa1.keys(), proteinesa1.keys(), saucesa1.keys()))
combinaisons2 = list(itertools.product(bases2a1.keys(), proteines2a1.keys(), sauces2a1.keys()))

# --- FONCTIONS ET BOUCLES (VOTRE STYLE) ---
lis={}
lis.update(dica1)
def afficfer(combi):
    # Cette fonction déballe la combinaison actuelle
    b, p, s = combi
    return b, p, s

def afficfer2(combi2):
    # Cette fonction déballe la combinaison du groupe 2
    b2, p2, s2 = combi2
    return b2, p2, s2

# Boucle pour le premier groupe
for combi in combinaisons:
    b, p, s = afficfer(combi)
    nom = f"{b} Sauce {s} avec {p}"
    # Fusion des listes d'ingrédients
    valeur = basesa1[b] + proteinesa1[p] + saucesa1[s]
    lis[nom] = valeur

# Boucle pour le deuxième groupe
for combi2 in combinaisons2:
    b2, p2, s2 = afficfer2(combi2)
    nom2 = f"{b2} Sauce {s2} avec {p2}"
    # Fusion des listes d'ingrédients
    valeur2 = bases2a1[b2] + proteines2a1[p2] + sauces2a1[s2]
    lis[nom2] = valeur2




RECIPES = lis

# --- LOGIQUE POUR COMPLÉTER JUSQU'À 1000 ---
# Pour éviter que l'app ne plante, on attribue une liste d'ingrédients de base
# aux variantes générées automatiquement.


MARKET_ITEMS = [
    # --- FÉCULENTS & TUBERCULES ---
    {"n": "Igname", "p": 1200, "u": "tubercule", "c": "Féculents"},
    {"n": "Farine de maïs", "p": 500, "u": "kg", "c": "Féculents"},
    {"n": "Farine de riz", "p": 800, "u": "kg", "c": "Féculents"},
    {"n": "Pâte de maïs fermentée", "p": 300, "u": "kg", "c": "Féculents"},
    {"n": "Riz", "p": 600, "u": "kg", "c": "Féculents"},
    {"n": "Couscous", "p": 1000, "u": "paquet", "c": "Féculents"},
    {"n": "Spaghetti", "p": 400, "u": "paquet", "c": "Féculents"},
    {"n": "Banane Plantain", "p": 1000, "u": "tas", "c": "Féculents"},
    {"n": "Haricot", "p": 900, "u": "kg", "c": "Féculents"},
    {"n": "Attiéké", "p": 250, "u": "boule", "c": "Féculents"},
    {"n": "Gari", "p": 450, "u": "kg", "c": "Féculents"},
    {"n": "Tapioca", "p": 700, "u": "kg", "c": "Féculents"},
    {"n": "Fonio", "p": 1200, "u": "kg", "c": "Féculents"},

    # --- VIANDES ---
    {"n": "Viande de Poulet", "p": 4500, "u": "unité", "c": "Viandes"},
    {"n": "Viande de Boeuf", "p": 3500, "u": "kg", "c": "Viandes"},
    {"n": "Viande de Mouton", "p": 4500, "u": "kg", "c": "Viandes"},
    {"n": "Peau de boeuf (Akpame)", "p": 500, "u": "tas", "c": "Viandes"},
    {"n": "Oeuf", "p": 100, "u": "unité", "c": "Viandes"},
    {"n": "Abats de Boeuf", "p": 2000, "u": "kg", "c": "Viandes"},

    # --- POISSONS & CRUSTACÉS ---
    {"n": "Poisson Capitaine", "p": 4000, "u": "kg", "c": "Poissons"},
    {"n": "Poisson fumé (Akpalan)", "p": 500, "u": "unité", "c": "Poissons"},
    {"n": "Petit poisson (Deuevi)", "p": 200, "u": "tas", "c": "Poissons"},
    {"n": "Poisson frit (Kanami)", "p": 600, "u": "unité", "c": "Poissons"},
    {"n": "Crabe (Aglan)", "p": 1500, "u": "tas", "c": "Poissons"},
    {"n": "Crevettes fraîches", "p": 3000, "u": "kg", "c": "Poissons"},
    {"n": "Crevettes séchées", "p": 500, "u": "verre", "c": "Poissons"},
    {"n": "Sardine en boite", "p": 600, "u": "boite", "c": "Poissons"},

    # --- LÉGUMES & FEUILLES ---
    {"n": "Tomate Fraiche", "p": 500, "u": "kg", "c": "Légumes"},
    {"n": "Oignon Galmi", "p": 450, "u": "kg", "c": "Légumes"},
    {"n": "Gombo frais (Fétri)", "p": 300, "u": "tas", "c": "Légumes"},
    {"n": "Gombo sec", "p": 400, "u": "tas", "c": "Légumes"},
    {"n": "Chou", "p": 500, "u": "unité", "c": "Légumes"},
    {"n": "Carotte", "p": 200, "u": "tas", "c": "Légumes"},
    {"n": "Concombre", "p": 200, "u": "unité", "c": "Légumes"},
    {"n": "Laitue", "p": 500, "u": "pied", "c": "Légumes"},
    {"n": "Beterave", "p": 300, "u": "tas", "c": "Légumes"},
    {"n": "Feuille de Gboma", "p": 200, "u": "attache", "c": "Légumes"},
    {"n": "Feuille d'Adémé", "p": 200, "u": "attache", "c": "Légumes"},
    {"n": "Feuille de Gnatou", "p": 200, "u": "attache", "c": "Légumes"},
    {"n": "Feuille de Baobab", "p": 200, "u": "attache", "c": "Légumes"},

    # --- ÉPICERIE & HUILES ---
    {"n": "Huile Végétale", "p": 1200, "u": "L", "c": "Épicerie"},
    {"n": "Huile de Palme", "p": 1100, "u": "L", "c": "Épicerie"},
    {"n": "Pâte d'Arachide", "p": 500, "u": "pot", "c": "Épicerie"},
    {"n": "Graine de courge (Goussi)", "p": 1000, "u": "bol", "c": "Épicerie"},
    {"n": "Tomate Concentrée", "p": 150, "u": "boite", "c": "Épicerie"},
    {"n": "Sucre", "p": 800, "u": "kg", "c": "Épicerie"},
    {"n": "Lait liquide", "p": 2000, "u": "boite", "c": "Épicerie"},
    {"n": "Lait en poudre", "p": 150, "u": "sachet", "c": "Épicerie"},
    {"n": "Levure boulanger", "p": 150, "u": "sachet", "c": "Épicerie"},
    {"n": "Mayonnaise", "p": 1500, "u": "bocal", "c": "Épicerie"},
    {"n": "Vinaigre", "p": 600, "u": "bouteille", "c": "Épicerie"},
    {"n": "Pain Baguette", "p": 150, "u": "unité", "c": "Épicerie"},

    # --- ÉPICES & ASSAISONNEMENTS ---
    {"n": "Ail", "p": 100, "u": "tas", "c": "Épices"},
    {"n": "Gingembre", "p": 100, "u": "tas", "c": "Épices"},
    {"n": "Piment frais", "p": 200, "u": "tas", "c": "Épices"},
    {"n": "Piment en poudre", "p": 100, "u": "sachet", "c": "Épices"},
    {"n": "Sel Iodé", "p": 250, "u": "sachet", "c": "Épices"},
    {"n": "Cube bouillon", "p": 25, "u": "unité", "c": "Épices"},
    {"n": "Potasse", "p": 50, "u": "unité", "c": "Épices"},
    {"n": "Afiti (Moutarde locale)", "p": 100, "u": "boule", "c": "Épices"},
    {"n": "Poivre noir", "p": 100, "u": "sachet", "c": "Épices"},
]
# --- BASES DE DONNÉES (Coût des ingrédients par personne) ---
import itertools
#-------------------
import itertools
import math

import itertools
import math

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
print(PLATS_FAMILLE)
print(PLATS_PETIT_COMITE)

# État de l'application
state = {"plats_selectionnes": {}, "planning_genere": []}


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


def main(page: ft.Page):
    page.title = "Gestionnaire de Budget Cuisine"
    page.scroll = "auto"
    page.theme_mode = ft.ThemeMode.LIGHT
    test = 21

    # --- COMPOSANTS DE SAISIE ---

    # Configuration des champs avec une meilleure UX
    # --------------------------------------------

    # 1. Champs de Budget (avec suffixe et clavier monétaire)
    budg_total = ft.TextField(
        label="Budget Total",
        value="50000",
        suffix="FCFA",
        expand=1,
        border_radius=12,
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_icon=ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED,
        content_padding=10
    )

    daily_limit = ft.TextField(
        label="Limite/Jour",
        value="8000",
        suffix="FCFA",
        expand=1,
        border_radius=12,
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_icon=ft.Icons.SPEED_OUTLINED,
        content_padding=10
    )

    # 2. Champs de Configuration (avec icônes parlantes)
    guests_input = ft.TextField(
        label="Pers.",
        value="4",
        expand=1,
        border_radius=12,
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_icon=ft.Icons.PEOPLE_ALT_OUTLINED,
        text_align=ft.TextAlign.CENTER,
    )

    days_input = ft.TextField(
        label="Jours",
        value="7",
        expand=1,
        border_radius=12,
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_icon=ft.Icons.CALENDAR_MONTH_OUTLINED,
        text_align=ft.TextAlign.CENTER,
    )

    meals_input = ft.TextField(
        label="Repas / Jour",
        value="2",
        expand=1,
        border_radius=12,
        keyboard_type=ft.KeyboardType.NUMBER,
        prefix_icon=ft.Icons.RESTAURANT_OUTLINED,
        text_align=ft.TextAlign.CENTER,
    )

    # --- ASTUCE UX : Groupement visuel ---
    # Pour que ce soit propre sur Android, on les groupe dans des colonnes et des lignes
    config_section = ft.Container(
        padding=10,
        content=ft.Column([
            ft.Row([guests_input, days_input, meals_input], spacing=10),
            ft.Row([budg_total, daily_limit], spacing=10),
        ], spacing=10)
    )

    search_results = ft.Column(spacing=0)
    chips_row = ft.Row(wrap=True, spacing=5)
    result_display = ft.Column(spacing=10)

    def go_to_signup(e=None):
        """Affiche le formulaire d'inscription avec UX optimisée"""
        page.clean()
        CP = "#5D8A66"  # Couleur principale

        # --- ÉLÉMENTS DU FORMULAIRE ---
        nom_in = ft.TextField(
            label="Nom complet", border_radius=12,
            prefix_icon=ft.Icons.PERSON_OUTLINE, border_color=CP
        )
        email_in = ft.TextField(
            label="Email", border_radius=12,
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            keyboard_type=ft.KeyboardType.EMAIL,
            border_color=CP
        )
        # Champ téléphone simplifié pour éviter le bug de suppression
        tel_in = ft.TextField(
            label="Téléphone",
            border_radius=12,
            prefix_icon=ft.Icons.PHONE_ANDROID_OUTLINED,
            keyboard_type=ft.KeyboardType.PHONE,
            border_color=CP,
            max_length=8
        )

        ville_in = ft.TextField(label="Ville", border_radius=12, expand=True, border_color=CP)
        quartier_in = ft.TextField(label="Quartier", border_radius=12, expand=True, border_color=CP)

        pass_in = ft.TextField(
            label="Mot de passe (min. 6 caractères)",
            password=True, can_reveal_password=True,
            border_radius=12, prefix_icon=ft.Icons.LOCK_OUTLINE,
            border_color=CP
        )
        err_msg = ft.Text("", color="red", size=12, weight="w500")

        # --- LOGIQUE D'INSCRIPTION ---
        def register(e):
            # Vérification si les champs sont vides
            if not all([nom_in.value, email_in.value, pass_in.value, tel_in.value]):
                err_msg.value = "Veuillez remplir tous les champs obligatoires."
                page.update()
                return

            # Nettoyage du numéro (on ne garde que les chiffres pour la base de données)
            digits_only = "".join(filter(str.isdigit, tel_in.value))

            if len(digits_only) < 8:
                err_msg.value = "Veuillez entrer un numéro valide (8 chiffres min)."
                page.update()
                return

            if len(pass_in.value) < 6:
                err_msg.value = "Le mot de passe doit faire 6 caractères."
                page.update()
                return

            # Feedback visuel : chargement
            btn_reg.disabled = True
            btn_reg.content = ft.ProgressRing(width=20, height=20, color="white", stroke_width=2)
            page.update()

            try:
                # Création Firebase Auth
                user = auth.create_user_with_email_and_password(email_in.value, pass_in.value)

                # Préparation des données
                user_data = {
                    "nom": nom_in.value,
                    "email": email_in.value,
                    "tel": digits_only,
                    "ville": ville_in.value,
                    "quartier": quartier_in.value,
                    "localId": user['localId']
                }

                # Enregistrement Database
                db.child("users").child(user['localId']).set(user_data)

                # Sauvegarde session locale
                import json
                with open("session_utilisateur.txt", "w", encoding="utf-8") as f:
                    json.dump(user_data, f, ensure_ascii=False)

                # Redirection vers l'accueil
                render_home()

            except Exception as error:
                print(f"Erreur inscription: {error}")
                err_msg.value = "Erreur: Email déjà utilisé ou problème réseau."
                btn_reg.disabled = False
                btn_reg.content = ft.Text("CRÉER MON COMPTE", weight="bold")
                page.update()

        # --- BOUTON PRINCIPAL ---
        btn_reg = ft.ElevatedButton(
            content=ft.Text("CRÉER MON COMPTE", weight="bold"),
            bgcolor=CP, color="white",
            height=55, width=400,
            on_click=register,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
        )

        # --- MISE EN PAGE FINALE ---
        # On met tout dans une liste propre
        formulaire = ft.Column(
            [
                ft.Image(src="Sans titre-5.png", height=80, fit="contain"),
                ft.Text("Rejoignez Cliexe", size=24, weight="bold", color=CP),
                ft.Divider(height=10, color="transparent"),
                nom_in,
                email_in,
                tel_in,
                ft.Row([ville_in, quartier_in], spacing=10),
                pass_in,
                err_msg,
                ft.Container(height=10),
                btn_reg,
                ft.TextButton(
                    "Déjà un compte ? Connexion",
                    on_click=lambda _: go_to_login()
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE
        )

        page.add(ft.Container(padding=20, content=formulaire))
        page.update()

    def go_to_login(e=None):
        """Affiche le formulaire de connexion avec UX optimisée"""
        page.clean()
        CP = "#5D8A66"  # Ta couleur verte Cliexe

        # --- ÉLÉMENTS DE SAISIE ---
        email_log = ft.TextField(
            label="Email",
            border_radius=12,
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            keyboard_type=ft.KeyboardType.EMAIL,
            border_color=CP,
            on_submit=lambda _: pass_log.focus()  # Passe au champ suivant avec 'Entrée'
        )
        pass_log = ft.TextField(
            label="Mot de passe",
            password=True,
            can_reveal_password=True,
            border_radius=12,
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            border_color=CP,
            on_submit=lambda e: login(e)
        )
        err_log = ft.Text("", color="red600", weight="w500", size=13)

        # --- LOGIQUE DE CONNEXION ---
        def login(e):
            # Désactiver le bouton et montrer le chargement
            btn_login.disabled = True
            btn_login.content = ft.ProgressRing(width=20, height=20, color="white", stroke_width=2)
            page.update()

            try:
                # 1. Authentification Firebase
                user = auth.sign_in_with_email_and_password(email_log.value, pass_log.value)

                # 2. Récupération & Session
                info = db.child("users").child(user['localId']).get().val()
                if info:
                    data = {k: info.get(k) for k in ["nom", "email", "tel", "ville", "quartier"]}
                    data["localId"] = user['localId']
                    with open("session_utilisateur.txt", "w", encoding="utf-8") as f:
                        json.dump(data, f, indent=4)

                # 3. Redirection intelligente
                conn = sqlite3.connect("repas_db.sqlite")
                count = conn.execute("SELECT COUNT(*) FROM planning").fetchone()[0]
                conn.close()

                render_final_view() if count > 0 else render_home()

            except Exception as ex:
                err_log.value = "Identifiants invalides ou problème réseau."
                btn_login.disabled = False
                btn_login.content = ft.Text("SE CONNECTER", weight="bold")
                page.update()

        # --- BOUTON PRINCIPAL ---
        btn_login = ft.ElevatedButton(
            content=ft.Text("SE CONNECTER", weight="bold"),
            bgcolor=CP,
            color="white",
            height=55,
            width=320,
            on_click=login,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
        )

        # --- MISE EN PAGE ---
        page.add(
            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=ft.Column([
                    # Section Logo
                    ft.Container(
                        content=ft.Column([
                            ft.Image(src="logo.png", height=90, fit="contain"),  #
                            ft.Text("Bon retour parmi nous !", size=14, color="grey600"),
                        ], alignment=ft.Alignment(0,0)),
                        margin=ft.margin.only(bottom=20)
                    ),

                    # Formulaire
                    email_log,
                    pass_log,
                    err_log,

                    ft.Container(height=10),
                    btn_login,

                    ft.TextButton(
                        "Nouveau sur Cliexe ? Créer un compte",
                        on_click=lambda _: go_to_signup(),
                        style=ft.ButtonStyle(color=CP)
                    )
                ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    tight=True
                )
            )
        )
        page.update()
        try:
            requests.get('https://www.google.com', timeout=5)



        except:
            print("pas de connexion")

            def close_dlg(e):
                dlg.open = False
                page.update()

            def confirm_action(e):
                dlg.open = False
                page.update()
                try:
                    conn = sqlite3.connect("repas_db.sqlite")
                    c = conn.cursor()
                    # On vérifie si la table planning contient au moins une ligne
                    c.execute("SELECT COUNT(*) FROM planning")
                    count = c.fetchone()[0]
                    conn.close()
                    render_final_view()
                except:
                    render_home()
                # Appelle votre fonction de redirection

            # Palette de couleurs conseillée
            C_OFFLINE = "#546E7A"  # Gris-bleu pour le mode hors-ligne
            CP = "#5D8A66"  # Vert principal pour l'action positive

            dlg = ft.AlertDialog(
                modal=True,
                shape=ft.RoundedRectangleBorder(radius=25),
                content_padding=ft.padding.all(25),
                content=ft.Column([
                    # Illustration visuelle
                    ft.Container(
                        content=ft.Icon(ft.Icons.SIGNAL_WIFI_OFF_ROUNDED, color=ft.Colors.ORANGE_700, size=50),
                        bgcolor=ft.Colors.ORANGE_50,
                        padding=20,
                        shape=ft.BoxShape.CIRCLE,
                    ),
                    # Titre et message
                    ft.Column([
                        ft.Text("Oups ! Pas d'internet", weight="bold", size=20, text_align="center"),
                        ft.Text(
                            "Nous ne parvenons pas à joindre nos serveurs. Vous pouvez continuer à consulter vos données locales en mode hors-ligne.",
                            size=14, color="grey700", text_align="center"
                        ),
                    ], horizontal_alignment="center", spacing=10),

                    ft.Divider(height=10, color="transparent"),

                    # Action principale (Hors-ligne)
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.Icons.CLOUDY_SNOWING, size=20),
                            ft.Text("CONTINUER HORS-LIGNE", weight="bold"),
                        ], alignment="center"),
                        on_click=confirm_action,
                        bgcolor=C_OFFLINE,
                        color="white",
                        height=50,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                    ),

                    # Action secondaire (Réessayer)
                    ft.TextButton(
                        "Réessayer la connexion",
                        on_click=lambda _: (setattr(dlg, "open", False), page.update()),  # Ou votre fonction close_dlg
                        style=ft.ButtonStyle(color=CP)
                    )

                ], tight=True, spacing=15, horizontal_alignment="center"),
            )

            page.overlay.append(dlg)
            dlg.open = True
            page.update()

        page.update()

    def no_compte(ns):
        # Palette de couleurs (assurez-vous que CP et CERR sont définis)
        CP = "#5D8A66"

        def go_to_auth(e):
            dlg.open = False
            page.update()
            go_to_login()  # Appelle votre fonction de connexion existante

        dlg = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=25),
            content_padding=ft.padding.all(25),
            content=ft.Column([
                # Icône stylisée
                ft.Container(
                    content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE_OUTLINED, color=CP, size=50),
                    bgcolor=ft.Colors.with_opacity(0.1, CP),
                    padding=20,
                    shape=ft.BoxShape.CIRCLE,
                ),
                # Texte informatif
                ft.Column([
                    ft.Text("Connexion requise", weight="bold", size=20, text_align="center"),
                    ft.Text(ns, size=14, color="grey700", text_align="center"),
                ], horizontal_alignment="center", spacing=5),

                ft.Divider(height=10, color="transparent"),

                # Action principale : Se connecter
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.LOGIN_ROUNDED, size=20),
                        ft.Text("SE CONNECTER", weight="bold"),
                    ], alignment="center"),
                    on_click=go_to_auth,
                    bgcolor=CP,
                    color="white",
                    height=50,
                    width=250,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                ),

                # Action secondaire : Fermer
                ft.TextButton(
                    "Plus tard",
                    on_click=lambda _: (setattr(dlg, "open", False), page.update()),
                    style=ft.ButtonStyle(color="grey600")
                )

            ], tight=True, spacing=15, horizontal_alignment="center"),
        )

        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def no_connexion():
        # On ne fait pas forcément un page.clean() pour garder le contexte visuel en fond

        def retry(e):
            dlg.open = False
            page.update()
            # On tente de recharger la vue précédente (ici le marché par exemple)
            render_market(page, render_final_view)

        dlg = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=25),
            content_padding=ft.padding.all(30),
            content=ft.Column([
                # Animation visuelle simple avec une icône entourée
                ft.Container(
                    content=ft.Icon(ft.Icons.WIFI_OFF_ROUNDED, color=ft.Colors.AMBER_700, size=50),
                    bgcolor=ft.Colors.AMBER_50,
                    padding=20,
                    border_radius=40,
                ),
                ft.Text(
                    "Connexion perdue",
                    weight="bold",
                    size=22,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.BLUE_GREY_800
                ),
                ft.Text(
                    "Nous n'arrivons pas à joindre nos serveurs. Vérifiez votre Wi-Fi ou vos données mobiles.",
                    size=14,
                    color=ft.Colors.BLUE_GREY_500,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Divider(height=10, color="transparent"),
                # Bouton d'action principal
                ft.ElevatedButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.REFRESH_ROUNDED, size=20),
                        ft.Text("RÉESSAYER MAINTENANT", weight="bold"),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    on_click=retry,
                    bgcolor=CP,
                    color="white",
                    height=50,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                ),
                # Option pour fermer simplement
                ft.TextButton(
                    "Retour à l'accueil",
                    on_click=lambda _: (setattr(dlg, "open", False), render_final_view()),
                    style=ft.ButtonStyle(color=ft.Colors.BLUE_GREY_400)
                )
            ], tight=True, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        )

        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def cv():
        try:
            # Vérification rapide de la connexion
            requests.get('https://www.google.com', timeout=5)

            if os.path.exists("session_utilisateur.txt"):

                def confirm_logout(e):
                    try:
                        if os.path.exists("session_utilisateur.txt"):
                            os.remove("session_utilisateur.txt")  # Suppression effective
                        dlg.open = False
                        page.update()
                        go_to_login()  # Retour à la page de connexion
                    except Exception as ex:
                        print(f"Erreur lors de la suppression : {ex}")

                def close_dlg(e):
                    dlg.open = False
                    page.update()

                # Dialogue de déconnexion stylisé
                dlg = ft.AlertDialog(
                    modal=True,
                    title=ft.Row([
                        ft.Icon(ft.Icons.LOGOUT_ROUNDED, color=ft.Colors.RED_400),
                        ft.Text(" Déconnexion")
                    ]),
                    content=ft.Text(
                        "Êtes-vous sûr de vouloir vous déconnecter ? Vous devrez saisir vos identifiants à nouveau.",
                        size=14,
                        color=ft.Colors.BLUE_GREY_700
                    ),
                    actions=[
                        ft.TextButton(
                            "ANNULER",
                            on_click=close_dlg,
                            style=ft.ButtonStyle(color=ft.Colors.BLUE_GREY_400)
                        ),
                        ft.ElevatedButton(
                            "OUI, DÉCONNEXION",
                            on_click=confirm_logout,
                            bgcolor=ft.Colors.RED_50,
                            color=ft.Colors.RED_600,
                            style=ft.ButtonStyle(
                                elevation=0,
                                shape=ft.RoundedRectangleBorder(radius=10)
                            )
                        ),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                    shape=ft.RoundedRectangleBorder(radius=15),
                )

                page.overlay.append(dlg)
                dlg.open = True
                page.update()

        except requests.RequestException:
            # On appelle la fonction de connexion optimisée qu'on a créée juste avant
            no_connexion()

    # Note : Assurez-vous que 'db' et 'auth' sont accessibles (importés ou globaux)


    # --- CONFIGURATION GLOBALE ---
    C_MARKET = "#2E7D32"
    SESSION_FILE = "session_utilisateur.txt"
    CONFIG_FILE = "config.json"


    # --- CONFIGURATION ET THEME ---
    THEME_COLOR = "#2E7D32"  # Vert Forêt
    ACCENT_COLOR = "#E8F5E9"  # Vert très clair
    TEXT_PRIMARY = "#1B5E20"

    class MarketManager:
        """Classe pour gérer l'état du panier de manière professionnelle."""

        def __init__(self):
            self.cart = {}

        def update(self, item_name, qty, price):
            if qty > 0:
                self.cart[item_name] = {"qty": qty, "price": price, "total": qty * price}
            elif item_name in self.cart:
                del self.cart[item_name]

        def get_total(self):
            return sum(item["total"] for item in self.cart.values())

        def get_count(self):
            return len(self.cart)

    def render_market(page, render_final_view):
        # Chemin vers le fichier de session créé à l'inscription/connexion
        SESSION_FILE = "session_utilisateur.txt"

        if os.path.exists(SESSION_FILE):
            try:
                requests.get('https://www.google.com', timeout=5)
                page.clean()

                # ================= ÉTAT =================
                cart_items = {}
                C_MARKET = "#2E7D32"
                total_view = ft.Text("0 FCFA", size=24, weight="bold", color=C_MARKET)
                market_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=12)

                # ================= UTIL =================
                def notify(message, color="orange"):
                    page.snack_bar = ft.SnackBar(content=ft.Text(message), bgcolor=color)
                    page.snack_bar.open = True
                    page.update()

                def get_user_session():
                    """Récupère les infos de l'utilisateur stockées localement"""
                    try:
                        with open(SESSION_FILE, "r", encoding="utf-8") as f:
                            # On charge le dictionnaire stocké par json.dumps
                            return json.loads(f.read())
                    except:
                        return {"nom": "Client Inconnu", "tel": "Non spécifié"}

                # ============ LOGIQUE PANIER ============
                def update_cart(name, q, p):
                    if q > 0:
                        cart_items[name] = {"qty": q, "price": p, "total": q * p}
                    elif name in cart_items:
                        del cart_items[name]

                    total = sum(item["total"] for item in cart_items.values())
                    total_view.value = f"{total:,} FCFA".replace(",", " ")
                    page.update()

                # ============ NAVIGATION ============
                def go_market():
                    render_market(page, render_final_view)

                def go_cart():
                    if not cart_items:
                        notify("Votre panier est vide 🧺")
                        return
                    render_cart()

                def go_confirmation():
                    if not cart_items:
                        notify("Ajoutez au moins un produit avant de commander")
                        return

                    # ENVOI VERS FIREBASE AVANT D'AFFICHER LE DIALOGUE
                    envoi_reussi = envoyer_commande_firebase()
                    if envoi_reussi:
                        render_confirmation_dialog()

                # ============ FIREBASE SEND ============
                def envoyer_commande_firebase():
                    try:
                        user_info = get_user_session()

                        # Construction de l'objet de commande final
                        commande_finale = {
                            "info": user_info.get("nom"),
                            "telephone": user_info.get("tel"),
                            "ville": user_info.get("ville", "Non précisée"),
                            "quartier": user_info.get("quartier", "Non précisé"),
                            "type": "MARCHÉ",
                            "panier": cart_items,  # Contient noms, quantités et prix
                            "total_paye": total_view.value,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "statut": "En attente"
                        }

                        # Envoi vers le noeud 'commandes' de Firebase
                        db.child("commandes").push(commande_finale)
                        return True
                    except Exception as e:
                        notify(f"Erreur d'envoi : {str(e)}", color="red")
                        return False

                # ============ PAGE PANIER ============
                def update_cart_and_refresh():
                    # Recalcule le total global
                    nouveau_total = sum(item['total'] for item in cart_items.values())
                    total_view.value = str(nouveau_total)
                    # Relance le rendu pour voir les changements
                    render_cart()

                def increase_qty(name):
                    # Augmente la quantité et met à jour le total de la ligne
                    prix_unitaire = cart_items[name]['total'] // cart_items[name]['qty']
                    cart_items[name]['qty'] += 1
                    cart_items[name]['total'] = cart_items[name]['qty'] * prix_unitaire
                    update_cart_and_refresh()

                def decrease_qty(name):
                    # Diminue la quantité ou supprime si on tombe à 0
                    if cart_items[name]['qty'] > 1:
                        prix_unitaire = cart_items[name]['total'] // cart_items[name]['qty']
                        cart_items[name]['qty'] -= 1
                        cart_items[name]['total'] = cart_items[name]['qty'] * prix_unitaire
                    else:
                        del cart_items[name]
                    update_cart_and_refresh()

                def remove_from_cart(name):
                    # Supprime l'article directement
                    if name in cart_items:
                        del cart_items[name]
                    update_cart_and_refresh()
                def render_cart():
                    page.clean()
                    page.bgcolor = "#F8F9FA" # Fond gris très clair

                    items_ui = ft.Column(spacing=15, scroll=ft.ScrollMode.ADAPTIVE, expand=True)

                    # Si le panier est vide
                    if not cart_items:
                        items_ui.controls.append(
                            ft.Container(
                                content=ft.Column([
                                    ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED, size=50, color="grey"),
                                    ft.Text("Votre panier est vide", color="grey")
                                ], horizontal_alignment="center"),
                                margin=ft.margin.only(top=100)
                            )
                        )
                    else:
                        for name, data in cart_items.items():
                            items_ui.controls.append(
                                ft.Container(
                                    bgcolor="white",
                                    padding=15,
                                    border_radius=15,
                                    shadow=ft.BoxShadow(blur_radius=5, color=ft.Colors.with_opacity(0.05, "black")),
                                    content=ft.Column([
                                        ft.Row([
                                            ft.Text(name, weight="bold", size=16, expand=True),
                                            ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_color="red", icon_size=20,
                                                          on_click=lambda e, n=name: remove_from_cart(n)),
                                        ]),
                                        ft.Row([
                                            # Contrôles de quantité (+ / -)
                                            ft.Container(
                                                bgcolor="#F0F0F0",
                                                border_radius=10,
                                                content=ft.Row([
                                                    ft.IconButton(ft.Icons.REMOVE, icon_size=16, on_click=lambda e: decrease_qty(name)),
                                                    ft.Text(str(data['qty']), weight="bold"),
                                                    ft.IconButton(ft.Icons.ADD, icon_size=16, on_click=lambda e: increase_qty(name)),
                                                ], spacing=0)
                                            ),
                                            ft.Text(f"{data['total']} F", weight="bold", size=16, color=C_MARKET),
                                        ], alignment="spaceBetween")
                                    ])
                                )
                            )

                    page.add(
                        # App Bar Custom
                        ft.Container(
                            padding=ft.padding.only(top=40, left=10, right=10, bottom=10),
                            content=ft.Row([
                                ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW, icon_size=20, on_click=lambda e: go_market()),
                                ft.Text("Mon Panier", size=20, weight="bold", expand=True),
                                ft.Text(f"{len(cart_items)} articles", color="grey")
                            ])
                        ),

                        # Liste des articles
                        ft.Container(padding=20, expand=True, content=items_ui),

                        # Panneau de validation (Bottom Bar)
                        ft.Container(
                            padding=20,
                            bgcolor="white",
                            border_radius=ft.border_radius.only(top_left=30, top_right=30),
                            shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.with_opacity(0.1, "black")),
                            content=ft.Column([
                                ft.Row([
                                    ft.Text("Total à payer", size=16, color="grey"),
                                    ft.Text(f"{total_view.value} FCFA", weight="bold", size=22, color=C_MARKET)
                                ], alignment="spaceBetween"),
                                ft.Container(height=10),
                                ft.ElevatedButton(
                                    content=ft.Row([
                                        ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE),
                                        ft.Text("VALIDER LA COMMANDE", weight="bold", size=16)
                                    ], alignment="center"),
                                    bgcolor=C_MARKET,
                                    color="white",
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15)),
                                    height=55,
                                    width=float("inf"), # Prend toute la largeur
                                    on_click=lambda e: go_confirmation()
                                )
                            ], tight=True)
                        )
                    )
                    page.update()

                # ============ DIALOGUE CONFIRMATION ============
                def render_confirmation_dialog():
                    dlg = ft.AlertDialog(
                        modal=True,
                        title=ft.Text("Commande envoyée !", weight="bold", text_align="center"),
                        content=ft.Column([
                            ft.Icon(ft.Icons.PHONE_IN_TALK_ROUNDED, color=C_MARKET, size=60),
                            ft.Text("Notre équipe vous contacte dans 5 minutes.", text_align="center"),
                        ], tight=True, spacing=20, horizontal_alignment="center"),
                        actions=[
                            ft.ElevatedButton(
                                "D'ACCORD",
                                on_click=lambda _: (setattr(dlg, "open", False), render_final_view()),
                                bgcolor=C_MARKET, color="white"
                            )
                        ],
                        actions_alignment="center",
                        shape=ft.RoundedRectangleBorder(radius=20),
                    )
                    page.overlay.append(dlg)
                    dlg.open = True
                    page.update()

                # ============ RECHERCHE & AFFICHAGE ============
                def filter_items(e):
                    page.update()
                    page.update()
                    query = search_field.value.lower() if search_field.value else ""
                    market_list.controls.clear()
                    for item in MARKET_ITEMS:
                        if query in item["n"].lower():
                            market_list.controls.append(MarketTile(item, update_cart))
                    page.update()

                search_field = ft.TextField(
                    hint_text="Rechercher (ex: Oignon)...",
                    prefix_icon=ft.Icons.SEARCH, bgcolor="white",
                    on_change=filter_items,
                )

                filter_items(None)

                page.add(
                    ft.Container(
                        padding=20, bgcolor=C_MARKET,
                        content=ft.Row([
                            ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white",
                                          on_click=lambda e: render_final_view()),
                            ft.Text("LE MARCHÉ", color="white", size=20, weight="bold"),
                            ft.IconButton(ft.Icons.SHOPPING_BASKET, icon_color="white", on_click=lambda e: go_cart())
                        ], alignment="spaceBetween")
                    ),
                    ft.Container(padding=20, content=search_field),
                    ft.Container(expand=True, padding=20, content=market_list),
                    ft.Container(
                        padding=20, bgcolor="white",
                        content=ft.Row([
                            ft.Column([ft.Text("TOTAL ESTIMÉ", size=10), total_view], expand=True),
                            ft.ElevatedButton("COMMANDE", bgcolor=C_MARKET, color="white",
                                              on_click=lambda e: go_cart())
                        ])
                    )
                )
                page.update()

            except requests.RequestException:
                no_connexion()
        else:
            no_compte("Connectez-vous pour commander")
    def render_loan_page(page: ft.Page, on_back_callback):
        SESSION_FILE = "session_utilisateur.txt"

        def get_user_session():
            """Récupère les infos de l'utilisateur stockées localement"""
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    return json.loads(f.read())
            except:
                return {"nom": "Client Inconnu", "tel": "Non spécifié", "ville": "N/A", "quartier": "N/A"}

        user_info = get_user_session()
        nom_client = user_info.get("nom", "Client")

        # --- LOGIQUE DE POINTS & SQLITE ---
        conn = sqlite3.connect('fidelite.db')
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO clients (nom, points) VALUES (?, 0)', (nom_client,))
        conn.commit()

        cursor.execute('SELECT points FROM clients WHERE nom = ?', (nom_client,))
        resultat = cursor.fetchone()
        conn.close()

        points_actuels = resultat[0] if resultat else 0

        # --- VÉRIFICATION DU SEUIL MINIMUM (10 points) ---
        if points_actuels < 10:
            def fermer_et_retour(e):
                dialogue_refus.open = False
                page.update()
                on_back_callback()

            dialogue_refus = ft.AlertDialog(
                modal=True,
                title=ft.Text("⚠️ Fidélité insuffisante"),
                content=ft.Text(
                    f"Il vous faut au moins 10 points pour un prêt.\n"
                    f"Points actuels : {points_actuels}\n\n"
                    "Continuez vos commandes pour débloquer cette option !"
                ),
                actions=[ft.TextButton("Compris", on_click=fermer_et_retour)],
            )
            page.overlay.append(dialogue_refus)
            dialogue_refus.open = True
            page.update()
            return

        # --- CALCUL DU PLAFOND (10 pts = 5000 FCFA) ---
        plafond_max = (points_actuels // 10) * 5000
        if plafond_max > 150000: plafond_max = 150000  # Limite haute de sécurité

        # --- RENDU DE LA PAGE DE PRÊT ---
        try:
            # Vérification connexion
            requests.get('https://www.google.com', timeout=5)
            page.clean()

            PRIX_MOYEN_REPAS = 1500

            # Slider dynamique selon le plafond calculé
            amt_slider = ft.Slider(
                min=5000,
                max=plafond_max,
                divisions=max(1, (plafond_max - 5000) // 1000),
                value=min(25000, plafond_max),
                label="{value} FCFA",
                active_color=CP
            )

            duration_slider = ft.Slider(min=1, max=6, divisions=5, value=1, label="{value} mois", active_color=CP)

            monthly_txt = ft.Text("0 FCFA", size=32, weight="bold", color=CP)
            repas_info_txt = ft.Text("", color=CP, weight="bold", size=14)

            def update_simulation(e=None):
                amt = amt_slider.value
                total = amt * 1.05  # 5% de frais
                monthly = total / duration_slider.value
                nb_repas = int(amt / PRIX_MOYEN_REPAS)

                monthly_txt.value = f"{int(monthly):,} FCFA".replace(",", " ")
                repas_info_txt.value = f"Équivaut à environ {nb_repas} repas"
                page.update()

            def envoyer_demande_pret(e):
                try:
                    requests.get('https://www.google.com', timeout=5)
                    btn_submit.disabled = True
                    btn_submit.content = ft.ProgressRing(width=20, height=20, color="white")
                    page.update()

                    demande_pret = {
                        "nom": user_info.get("nom"),
                        "telephone": user_info.get("tel"),
                        "ville": user_info.get("ville"),
                        "quartier": user_info.get("quartier"),
                        "type": "DEMANDE_PRET",
                        "montant": f"{int(amt_slider.value):,} FCFA",
                        "duree": f"{int(duration_slider.value)} mois",
                        "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "statut": "En attente étude"
                    }

                    db.child("commandes").push(demande_pret)

                    dlg_pret = ft.AlertDialog(
                        modal=True,
                        title=ft.Text("Demande de prêt reçue", weight="bold", text_align=ft.TextAlign.CENTER),
                        content=ft.Column([
                            ft.Icon(ft.Icons.SUPPORT_AGENT_ROUNDED, color=CP, size=60),
                            ft.Text(
                                "Étude de votre dossier",
                                weight="bold",
                                size=16,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                "Un conseiller financier va vous appeler d'ici quelques instants pour valider votre demande de prêt alimentaire.",
                                size=14,
                                color=CT2,
                                text_align=ft.TextAlign.CENTER
                            ),
                        ], tight=True, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        actions=[
                            ft.Container(
                                content=ft.ElevatedButton(
                                    "J'ATTENDS L'APPEL DU CONSEILLER",
                                    on_click=lambda _: (setattr(dlg_pret, "open", False), on_back_callback()),
                                    bgcolor=CP,
                                    color="white",
                                    height=50,
                                ),
                                alignment=ft.alignment.Alignment(0, 0),
                                padding=ft.padding.only(bottom=10)
                            )
                        ],
                        actions_alignment=ft.MainAxisAlignment.CENTER,
                        shape=ft.RoundedRectangleBorder(radius=20),
                    )

                    page.overlay.append(dlg_pret)
                    dlg_pret.open = True
                    page.update()

                except:
                    btn_submit.disabled = False
                    btn_submit.content = ft.Text("SOUMETTRE MA DEMANDE", weight="bold")
                    page.update()

            amt_slider.on_change = update_simulation
            duration_slider.on_change = update_simulation

            btn_submit = ft.ElevatedButton(
                content=ft.Text("SOUMETTRE MA DEMANDE", weight="bold"),
                bgcolor=CP, color="white", height=55, width=400,
                on_click=envoyer_demande_pret,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
            )

            update_simulation()

            page.add(
                # Header
                ft.Container(
                    padding=ft.padding.only(top=40, left=10, right=10, bottom=10),
                    bgcolor=CP,
                    content=ft.Row([
                        ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=lambda _: on_back_callback()),
                        ft.Text("DEMANDE DE PRÊT", color="white", size=18, weight="bold")
                    ])
                ),
                # Corps
                ft.Container(
                    padding=20,
                    content=ft.Column([
                        ft.Container(
                            padding=15, bgcolor=CC, border_radius=12,
                            shadow=ft.BoxShadow(blur_radius=8, color="#00000010"),
                            content=ft.Column([
                                ft.Text("VOTRE MENSUALITÉ ESTIMÉE", size=11, color=CT2, text_align="center", width=400),
                                ft.Row([monthly_txt], alignment="center"),
                            ])
                        ),
                        ft.Divider(height=10, color="transparent"),
                        ft.Row([
                            ft.Icon(ft.Icons.STAR, color="amber", size=16),
                            ft.Text(f"Score Fidélité : {points_actuels} points", weight="bold", size=14)
                        ]),
                        # --- Bloc info correspondance ---
                        ft.Container(
                            padding=10,
                            bgcolor=ft.Colors.BLUE_GREY_50,
                            border_radius=10,
                            content=ft.Column([
                                ft.Text("💡 Règle du prêt :", size=12, weight="bold", color=CP),
                                ft.Text(
                                    "Chaque tranche de 10 points vous donne droit à 5 000 FCFA de prêt.\n"
                                    f"Avec vos {points_actuels} points, vous pouvez emprunter jusqu'à {int(plafond_max):,} FCFA.".replace(
                                        ",", " "),
                                    size=12, color=CT2
                                ),
                            ], spacing=5)
                        ),
                        ft.Divider(height=10, color="transparent"),
                        ft.Text(f"Montant maximum autorisé : {int(plafond_max):,} FCFA".replace(",", " "), color=CP,
                                size=13, weight="w500"),
                        amt_slider,

                        ft.Container(
                            padding=10, bgcolor=CA, border_radius=8,
                            content=ft.Row([ft.Icon(ft.Icons.RESTAURANT, size=18, color=CP), repas_info_txt],
                                           alignment="center")
                        ),

                        ft.Text("Durée de remboursement (mois)", weight="bold", margin=ft.margin.only(top=10)),
                        duration_slider,

                        ft.Text(
                            "Note: L'octroi définitif dépend de l'appel de validation de notre agent.",
                            size=11, color=CT2, italic=True
                        ),
                        ft.Container(height=10),
                        btn_submit
                    ], spacing=10, scroll=ft.ScrollMode.ADAPTIVE)
                )
            )
            page.update()

        except requests.RequestException:
            # Fonction no_connexion() supposée existante dans votre code global
            if 'no_connexion' in locals() or 'no_connexion' in globals():
                no_connexion()
            else:
                print("Erreur : Pas de connexion internet.")

    def render_order_page(plat_name, base_price, shipping, i, date_livraison):
        SESSION_FILE = "session_utilisateur.txt"
        if os.path.exists("session_utilisateur.txt"):
            try:
                requests.get('https://www.google.com', timeout=5)
                page.clean()

                # Récupération des ingrédients de la recette
                ingredients_recette = RECIPES.get(plat_name, ["Ingrédients de base"])
                # Par défaut, tout est inclus dans le kit
                panier_kit = list(ingredients_recette)

                total_txt = ft.Text(f"{base_price + shipping} FCFA", size=26, weight="bold", color=CP)

                def maj_prix(e, ing):
                    """Ajuste le prix si le client retire un ingrédient du kit (ex: il a déjà l'huile)"""
                    if e.control.value is False:  # Décoché
                        if ing in panier_kit:
                            panier_kit.remove(ing)
                    else:  # Recoché
                        if ing not in panier_kit:
                            panier_kit.append(ing)

                        # Calcul : Prix de base - (nombre d'ingrédients absents * prix unitaire)
                    nb_retires = len(ingredients_recette) - len(panier_kit)
                    nouveau_total = (base_price - (nb_retires * 100)) + shipping

                    total_txt.value = f"{max(nouveau_total, shipping + 500)} FCFA"
                    page.update()

                def get_user_session():
                    """Récupère les infos de l'utilisateur stockées localement"""
                    try:
                        with open(SESSION_FILE, "r", encoding="utf-8") as f:
                            # On charge le dictionnaire stocké par json.dumps
                            return json.loads(f.read())
                    except:
                        return {"nom": "Client Inconnu", "tel": "Non spécifié"}

                def envoyer_commande_kit(e):
                    try:
                        # 1. Vérification connexion
                        requests.get('https://www.google.com', timeout=5)

                        # 2. Animation visuelle immédiate
                        btn_kit.disabled = True
                        btn_kit.content = ft.ProgressRing(width=20, height=20, color="white")
                        page.update()

                        # 3. Récupération des données utilisateur et de la commande
                        user_info = get_user_session()
                        date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        # Nettoyage du prix : on garde uniquement les chiffres
                        prix_clean = "".join(filter(str.isdigit, total_txt.value))
                        prix_numerique = int(prix_clean) if prix_clean else 0

                        # 4. STRUCTURE DE LA COMMANDE FINALE (Kit Cuisine)
                        commande_finale = {
                            "info": user_info.get("nom", "Client"),
                            "telephone": user_info.get("tel", "Inconnu"),
                            "ville": user_info.get("ville", "Non précisée"),
                            "quartier": user_info.get("quartier", "Non précisé"),
                            "type": "KIT_CUISINE",
                            "nom_plat": plat_name,
                            "panier": panier_kit,  # Liste des ingrédients sélectionnés
                            "total_paye": total_txt.value,
                            "date": date_actuelle,
                            "statut": "En attente"
                        }

                        # 5. ENVOI FIREBASE
                        try:
                            db.child("commandes").push(commande_finale)
                        except Exception as ex:
                            print(f"Erreur Firebase : {ex}")

                        # 6. ENREGISTREMENT SQLITE LOCAL
                        try:
                            date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            conn = sqlite3.connect("commandes.db")
                            cursor = conn.cursor()
                            cursor.execute('''
                                    INSERT INTO commandes (date_commande, nom_plat, prix_total, ingredients)
                                    VALUES (?, ?, ?, ?)
                                ''', (date_livraison, plat_name, prix_numerique, ", ".join(panier_kit)))
                            conn.commit()
                            conn.close()
                            # 7 point fidelite
                            nom = user_info.get("nom", "Client")
                            conn = sqlite3.connect('fidelite.db')
                            cursor = conn.cursor()

                            # On vérifie si le client existe, sinon on le crée
                            cursor.execute('INSERT OR IGNORE INTO clients (nom, points) VALUES (?, 0)', (nom,))

                            # On ajoute +1 point à chaque commande
                            cursor.execute('UPDATE clients SET points = points + 1 WHERE nom = ?', (nom,))

                            # On récupère le nouveau solde
                            cursor.execute('SELECT points FROM clients WHERE nom = ?', (nom,))
                            nouveau_solde = cursor.fetchone()[0]

                            conn.commit()
                            conn.close()
                        except Exception as ex:
                            print(f"Erreur SQLite : {ex}")

                        # 7. AFFICHAGE DU DIALOGUE DE SUCCÈS
                        dlg = ft.AlertDialog(
                            modal=True,
                            title=ft.Text("Commande bien reçue !", weight="bold", text_align=ft.TextAlign.CENTER),
                            content=ft.Column([
                                ft.Icon(ft.Icons.PHONE_IN_TALK_ROUNDED, color=CP, size=60),
                                ft.Text("Restez à côté de votre téléphone.", weight="bold", size=16,
                                        text_align=ft.TextAlign.CENTER),
                                ft.Text(
                                    "Notre équipe va vous appeler d'ici 5 minutes pour confirmer la livraison de vos ingrédients.",
                                    size=14, color=CT2, text_align=ft.TextAlign.CENTER
                                ),
                            ], tight=True, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            actions=[
                                ft.Container(
                                    content=ft.ElevatedButton(
                                        "D'ACCORD, J'ATTENDS L'APPEL",
                                        on_click=lambda _: (setattr(dlg, "open", False), render_final_view()),
                                        bgcolor=CP, color="white", height=50,
                                    ),
                                    alignment=ft.Alignment(0, 0),
                                    padding=ft.padding.only(bottom=10)
                                )
                            ],
                            actions_alignment=ft.MainAxisAlignment.CENTER,
                            shape=ft.RoundedRectangleBorder(radius=20),
                        )

                        page.overlay.append(dlg)
                        dlg.open = True
                        page.update()

                    except requests.RequestException:
                        # En cas d'erreur, on réactive le bouton
                        btn_kit.disabled = False
                        btn_kit.content = ft.Text("COMMANDER LE KIT", weight="bold")
                        page.update()
                        no_connexion()

                # Liste des ingrédients avec icônes de "marché"
                liste_items = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
                for ing in ingredients_recette:
                    liste_items.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Icon(ft.Icons.INVENTORY_2_OUTLINED, color=CS, size=20),
                                ft.Column([
                                    ft.Text(ing, size=16, weight="w500"),
                                    ft.Text("Portion exacte pour la recette", size=11, color=CT2),
                                ], expand=True),
                                ft.Checkbox(value=True, fill_color=CP, on_change=lambda e, i=ing: maj_prix(e, i))
                            ]),
                            padding=12, bgcolor="#FFFFFF", border_radius=12,
                            border=ft.border.all(1, "#F0F0F0")
                        )
                    )

                btn_kit = ft.ElevatedButton(
                    content=ft.Text("COMMANDER LE KIT", weight="bold"),
                    bgcolor=CP, color="white", height=55, expand=True,
                    on_click=envoyer_commande_kit,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                )

                page.add(
                    ft.Container(
                        padding=ft.padding.only(top=50, left=20, right=20, bottom=20),
                        bgcolor=CP,
                        content=ft.Row([
                            ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white",
                                          on_click=lambda _: render_final_view()),
                            ft.Text("MON PANIER D'INGRÉDIENTS", color="white", size=18, weight="bold")
                        ])
                    ),
                    ft.Container(
                        padding=25,
                        expand=True,
                        content=ft.Column([
                            ft.Text(f"Kit : {plat_name}", size=24, weight="bold", color=CT1),
                            ft.Text("Nous livrons les ingrédients frais, dosés et prêts à cuisiner.", color=CS, size=13,
                                    italic=True),

                            ft.Divider(height=20, color="transparent"),

                            # Zone des ingrédients à livrer
                            ft.Container(height=380, content=liste_items),

                            ft.Divider(),

                            # Résumé Paiement
                            ft.Container(
                                padding=10,
                                content=ft.Row([
                                    ft.Column([
                                        ft.Text("TOTAL KIT + LIVRAISON", size=10, color=CT2, weight="bold"),
                                        total_txt
                                    ], expand=True),
                                    btn_kit
                                ])
                            )
                        ])
                    )
                )
                page.update()
            except requests.RequestException:
                no_connexion()
        else:
            no_compte("Vous devez vous connectez a un compte pour pouvoir commander")


    import asyncio
    def render_splash(page: ft.Page):

        page.clean()
        page.padding = 0

        logo = ft.Image(
            src="logo.png",
            width=140,
            height=140,
            fit="contain"
        )

        loader = ft.ProgressRing(width=28, height=28, stroke_width=3)

        card = ft.Container(
            content=ft.Column(
                [
                    logo,
                    ft.Container(height=10),
                    ft.Text("Chargement...", color="white"),
                    ft.Container(height=15),
                    loader
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=220,
            height=260,
            bgcolor=ft.Colors.with_opacity(0.15, "white"),
            border_radius=20,
            alignment=ft.Alignment(0,0),
            padding=20
        )

        splash = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(
                        expand=True,
                        gradient=ft.LinearGradient(
                            begin=ft.alignment.Alignment(-1, -1),
                            end=ft.alignment.Alignment(1, 1),
                            colors=["#0f2027", "#203a43", "#2c5364"]
                        )
                    ),
                    ft.Container(
                        content=card,
                        alignment=ft.Alignment(0,0),
                        expand=True
                    )
                ]
            ),
            expand=True
        )

        page.add(splash)
        page.update()

        async def load():
            await asyncio.sleep(2)
            format_date = "%Y-%m-%d %H:%M:%S"
            maintenant = datetime.now()
            if os.path.exists("commandes.db"):
                try:
                    with open("commandes.db", "r") as f:
                        commandes = json.load(f)

                    if commandes:
                        # On récupère la date de la dernière commande
                        # (Supposant que c'est une liste et que la date est dans "date")
                        derniere_commande = commandes[-1]
                        date_cmd = datetime.strptime(derniere_commande["date"], format_date)

                        # SI LA DATE EST DÉPASSÉE (plus petite que maintenant)
                        if maintenant > date_cmd:
                            print("Date de commande dépassée, redirection vers Home.")
                            render_home(page)
                            return  # On arrête le splash ici
                except Exception as e:
                    print(f"Erreur lecture commandes: {e}")

                # --- 2. TA LOGIQUE D'EXPIRATION ACTUELLE (CONFIG_FILE) ---
            if not os.path.exists(CONFIG_FILE):
                date_limite = maintenant + timedelta(days=90)
                donnees = {"expiration_date": date_limite.strftime(format_date)}
                with open(CONFIG_FILE, "w") as f:
                    json.dump(donnees, f)
                est_expire = False
                date_fin_str = date_limite.strftime("%d/%m/%Y")
            else:
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                date_limite = datetime.strptime(config["expiration_date"], format_date)
                date_fin_str = date_limite.strftime("%d/%m/%Y")
                est_expire = maintenant > date_limite
            # --- 1. LOGIQUE DE VÉRIFICATION DE LA DATE ---
            if not os.path.exists(CONFIG_FILE):
                date_limite = maintenant + timedelta(days=90)
                donnees = {"expiration_date": date_limite.strftime(format_date)}
                with open(CONFIG_FILE, "w") as f:
                    json.dump(donnees, f)
                est_expire = False
                date_fin_str = date_limite.strftime("%d/%m/%Y")
            else:
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                date_limite = datetime.strptime(config["expiration_date"], format_date)
                date_fin_str = date_limite.strftime("%d/%m/%Y")
                est_expire = maintenant > date_limite

            # --- 2. SI EXPIREE : AFFICHER LE DIALOGUE ET STOP ---
            if est_expire:
                def fermer_app(e):
                    page.window_close(page)
                    sys.exit()

                # Remplace l'ID après 'id=' par celui de ton application
                play_store_url = "https://play.google.com/store/apps/details?id=ton.package.name"

                dialogue_expiration = ft.AlertDialog(
                    modal=True,
                    title=ft.Row(
                        [ft.Icon(ft.Icons.UPDATE, color="red"), ft.Text("Mise à jour requise")],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    content=ft.Text(
                        f"Votre version d'essai a expiré le {date_fin_str}.\n"
                        "Veuillez télécharger la version complète sur le Play Store pour continuer.",
                        size=16
                    ),
                    actions=[
                        ft.ElevatedButton(
                            "Ouvrir le Play Store",
                            icon=ft.Icons.SHOPPING_BAG,
                            bgcolor=ft.Colors.GREEN_700,
                            color=ft.Colors.WHITE,
                            on_click=lambda _: page.launch_url(play_store_url)
                        ),
                        ft.TextButton("Plus tard", on_click=fermer_app),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )

                page.overlay.append(dialogue_expiration)
                page.update()

                # Petit délai pour garantir l'affichage sur Android
                import time
                time.sleep(0.1)

                dialogue_expiration.open = True
                page.update()
                return

            # --- 3. SI NON EXPIREE : LOGIQUE DE SESSION ET SQLITE ---
            if os.path.exists("session_utilisateur.txt"):
                try:
                    # Vérification de la base de données
                    conn = sqlite3.connect("repas_db.sqlite")
                    c = conn.cursor()
                    c.execute("SELECT COUNT(*) FROM planning")
                    count = c.fetchone()[0]
                    conn.close()

                    if count > 0:
                        render_final_view(page)
                    else:
                        render_home(page)

                except Exception as e:
                    print(f"Erreur lors de la lecture : {e}")
                    go_to_login(page)
            else:
                print("Aucun fichier de session trouvé.")
                go_to_login(page)

        page.run_task(load)

    # --- DIALOGUE D'EXPIRATION (Séparé pour la clarté) ---
    def show_expiration_dialog(page, date_fin_str):
        def fermer_app(e):
            page.window_close()
            sys.exit()

        dialogue = ft.AlertDialog(
            modal=True,
            title=ft.Text("Mise à jour requise"),
            content=ft.Text(f"Version expirée le {date_fin_str}.\nInstallez la version complète."),
            actions=[
                ft.ElevatedButton("Play Store", on_click=lambda _: page.launch_url("URL_ICI")),
                ft.TextButton("Quitter", on_click=fermer_app),
            ]
        )
        page.overlay.append(dialogue)
        dialogue.open = True
        page.update()

    def modifier_plat_action(plat_name, date_iso, index_repas, rows_originales):
        # 1. On récupère la liste des noms de plats (assurez-vous que PLATS_FAMILLE est accessible)
        # On trie pour que ce soit plus facile à trouver
        options_repas = sorted(list(PLATS_FAMILLE.keys()))

        def enregistrer_modif(e):
            # Récupération de la valeur choisie dans le menu déroulant
            nouveau_nom = dd_choix.value

            if not nouveau_nom:
                return

            try:
                # Reconstruction de la chaîne des plats
                liste_plats = rows_originales.split(", ")
                if index_repas < len(liste_plats):
                    liste_plats[index_repas] = nouveau_nom

                nouveau_string = ", ".join(liste_plats)

                # Mise à jour SQL
                conn = sqlite3.connect("repas_db.sqlite")
                c = conn.cursor()
                c.execute("UPDATE planning SET repas = ? WHERE timestamp = ?", (nouveau_string, date_iso))
                conn.commit()
                conn.close()

                # Fermeture et rafraîchissement
                dlg_edit.open = False
                page.update()

                # Appel du rendu (Vérifiez que cette fonction est bien définie dans votre main)
                render_final_view()

            except Exception as ex:
                print(f"Erreur SQL : {ex}")

        # Le composant Dropdown avec recherche activée (enable_filter)
        dd_choix = ft.Dropdown(
            label="Rechercher ou choisir un plat",
            value=plat_name,
            width=400,
            bgcolor="white",
            border_radius=12,
            # 'enable_filter' permet de taper du texte pour filtrer la liste
            enable_filter=True,
            options=[ft.dropdown.Option(p) for p in options_repas],
        )

        dlg_edit = ft.AlertDialog(
            title=ft.Text("Modifier le repas", weight="bold"),
            content=ft.Column([
                ft.Text(f"Ancien plat : {plat_name}", size=12, italic=True),
                dd_choix,
            ], tight=True, spacing=15),
            actions=[
                ft.TextButton("Annuler", on_click=lambda _: (setattr(dlg_edit, "open", False), page.update())),
                ft.ElevatedButton("Enregistrer", on_click=enregistrer_modif, bgcolor=CP, color="white")
            ],
        )

        page.overlay.append(dlg_edit)
        dlg_edit.open = True
        page.update()



    # --- CONFIGURATION DES CHEMINS (Crucial pour Android) ---
    # On définit le dossier de stockage de l'application
    DB_PATH = os.getcwd()

    def render_final_view(e=None):
        try:
            global i_plat, i_jour
            page.clean()
            SESSION_FILE = "session_utilisateur.json"

            # 1. Récupération réelle de l'utilisateur
            import json
            import os

            def get_current_user():
                file_path = "session_utilisateur.json"
                default_user = {"nom": "Client Inconnu"}

                if not os.path.exists(file_path):
                    return default_user

                # On essaie d'abord de lire en UTF-8, puis en latin-1 si UTF-8 échoue (erreur 0x8a)
                for encoding_type in ["utf-8", "latin-1"]:
                    try:
                        with open(file_path, "r", encoding=encoding_type) as f:
                            content = f.read().strip()

                        if not content:
                            return default_user

                        # Cas 1 : Format JSON (recommandé)
                        if content.startswith("{"):
                            return json.loads(content)

                        # Cas 2 : Ancien format texte avec "|"
                        elif "|" in content:
                            parts = content.split("|")
                            return {"nom": parts[0]}

                        # Cas 3 : Texte brut (juste le nom)
                        else:
                            return {"nom": content}

                    except (UnicodeDecodeError, json.JSONDecodeError):
                        continue  # On tente l'encodage suivant si celui-ci plante
                    except Exception as e:
                        print(f"Erreur lecture session: {e}")
                        return default_user

                return default_user

            user_info = get_current_user()
            nom_utilisateur = user_info.get("nom", "Client Inconnu")

            # 2. Gestion de la base de données Fidelia
            import sqlite3
            DB_PATH =os.getcwd()
            conn = sqlite3.connect(os.path.join(DB_PATH, "fidelite.db"))
            cursor = conn.cursor()

            cursor.execute('''
                    CREATE TABLE IF NOT EXISTS clients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT UNIQUE,
                        points INTEGER
                    )
                ''')

            # On insère l'utilisateur actuel s'il n'existe pas
            cursor.execute('INSERT OR IGNORE INTO clients (nom, points) VALUES (?, 0)', (nom_utilisateur,))
            conn.commit()
            SESSION_FILE = "session_utilisateur.txt"

            def get_user_session():
                """Récupère les infos de l'utilisateur stockées localement"""
                try:
                    with open(SESSION_FILE, "r", encoding="utf-8") as f:
                        return json.loads(f.read())
                except:
                    return {"nom": "Client Inconnu", "tel": "Non spécifié", "ville": "N/A", "quartier": "N/A"}

            user_info = get_user_session()
            nom_client = user_info.get("nom", "Client")

            # On récupère ses points
            cursor.execute('SELECT points FROM clients WHERE nom = ?', (nom_utilisateur,))
            resultat = cursor.fetchone()
            conn = sqlite3.connect('fidelite.db')
            cursor = conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO clients (nom, points) VALUES (?, 0)', (nom_client,))
            conn.commit()

            cursor.execute('SELECT points FROM clients WHERE nom = ?', (nom_client,))
            resultat = cursor.fetchone()
            conn.close()

            points_actuels = resultat[0] if resultat else 0



            with open("liste.json", "r") as f:
                ELEMENTS_VALUES = json.load(f)

            # 1. Préparation des dates
            today_iso = datetime.now().strftime("%Y-%m-%d")
            tomorrow_iso = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            rows = []

            # 2. Récupération sécurisée du planning
            try:
                conn = sqlite3.connect(os.path.join(DB_PATH,"repas_db.sqlite"))
                c = conn.cursor()
                c.execute("SELECT repas, timestamp FROM planning WHERE timestamp IN (?, ?)", (today_iso, tomorrow_iso))
                rows = c.fetchall()
                conn.close()
            except Exception as e:
                print(f"Erreur SQL Planning : {e}")

            # 3. Action d'annulation avec rafraîchissement
            def annuler_commande_action(plat_name, date_a_annuler):
                SESSION_FILE = "session_utilisateur.txt"

                def get_user_session():
                    """Récupère les infos de l'utilisateur (Gestion des formats JSON ou Texte)"""
                    try:
                        if not os.path.exists(SESSION_FILE): return {}
                        with open(SESSION_FILE, "r", encoding="utf-8") as f:
                            content = f.read()
                            if "|" in content:  # Format Texte Pipe
                                d = content.split("|")
                                return {"nom": d[0], "tel": d[2], "ville": d[3], "quartier": d[4]}
                            else:  # Format JSON
                                return json.loads(content)
                    except:
                        return {"nom": "Client", "tel": "Inconnu"}

                def valider_annulation(e):
                    try:
                        # 1. Vérification Connexion Internet
                        requests.get('https://www.google.com',timeout=5)

                        # 2. Préparation des données pour l'Admin
                        user_info = get_user_session()
                        date_jour = datetime.now().strftime("%Y-%m-%d")

                        demande_annulation = {
                            "client": user_info.get("nom"),
                            "telephone": user_info.get("tel"),
                            "ville": user_info.get("ville"),
                            "quartier": user_info.get("quartier"),
                            "type": "ANNULATION_KIT",
                            "nom_plat": plat_name,
                            "date_action": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "statut": "Demande Reçue"
                        }

                        # 3. Envoi à Firebase

                        # 4. Suppression Locale (SQLite) pour libérer le bouton
                        today = datetime.now().strftime("%Y-%m-%d")  # Format identique

                        with sqlite3.connect("commandes.db") as conn:
                            c = conn.cursor()
                            c.execute(
                                "DELETE FROM commandes WHERE nom_plat = ? AND date_commande = ?",
                                (plat_name, date_a_annuler)
                            )
                            conn.commit()

                        # 5. Fermeture et Feedback
                        # 5. Fermeture et Feedback
                        dlg.open = False
                        page.update()

                        # 6. Feedback
                        page.snack_bar = ft.SnackBar(
                            content=ft.Text(f"Annulation confirmée pour {plat_name}"),
                            bgcolor="red-700"
                        )
                        page.snack_bar.open = True

                        # 7. RECHARGER LA VUE (Correction ici)
                        import time
                        # Laisse le temps au système de fermer le fichier DB
                        page.clean()
                        page.update()
                        render_final_view()

                    except (requests.ConnectionError, requests.Timeout):
                        no_connexion()
                    except Exception as ex:
                        print(f"Erreur lors de l'annulation : {ex}")

                # --- DIALOGUE DE CONFIRMATION ---
                dlg = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Annuler la commande ?"),
                    content=ft.Text(
                        f"Voulez-vous vraiment annuler la livraison des ingrédients pour le plat : {plat_name} ?"),
                    actions=[
                        ft.TextButton("NON, GARDER", on_click=lambda _: (setattr(dlg, "open", False), page.update())),
                        ft.ElevatedButton("OUI, ANNULER", bgcolor="red", color="white", on_click=valider_annulation),
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )

                page.overlay.append(dlg)
                dlg.open = True
                page.update()

            # 4. Interface de base
            lv = ft.ListView(expand=True, spacing=0, padding=15)
            repas_labels = ["Petit-déjeuner", "Déjeuner", "Dîner", "Goûter", "Extra"]
            if os.path.exists("session_utilisateur.txt"):
                mns = "Se deconnecter"
            else:
                mns = "Se connecter"
            options_btn = ft.PopupMenuButton(
                # Style du menu (Coins arrondis typiques de Material 3)
                menu_position=ft.PopupMenuPosition.UNDER,
                shape=ft.RoundedRectangleBorder(radius=15),
                items=[
                    # SECTION COMPTE / UTILISATEUR
                    ft.PopupMenuItem(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PERSON_OUTLINE, size=20, color=ft.Colors.BLUE_700),
                            ft.Text(mns, weight="w500")
                        ], spacing=10),
                        on_click=lambda _: cv()
                    ),
                    ft.PopupMenuItem(content=ft.Divider(height=1, thickness=1)),  # Séparateur

                    # SECTION NAVIGATION / SERVICES
                    ft.PopupMenuItem(
                        content=ft.Row([
                            ft.Icon(ft.Icons.STOREFRONT_OUTLINED, size=20, color=CP),
                            ft.Text("Aller au Marché")
                        ], spacing=10),
                        on_click=lambda _: render_market(page, render_final_view)
                    ),
                    ft.PopupMenuItem(
                        content=ft.Row([
                            ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, size=20, color=CP),
                            ft.Text("Prêt Alimentaire")
                        ], spacing=10),
                        on_click=lambda _: render_loan_page(page, render_final_view)
                    ),
                    ft.PopupMenuItem(content=ft.Divider(height=1, thickness=1)),

                    # SECTION ACTIONS SYSTÈME
                    ft.PopupMenuItem(
                        content=ft.Row([
                            ft.Icon(ft.Icons.RESTART_ALT, size=20, color=ft.Colors.ORANGE_700),
                            ft.Text("Nouveau Planning", color=ft.Colors.ORANGE_700)
                        ], spacing=10),
                        on_click=lambda _: render_home()
                    ),
                ],
                # Aspect du bouton déclencheur (Look "Chip" moderne)
                content=ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.SETTINGS_OUTLINED, color=CP, size=18),
                        ft.Text("Options", color=CP, weight="bold", size=13),
                        ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=CP, size=20)
                    ], spacing=5, alignment=ft.Alignment(0, 0)),
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    bgcolor=ft.Colors.with_opacity(0.1, CP),  # Fond léger de la couleur primaire
                    border_radius=20  # Style "pill" ou "chip"
                )
            )

            # 5. Message si planning vide
            if not rows:
                lv.controls.append(
                    ft.Container(
                        padding=30,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=20,
                        content=ft.Column([
                            ft.Icon(ft.Icons.RESTAURANT_MENU_ROUNDED, size=50, color=CP),
                            ft.Text("Aucun planning trouvé", size=18, weight="bold"),
                            ft.Text("Appuyez sur le bouton pour calculer vos repas selon les prix du Togo.",
                                    text_align="center", color=CT2),
                            ft.Container(height=10),
                            ft.ElevatedButton(
                                content=ft.Row([
                                    ft.Icon(ft.Icons.AUTO_AWESOME),
                                    ft.Text("GÉNÉRER UN PLANNING", weight="bold")
                                ], alignment="center"),
                                bgcolor=CP,
                                color="white",
                                height=50,
                                width=400,  # Format large Android
                                on_click=render_home,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                            )
                        ], horizontal_alignment="center")
                    )
                )

            # 6. Boucle de génération des cartes
            for iso, label, shipping in [(today_iso, "Aujourd'hui", DELIVERY_TODAY),
                                         (tomorrow_iso, "Demain", DELIVERY_TOMORROW)]:
                day_data = [r for r in rows if r[1] == iso]
                if day_data:
                    lv.controls.append(create_section_header(label, datetime.now().strftime(
                        "%d %b") if label == "Aujourd'hui" else (datetime.now() + timedelta(1)).strftime("%d %b")))

                    for entry in day_data:
                        plats_list = entry[0].split(", ")
                        for i, plat_name in enumerate(plats_list):
                            prix_plat = ELEMENTS_VALUES.get(plat_name, 0)

                            # VERIFICATION DU VERROUILLAGE
                            deja_pris = est_commande(plat_name, iso)

                            lv.controls.append(
                                ft.Container(
                                    padding=20,
                                    bgcolor=CC,
                                    border_radius=20,  # Coins plus arrondis pour le look M3
                                    margin=ft.margin.only(bottom=15),
                                    shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.with_opacity(0.05, "black")),
                                    # Ombre légère
                                    content=ft.Column([
                                        # HEADER : Badge Repas + Bouton Modifier
                                        ft.Row([
                                            ft.Container(
                                                ft.Text(repas_labels[i].upper() if i < 5 else "EXTRA",
                                                        size=10, color="white", weight="bold"),
                                                bgcolor=CP,
                                                padding=ft.padding.symmetric(horizontal=10, vertical=4),
                                                border_radius=8
                                            ),
                                            ft.IconButton(
                                                icon=ft.Icons.EDIT_OUTLINED,  # Style plus léger
                                                icon_color=ft.Colors.GREY_600,
                                                icon_size=20,
                                                tooltip="Modifier ce plat",
                                                on_click=lambda _, p=plat_name, d=iso, idx=i, raw=entry[0]:
                                                modifier_plat_action(p, d, idx, raw)
                                            ),
                                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                                        # CORPS : Nom et Détails
                                        ft.Column([
                                            ft.Text(plat_name, size=18, weight="bold", color=CT1),
                                            ft.Row([
                                                ft.Text(f"{prix_plat} FCFA", size=16, weight="w500", color=CP),
                                                ft.Text("•", color=CT2),
                                                ft.Text(f"Livraison {shipping} FCFA", size=14, color=CT2),
                                            ], spacing=8),
                                        ], spacing=4),

                                        ft.Divider(height=20, color="transparent"),

                                        # ACTIONS : Commander / Annuler
                                        ft.Row([
                                            # BOUTON COMMANDER (Primaire)
                                            ft.ElevatedButton(
                                                content=ft.Row([
                                                    ft.Icon(ft.Icons.CHECK_CIRCLE if deja_pris else ft.Icons.SHOPPING_CART,
                                                            size=18),
                                                    ft.Text("Commandé" if deja_pris else "Commander", weight="bold")
                                                ], alignment=ft.MainAxisAlignment.CENTER),
                                                style=ft.ButtonStyle(
                                                    color="white",
                                                    bgcolor=ft.Colors.GREY_400 if deja_pris else CP,
                                                    shape=ft.RoundedRectangleBorder(radius=12),
                                                ),
                                                expand=True,
                                                disabled=deja_pris,  # On peut désactiver si déjà pris
                                                on_click=lambda _, p=plat_name, pr=prix_plat, s=shipping, idx=i, d=iso:
                                                render_order_page(p, pr, s, idx, d)
                                            ),

                                            # BOUTON ANNULER (Secondaire / Outlined)
                                            ft.OutlinedButton(
                                                content=ft.Row([
                                                    ft.Icon(ft.Icons.CLOSE, size=18,
                                                            color="red" if deja_pris else ft.Colors.GREY_400),
                                                    ft.Text("Annuler", color="red" if deja_pris else ft.Colors.GREY_400)
                                                ], alignment=ft.MainAxisAlignment.CENTER),
                                                style=ft.ButtonStyle(
                                                    shape=ft.RoundedRectangleBorder(radius=12),
                                                    side={ft.ControlState.DEFAULT: ft.BorderSide(1,
                                                                                                 "red" if deja_pris else ft.Colors.GREY_200)},
                                                ),
                                                visible=deja_pris,  # On ne l'affiche que si une commande existe
                                                expand=True,
                                                on_click=lambda _, p=plat_name, d=iso: annuler_commande_action(p, d)
                                            )
                                        ], spacing=12)
                                    ], spacing=0)
                                )
                            )

            # 7. Affichage Final
            # --- Logique de progression ---

            # --- UI ---
            # Header avec correction du bug ImageFit
            def get_loyalty_data(points):
                if points <= 2:
                    return "NIVEAU BRONZE", "❤", ft.Colors.BROWN_400
                elif points <= 5:
                    return "NIVEAU ARGENT", "💕", ft.Colors.BLUE_GREY_400
                elif points <= 10:
                    return "NIVEAU OR", "🥇", ft.Colors.AMBER_600
                elif points <= 20:
                    return "NIVEAU PLATINE", "💎", ft.Colors.CYAN_400
                else:
                    return "NIVEAU LÉGENDE", "👑", ft.Colors.AMBER_700

            rank_name, emoji, rank_color = get_loyalty_data(points_actuels)

            # 1. HEADER
            header = ft.Container(
                padding=ft.padding.only(top=50, left=20, right=20, bottom=10),
                content=ft.Row([
                    ft.Image(src="logo.png", height=40, fit="contain"),
                    options_btn
                ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),  # Utilisation de string pour éviter les erreurs
            )

            # 2. BADGE DE FIDÉLITÉ
            fidelia_badge = ft.Container(
                margin=ft.margin.symmetric(horizontal=20, vertical=10),
                padding=15,
                border_radius=20,
                bgcolor="white",
                shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.05, "black")),
                content=ft.Row([
                    ft.Row([
                        # Icône de gauche
                        ft.Container(
                            content=ft.Text(emoji, size=22),
                            bgcolor=ft.Colors.with_opacity(0.1, rank_color),
                            width=45, height=45,
                            border_radius=22,
                            alignment=ft.Alignment(0, 0)  # Correction ici : (0,0) est le centre exact
                        ),
                        # Texte
                        ft.Column([
                            ft.Text(f"{points_actuels} Points Fidelia", size=16, weight="bold", color="black"),
                            ft.Text(rank_name, size=11, weight="w500", color=rank_color),
                        ], spacing=20)
                    ], spacing=15),
                    ft.Icon(ft.Icons.CHEVRON_RIGHT, color=ft.Colors.GREY_400)
                ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN )
            )

            page.add(header, fidelia_badge, lv)
            page.update()
        except Exception as e:
            import traceback
            print("ERREUR FATALE :", e)
            print(traceback.format_exc())
            page.add(ft.Text("l´app a planter"))
    def open_edit_modal(idx):  # L'argument est 'idx'
        day_data = state["planning_genere"][idx]

        # Préparation des options (Plats sélectionnés par l'utilisateur)
        choices = [ft.dropdown.Option(p) for p in state["plats_selectionnes"].keys()]

        dropdowns = []
        for i, current_plat in enumerate(day_data["plats_noms"]):
            dropdowns.append(
                ft.Dropdown(
                    label=f"Repas {i + 1}",
                    options=choices,
                    value=current_plat,
                    border_radius=12,
                    focused_border_color=CP,
                    content_padding=10
                )
            )

        def save_edit(e):
            new_selection = [dd.value for dd in dropdowns]

            # UX TIP: Charger le JSON une seule fois ou utiliser le dictionnaire global
            try:
                with open("liste.json", "r") as f:
                    ELEMENTS_VALUES = json.load(f)
            except Exception as err:
                print(f"Erreur JSON: {err}")
                ELEMENTS_VALUES = {}

            # Mise à jour des données dans le state
            state["planning_genere"][idx]["plats_noms"] = new_selection
            # Recalcul du coût pour cette journée spécifique
            state["planning_genere"][idx]["cout"] = sum(int(ELEMENTS_VALUES.get(n, 0)) for n in new_selection)

            dlg.open = False
            page.update()
            # On rafraîchit la page de vérification pour voir les changements
            render_verification()

        # Création du dialogue
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Column([
                # CORRECTION : On utilise 'idx' car c'est le nom du paramètre de la fonction
                ft.Text(f"Modifier le Jour {idx + 1}", weight="bold", size=20),
                ft.Text("Sélectionnez vos nouveaux plats :", size=13, color="grey700")
            ], spacing=5),

            content=ft.Container(
                content=ft.Column(dropdowns, tight=True, spacing=15),
                width=400,
                padding=ft.padding.symmetric(vertical=10)
            ),

            actions=[
                ft.TextButton(
                    "Annuler",
                    icon=ft.Icons.CLOSE,
                    on_click=lambda _: (setattr(dlg, "open", False), page.update())
                ),
                ft.ElevatedButton(
                    "Valider",
                    icon=ft.Icons.CHECK_ROUNDED,
                    on_click=save_edit,
                    bgcolor=CP,
                    color="white",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=20)
        )

        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    # On définit une couleur d'erreur plus douce pour l'UX

    def show_error(msg):
        # Création du dialogue
        CERR = "#D32F2F"
        dlg = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=24),  # Coins plus arrondis pour un look moderne
            content_padding=ft.padding.all(25),
            title=ft.Text(
                "Oups ! Quelque chose coince",
                weight="bold",
                size=20,
                text_align="center"
            ),
            content=ft.Column([
                # Icône avec effet de cercle en fond
                ft.Container(
                    content=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=CERR, size=50),
                    bgcolor=ft.Colors.with_opacity(0.1, CERR),
                    padding=20,
                    shape=ft.BoxShape.CIRCLE,
                ),
                ft.Text(
                    msg,
                    size=15,
                    color="grey700",
                    text_align=ft.TextAlign.CENTER,
                ),
            ], tight=True, spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            actions=[
                ft.Container(
                    width=float("inf"),  # Bouton qui prend toute la largeur
                    content=ft.ElevatedButton(
                        "RÉESSAYER",
                        on_click=lambda _: (setattr(dlg, "open", False), page.update()),
                        bgcolor=CP,
                        color="white",
                        height=50,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=12),
                        )
                    ),
                    padding=ft.padding.only(left=10, right=10, bottom=10)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
        )

        # Ajout à l'overlay et affichage
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def render_verification():
        page.clean()

        # Calcul du coût total pour le résumé
        total_planning = sum(int(d['cout']) for d in state["planning_genere"])

        # ListView optimisée
        scroll_lv = ft.ListView(expand=True, spacing=15, padding=15)

        for i, d in enumerate(state["planning_genere"]):
            scroll_lv.controls.append(
                ft.Container(
                    padding=15,
                    bgcolor="white",
                    border_radius=15,
                    border=ft.border.all(1, "grey200"),
                    shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.05, "black")),
                    content=ft.Row([
                        # Badge Jour
                        ft.Container(
                            content=ft.Text(str(i + 1), color="white", weight="bold"),
                            bgcolor=CP,
                            width=35,
                            height=35,
                            border_radius=20,
                            alignment=ft.Alignment(0, 0)
                        ),
                        ft.VerticalDivider(width=1, color="transparent"),
                        # Infos Repas
                        ft.Column([
                            ft.Text(f"{d['date']}".upper(), size=11, color=CP, weight="bold"),
                            ft.Text(", ".join(d["plats_noms"]), size=15, weight="w600", color=CT1),
                            ft.Row([
                                ft.Icon(ft.Icons.MONETIZATION_ON_OUTLINED, size=14, color=CT2),
                                ft.Text(f"{int(d['cout'])} FCFA", size=13, color=CT2, weight="w500"),
                            ], spacing=4)
                        ], expand=True, spacing=2),
                        # Bouton d'édition stylisé
                        ft.IconButton(
                            ft.Icons.EDIT_NOTE_ROUNDED,
                            icon_color=CP,
                            icon_size=28,
                            tooltip="Modifier ce jour",
                            on_click=lambda _, idx=i: open_edit_modal(idx)
                        )
                    ])
                )
            )

        page.add(
            # 1. Header avec Résumé Budgétaire
            ft.Container(
                padding=ft.padding.only(top=40, left=20, right=20, bottom=20),
                bgcolor=CP,
                content=ft.Column([
                    ft.Row([
                        ft.IconButton(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, icon_color="white",
                                      on_click=lambda _: render_home())
                        ,
                        ft.Text("VÉRIFICATION", color="white", size=18, weight="bold", expand=True),
                        ft.Image(src="logo.png", height=35),
                    ]),
                    ft.Container(height=10),
                    ft.Row([
                        ft.Column([
                            ft.Text("Budget Total estimé", color="white70", size=12),
                            ft.Text(f"{total_planning} FCFA", color="white", size=22, weight="bold"),
                        ]),
                        ft.VerticalDivider(color="white30"),
                        ft.Column([
                            ft.Text("Durée", color="white70", size=12),
                            ft.Text(f"{len(state['planning_genere'])} Jours", color="white", size=18, weight="bold"),
                        ]),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ])
            ),

            # 2. Corps de la page (Scrollable)
            ft.Container(
                expand=True,
                bgcolor="#F8F9FA",  # Fond gris très léger pour faire ressortir les cartes blanches
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("Détail de votre semaine :", color=CT2, weight="w500"),
                        padding=ft.padding.only(left=20, top=15, bottom=5)
                    ),
                    scroll_lv,
                ], spacing=0)
            ),

            # 3. Bouton d'action fixe
            ft.Container(
                padding=20,
                bgcolor="white",
                border=ft.border.only(top=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT)),
                content=ft.ElevatedButton(
                    "CONFIRMER ET ENREGISTRER",
                    icon=ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                    on_click=save_final,
                    bgcolor=CP,
                    color="white",
                    height=55,
                    width=float("inf"),
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                )
            )
        )
        page.update()

    def save_final(e):
        init_db()
        conn = sqlite3.connect("repas_db.sqlite")
        c = conn.cursor()
        c.execute("DELETE FROM planning")
        for d in state["planning_genere"]:
            c.execute("INSERT INTO planning (date_str, repas, cout, timestamp) VALUES (?, ?, ?, ?)",
                      (d["date"], ", ".join(d["plats_noms"]), d["cout"], d["raw_date"]))
        conn.commit()
        conn.close()
        render_final_view()

    def generate_plan(e):

        if not state["plats_selectionnes"]:
            show_error("Veuillez choisir des plats dans la liste avant de générer.")
            return

        b, d, r_j, limit = float(budg_total.value), int(days_input.value), int(meals_input.value), float(
            daily_limit.value)
        nb = int(guests_input.value)

        if nb <= 2:
            ele = PLATS_PETIT_COMITE
        elif 3 <= nb <= 5:
            ele = PLATS_FAMILLE
        elif 6 <= nb <= 20:
            ele = PLATS_GRANDE_TABLE

        with open("liste.json", "w+") as liste:
            json.dump(ele, liste)

        temp_res, current_dt = [], datetime.now()
        pool = list(state["plats_selectionnes"].keys())

        for i in range(d):
            success = False
            for attempt in range(100):
                selection = random.sample(pool, k=min(r_j, len(pool)))
                cost = sum(ele.get(n, 0) for n in selection)
                if cost <= limit and b >= cost:
                    b -= cost
                    temp_res.append({
                        "date": f"{JOURS_FR[current_dt.weekday()]} {current_dt.day}",
                        "raw_date": current_dt.strftime("%Y-%m-%d"),
                        "plats_noms": selection, "cout": cost
                    })
                    success = True;
                    break
            if not success:
                show_error(f"Budget insuffisant pour le jour {i + 1}.")
                return
            current_dt += timedelta(days=1)
        state["planning_genere"] = temp_res
        render_verification()

    search_timer = None
    def render_home():
        page.clean()
        CP = "#5D8A66"

        # --- DIALOGUE D'INFORMATION (REAJOUTÉ) ---
        def close_dlg(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, color=CP),
                ft.Text(" INFO LOGISTIQUE", weight="bold")
            ], alignment=ft.MainAxisAlignment.CENTER),
            content=ft.Text(
                "Cher utilisateur, nous ne livrons pas de repas préparés, mais tous les ingrédients frais nécessaires pour les cuisiner vous-même.",
                text_align=ft.TextAlign.CENTER,
                size=15
            ),
            actions=[
                ft.TextButton("J'AI COMPRIS", on_click=close_dlg, style=ft.ButtonStyle(color=CP))
            ],
            actions_alignment=ft.MainAxisAlignment.CENTER,
            shape=ft.RoundedRectangleBorder(radius=15),
        )

        # --- LOGIQUE DES SÉLECTIONS (CHIPS) ---
        chips_row = ft.Row(wrap=False, scroll=ft.ScrollMode.ADAPTIVE)

        selection_container = ft.Container(
            content=chips_row,
            margin=ft.margin.only(top=5, bottom=10),
            height=50,
        )

        def create_chip_widget(nom_plat):
            return ft.Chip(
                label=ft.Text(nom_plat),
                bgcolor=ft.Colors.GREEN_50,
                on_delete=lambda e: delete_action(nom_plat, e.control)
            )

        def delete_action(nom_plat, chip_obj):
            if nom_plat in state["plats_selectionnes"]:
                del state["plats_selectionnes"][nom_plat]
                chips_row.controls.remove(chip_obj)
                page.update()

        # Rechargement des plats depuis le state
        chips_row.controls.clear()
        for nom in state["plats_selectionnes"].keys():
            chips_row.controls.append(create_chip_widget(nom))

        def add_item(n, p):
            if n not in state["plats_selectionnes"]:
                state["plats_selectionnes"][n] = p
                chips_row.controls.append(create_chip_widget(n))
                page.update()

        # --- RECHERCHE ET RÉSULTATS ---
        import threading

        # 1. On garde la variable ici, locale à render_home
        search_timer = None

        def show_results(query=""):
            # 2. IMPORTANT : On utilise nonlocal car search_timer
            # appartient à la fonction parente (render_home)
            nonlocal search_timer

            # Annuler le lancement précédent si on continue de taper
            if search_timer is not None:
                search_timer.cancel()

            def perform_search():
                # Pour éviter les crashs si l'utilisateur quitte la page pendant la recherche
                try:
                    search_results.controls.clear()
                    nb = float(guests_input.value or 1)
                    dico, _ = get_active_dict(nb)

                    query_lower = query.lower()
                    filtered_items = []

                    # Filtrage optimisé
                    for k, v in dico.items():
                        if query_lower in k.lower():
                            filtered_items.append((k, v))
                        if len(filtered_items) >= 15:
                            break

                    new_controls = []
                    for n, p in filtered_items:
                        # Déterminer la catégorie de prix
                        if p <= 2000:
                            t, clr = "Éco", ft.Colors.GREEN_400
                        elif p <= 7000:
                            t, clr = "Moyen", ft.Colors.ORANGE_400
                        else:
                            t, clr = "Premium", ft.Colors.PURPLE_400

                        new_controls.append(
                            ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.Icons.RESTAURANT_MENU, color=clr, size=20),
                                    title=ft.Text(n, weight="w500", size=14),
                                    subtitle=ft.Text(f"{p} FCFA • {t}", size=12),
                                    trailing=ft.IconButton(
                                        ft.Icons.ADD_CIRCLE,
                                        icon_color=CP,
                                        on_click=lambda _, n=n, p=p: add_item(n, p)
                                    ),
                                ),
                                border=ft.border.all(1, ft.Colors.GREY_100),
                                border_radius=10,
                                margin=ft.margin.only(bottom=5)
                            )
                        )

                    search_results.controls = new_controls
                    page.update()
                except Exception as e:
                    print(f"Erreur dans perform_search: {e}")

            # 3. On relance le timer (Délai de 300ms)
            search_timer = threading.Timer(0.3, perform_search)
            search_timer.start()

        # --- MISE EN PAGE FINALE ---
        page.add(
            ft.Container(
                padding=15,
                content=ft.Row([
                    ft.Image(src="logo.png", height=45),
                    ft.Text("CLIEXE ASSISTANT", weight="bold", color=CP, size=18)
                ])
            ),
            ft.Container(
                padding=20,
                expand=True,
                content=ft.Column([
                    # Configuration Inputs
                    ft.Row([guests_input, days_input], spacing=10),
                    ft.Row([budg_total, daily_limit], spacing=10),
                    ft.Row([meals_input], spacing=15),

                    ft.Divider(height=10, color="transparent"),

                    ft.TextField(
                        hint_text="Que voulez-vous cuisiner ?",
                        prefix_icon=ft.Icons.SEARCH,
                        on_change=lambda e: show_results(e.control.value.lower()),
                        border_radius=15,
                        border_color=CP
                    ),

                    ft.Text("Vos sélections :", size=12, weight="bold", color="grey600"),
                    selection_container,

                    ft.Text("Suggestions & Résultats", weight="bold", size=16),
                    ft.Container(content=ft.Column([chips_row, search_results], scroll=ft.ScrollMode.AUTO), height=250,
                                 padding=10, border=ft.border.all(1, "#EEEEEE"), border_radius=12),


                    ft.ElevatedButton(
                        "GÉNÉRER MON PLANNING",
                        icon=ft.Icons.AUTO_AWESOME,
                        on_click=generate_plan,
                        bgcolor=CP, color="white",
                        height=55, width=float("inf"),
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=12))
                    ),
                ], spacing=10)
            )
        )

        # Affichage du dialogue et des premiers résultats
        page.overlay.append(dlg)
        dlg.open = True
        show_results()
        page.update()

    render_splash(page)


ft.app(target=main)
