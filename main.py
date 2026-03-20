
import sys
import flet as ft
import random
from datetime import datetime, timedelta
import sqlite3
import logging
import json
import requests
import os

CONFIG_FILE = ".app_config.json"
CP = "#5D8A66"  # Vert Primair
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
dica1 = {
    "DEGUE(ARACHIDE)": [
        "lait",
        "couscous",
        "sucre",
        "glace",
        "arachide"
    ],"DEGUE SIMPLE": [
        "lait",
        "couscous",
        "sucre",
        "glace",
        "arachide"
    ],
    "TAPIOCA ZOGBON": [
        "tapioca",
        "sel",
        "sucre",
        "lait en poudre"
    ],
    "ATTIEKE POISSON": [
        "poisson frais",
        "attieke",
        "oignon",
        "ail",
        "piment frai",
        "huile d´arachide",
        "sel",
        "cube"

    ],
    "SPAGHETTI BLANC": ["spagheti", "sel", "piment frais", "huil", "cube", ],
    "SALADE": [
        "Laitue",
        "Tomate",
        "oignon",
        "Beterave",
        "Carotte",
        "Concombre",
        "Mayonnaise",
        "cube",
        "sardine",
        "oeuf",
        "spagheti",
        "huil",
        "vinaigre",
        "pain"
    ],
    "HARICO HUIL ROUGE ": [
        "harico",
        "sel",
        "potasse",
        "oignon",
        "ail",
        "huil rouge",
        "Gari"
    ],
    "HARICO HUIL ARACHIDE 1": [
        "harico",
        "sel",
        "potasse",
        "oignon",
        "ail",
        "huil d´arachide",
        "Gari"
    ],
    "HARICO HUIL ARACHIDE 2": [
        "harico",
        "sel",
        "potasse",
        "oignon",
        "huil d´arachide",
        "Gari"
    ]
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
    {"n": "maïs", "p": 600, "u": "bole", "c": "Féculents"},
    {"n": "Pâte de maïs fermentée", "p": 200, "u": "boule", "c": "Féculents"},
    {"n": "Riz", "p": 600, "u": "kg", "c": "Féculents"},
    {"n": "Couscous", "p": 1000, "u": "paquet", "c": "Féculents"},
    {"n": "Spaghetti", "p": 350, "u": "paquet", "c": "Féculents"},
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



#---------------------------------------------------------------------------------------------
#generateur 1-3
#---------------------------------------------------------------------------------------------
# --- Initialisation des résultats ---
lis2 = {}
lis1 ={'TEKON(IGNAME BOULLIE) sauce TOMATE avec RIEN ': 2725, 'TEKON(IGNAME BOULLIE) sauce TOMATE avec AKPALAN(POISSON FUME)': 3225, 'TEKON(IGNAME BOULLIE) sauce TOMATE avec DEUEVI(PETIT POISSON)': 2925, 'TEKON(IGNAME BOULLIE) sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 3025, 'TEKON(IGNAME BOULLIE) sauce TOMATE avec POULET': 3225, 'TEKON(IGNAME BOULLIE) sauce TOMATE avec BOEUF': 3725, 'TEKON(IGNAME BOULLIE) sauce TOMATE avec MOUTON': 3725, 'TEKON(IGNAME BOULLIE) sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 3225, 'TEKON(IGNAME BOULLIE) sauce TOMATE avec AGLAN(CRABE)': 3225, 'TEKON(IGNAME BOULLIE) sauce TOMATE avec CREVETTE': 3225, 'ABLO sauce TOMATE avec RIEN ': 3825, 'ABLO sauce TOMATE avec AKPALAN(POISSON FUME)': 4325, 'ABLO sauce TOMATE avec DEUEVI(PETIT POISSON)': 4025, 'ABLO sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 4125, 'ABLO sauce TOMATE avec POULET': 4325, 'ABLO sauce TOMATE avec BOEUF': 4825, 'ABLO sauce TOMATE avec MOUTON': 4825, 'ABLO sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 4325, 'ABLO sauce TOMATE avec AGLAN(CRABE)': 4325, 'ABLO sauce TOMATE avec CREVETTE': 4325, 'DJINKOUME sauce TOMATE avec RIEN ': 2100, 'DJINKOUME sauce TOMATE avec AKPALAN(POISSON FUME)': 2600, 'DJINKOUME sauce TOMATE avec DEUEVI(PETIT POISSON)': 2300, 'DJINKOUME sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 2400, 'DJINKOUME sauce TOMATE avec POULET': 2600, 'DJINKOUME sauce TOMATE avec BOEUF': 3100, 'DJINKOUME sauce TOMATE avec MOUTON': 3100, 'DJINKOUME sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 2600, 'DJINKOUME sauce TOMATE avec AGLAN(CRABE)': 2600, 'DJINKOUME sauce TOMATE avec CREVETTE': 2600, 'COUSCOUS sauce TOMATE avec RIEN ': 2725, 'COUSCOUS sauce TOMATE avec AKPALAN(POISSON FUME)': 3225, 'COUSCOUS sauce TOMATE avec DEUEVI(PETIT POISSON)': 2925, 'COUSCOUS sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 3025, 'COUSCOUS sauce TOMATE avec POULET': 3225, 'COUSCOUS sauce TOMATE avec BOEUF': 3725, 'COUSCOUS sauce TOMATE avec MOUTON': 3725, 'COUSCOUS sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 3225, 'COUSCOUS sauce TOMATE avec AGLAN(CRABE)': 3225, 'COUSCOUS sauce TOMATE avec CREVETTE': 3225, 'KOLIKO sauce TOMATE avec RIEN ': 3025, 'KOLIKO sauce TOMATE avec AKPALAN(POISSON FUME)': 3525, 'KOLIKO sauce TOMATE avec DEUEVI(PETIT POISSON)': 3225, 'KOLIKO sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 3325, 'KOLIKO sauce TOMATE avec POULET': 3525, 'KOLIKO sauce TOMATE avec BOEUF': 4025, 'KOLIKO sauce TOMATE avec MOUTON': 4025, 'KOLIKO sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 3525, 'KOLIKO sauce TOMATE avec AGLAN(CRABE)': 3525, 'KOLIKO sauce TOMATE avec CREVETTE': 3525, 'TIMBANI sauce TOMATE avec RIEN ': 1725, 'TIMBANI sauce TOMATE avec AKPALAN(POISSON FUME)': 2225, 'TIMBANI sauce TOMATE avec DEUEVI(PETIT POISSON)': 1925, 'TIMBANI sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 2025, 'TIMBANI sauce TOMATE avec POULET': 2225, 'TIMBANI sauce TOMATE avec BOEUF': 2725, 'TIMBANI sauce TOMATE avec MOUTON': 2725, 'TIMBANI sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 2225, 'TIMBANI sauce TOMATE avec AGLAN(CRABE)': 2225, 'TIMBANI sauce TOMATE avec CREVETTE': 2225, 'RIZ sauce TOMATE avec RIEN ': 1975, 'RIZ sauce TOMATE avec AKPALAN(POISSON FUME)': 2475, 'RIZ sauce TOMATE avec DEUEVI(PETIT POISSON)': 2175, 'RIZ sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 2275, 'RIZ sauce TOMATE avec POULET': 2475, 'RIZ sauce TOMATE avec BOEUF': 2975, 'RIZ sauce TOMATE avec MOUTON': 2975, 'RIZ sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 2475, 'RIZ sauce TOMATE avec AGLAN(CRABE)': 2475, 'RIZ sauce TOMATE avec CREVETTE': 2475, 'AMANDA(ALLOCO) sauce TOMATE avec RIEN ': 2525, 'AMANDA(ALLOCO) sauce TOMATE avec AKPALAN(POISSON FUME)': 3025, 'AMANDA(ALLOCO) sauce TOMATE avec DEUEVI(PETIT POISSON)': 2725, 'AMANDA(ALLOCO) sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 2825, 'AMANDA(ALLOCO) sauce TOMATE avec POULET': 3025, 'AMANDA(ALLOCO) sauce TOMATE avec BOEUF': 3525, 'AMANDA(ALLOCO) sauce TOMATE avec MOUTON': 3525, 'AMANDA(ALLOCO) sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 3025, 'AMANDA(ALLOCO) sauce TOMATE avec AGLAN(CRABE)': 3025, 'AMANDA(ALLOCO) sauce TOMATE avec CREVETTE': 3025, 'AYIMOLOU sauce TOMATE avec RIEN ': 2500, 'AYIMOLOU sauce TOMATE avec AKPALAN(POISSON FUME)': 3000, 'AYIMOLOU sauce TOMATE avec DEUEVI(PETIT POISSON)': 2700, 'AYIMOLOU sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 2800, 'AYIMOLOU sauce TOMATE avec POULET': 3000, 'AYIMOLOU sauce TOMATE avec BOEUF': 3500, 'AYIMOLOU sauce TOMATE avec MOUTON': 3500, 'AYIMOLOU sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 3000, 'AYIMOLOU sauce TOMATE avec AGLAN(CRABE)': 3000, 'AYIMOLOU sauce TOMATE avec CREVETTE': 3000, 'SPAGHETTI sauce TOMATE avec RIEN ': 1575, 'SPAGHETTI sauce TOMATE avec AKPALAN(POISSON FUME)': 2075, 'SPAGHETTI sauce TOMATE avec DEUEVI(PETIT POISSON)': 1775, 'SPAGHETTI sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 1875, 'SPAGHETTI sauce TOMATE avec POULET': 2075, 'SPAGHETTI sauce TOMATE avec BOEUF': 2575, 'SPAGHETTI sauce TOMATE avec MOUTON': 2575, 'SPAGHETTI sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 2075, 'SPAGHETTI sauce TOMATE avec AGLAN(CRABE)': 2075, 'SPAGHETTI sauce TOMATE avec CREVETTE': 2075, 'FOUFOU IGNAME sauce GBOMA avec RIEN ': 3625, 'FOUFOU IGNAME sauce GBOMA avec AKPALAN(POISSON FUME)': 4125, 'FOUFOU IGNAME sauce GBOMA avec DEUEVI(PETIT POISSON)': 3825, 'FOUFOU IGNAME sauce GBOMA avec APKALAN KANAMI(POISSON FRIT)': 3925, 'FOUFOU IGNAME sauce GBOMA avec POULET': 4125, 'FOUFOU IGNAME sauce GBOMA avec BOEUF': 4625, 'FOUFOU IGNAME sauce GBOMA avec MOUTON': 4625, 'FOUFOU IGNAME sauce GBOMA avec AKPAMA(PEAU DE BOEUF)': 4125, 'FOUFOU IGNAME sauce GBOMA avec AGLAN(CRABE)': 4125, 'FOUFOU IGNAME sauce GBOMA avec CREVETTE': 4125, 'FOUFOU IGNAME sauce TOMATE avec RIEN ': 3325, 'FOUFOU IGNAME sauce TOMATE avec AKPALAN(POISSON FUME)': 3825, 'FOUFOU IGNAME sauce TOMATE avec DEUEVI(PETIT POISSON)': 3525, 'FOUFOU IGNAME sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 3625, 'FOUFOU IGNAME sauce TOMATE avec POULET': 3825, 'FOUFOU IGNAME sauce TOMATE avec BOEUF': 4325, 'FOUFOU IGNAME sauce TOMATE avec MOUTON': 4325, 'FOUFOU IGNAME sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 3825, 'FOUFOU IGNAME sauce TOMATE avec AGLAN(CRABE)': 3825, 'FOUFOU IGNAME sauce TOMATE avec CREVETTE': 3825, 'FOUFOU IGNAME sauce GOUSSI avec RIEN ': 3325, 'FOUFOU IGNAME sauce GOUSSI avec AKPALAN(POISSON FUME)': 3825, 'FOUFOU IGNAME sauce GOUSSI avec DEUEVI(PETIT POISSON)': 3525, 'FOUFOU IGNAME sauce GOUSSI avec APKALAN KANAMI(POISSON FRIT)': 3625, 'FOUFOU IGNAME sauce GOUSSI avec POULET': 3825, 'FOUFOU IGNAME sauce GOUSSI avec BOEUF': 4325, 'FOUFOU IGNAME sauce GOUSSI avec MOUTON': 4325, 'FOUFOU IGNAME sauce GOUSSI avec AKPAMA(PEAU DE BOEUF)': 3825, 'FOUFOU IGNAME sauce GOUSSI avec AGLAN(CRABE)': 3825, 'FOUFOU IGNAME sauce GOUSSI avec CREVETTE': 3825, 'FOUFOU IGNAME sauce ADEME avec RIEN ': 3125, 'FOUFOU IGNAME sauce ADEME avec AKPALAN(POISSON FUME)': 3625, 'FOUFOU IGNAME sauce ADEME avec DEUEVI(PETIT POISSON)': 3325, 'FOUFOU IGNAME sauce ADEME avec APKALAN KANAMI(POISSON FRIT)': 3425, 'FOUFOU IGNAME sauce ADEME avec POULET': 3625, 'FOUFOU IGNAME sauce ADEME avec BOEUF': 4125, 'FOUFOU IGNAME sauce ADEME avec MOUTON': 4125, 'FOUFOU IGNAME sauce ADEME avec AKPAMA(PEAU DE BOEUF)': 3625, 'FOUFOU IGNAME sauce ADEME avec AGLAN(CRABE)': 3625, 'FOUFOU IGNAME sauce ADEME avec CREVETTE': 3625, 'FOUFOU IGNAME sauce FETRI(GOMBO) avec RIEN ': 2825, 'FOUFOU IGNAME sauce FETRI(GOMBO) avec AKPALAN(POISSON FUME)': 3325, 'FOUFOU IGNAME sauce FETRI(GOMBO) avec DEUEVI(PETIT POISSON)': 3025, 'FOUFOU IGNAME sauce FETRI(GOMBO) avec APKALAN KANAMI(POISSON FRIT)': 3125, 'FOUFOU IGNAME sauce FETRI(GOMBO) avec POULET': 3325, 'FOUFOU IGNAME sauce FETRI(GOMBO) avec BOEUF': 3825, 'FOUFOU IGNAME sauce FETRI(GOMBO) avec MOUTON': 3825, 'FOUFOU IGNAME sauce FETRI(GOMBO) avec AKPAMA(PEAU DE BOEUF)': 3325, 'FOUFOU IGNAME sauce FETRI(GOMBO) avec AGLAN(CRABE)': 3325, 'FOUFOU IGNAME sauce FETRI(GOMBO) avec CREVETTE': 3325, 'FOUFOU IGNAME sauce KODORO avec RIEN ': 2925, 'FOUFOU IGNAME sauce KODORO avec AKPALAN(POISSON FUME)': 3425, 'FOUFOU IGNAME sauce KODORO avec DEUEVI(PETIT POISSON)': 3125, 'FOUFOU IGNAME sauce KODORO avec APKALAN KANAMI(POISSON FRIT)': 3225, 'FOUFOU IGNAME sauce KODORO avec POULET': 3425, 'FOUFOU IGNAME sauce KODORO avec BOEUF': 3925, 'FOUFOU IGNAME sauce KODORO avec MOUTON': 3925, 'FOUFOU IGNAME sauce KODORO avec AKPAMA(PEAU DE BOEUF)': 3425, 'FOUFOU IGNAME sauce KODORO avec AGLAN(CRABE)': 3425, 'FOUFOU IGNAME sauce KODORO avec CREVETTE': 3425, 'FOUFOU IGNAME sauce GNATOU avec RIEN ': 3225, 'FOUFOU IGNAME sauce GNATOU avec AKPALAN(POISSON FUME)': 3725, 'FOUFOU IGNAME sauce GNATOU avec DEUEVI(PETIT POISSON)': 3425, 'FOUFOU IGNAME sauce GNATOU avec APKALAN KANAMI(POISSON FRIT)': 3525, 'FOUFOU IGNAME sauce GNATOU avec POULET': 3725, 'FOUFOU IGNAME sauce GNATOU avec BOEUF': 4225, 'FOUFOU IGNAME sauce GNATOU avec MOUTON': 4225, 'FOUFOU IGNAME sauce GNATOU avec AKPAMA(PEAU DE BOEUF)': 3725, 'FOUFOU IGNAME sauce GNATOU avec AGLAN(CRABE)': 3725, 'FOUFOU IGNAME sauce GNATOU avec CREVETTE': 3725, 'FOUFOU IGNAME sauce ARACHIDE avec RIEN ': 3175, 'FOUFOU IGNAME sauce ARACHIDE avec AKPALAN(POISSON FUME)': 3675, 'FOUFOU IGNAME sauce ARACHIDE avec DEUEVI(PETIT POISSON)': 3375, 'FOUFOU IGNAME sauce ARACHIDE avec APKALAN KANAMI(POISSON FRIT)': 3475, 'FOUFOU IGNAME sauce ARACHIDE avec POULET': 3675, 'FOUFOU IGNAME sauce ARACHIDE avec BOEUF': 4175, 'FOUFOU IGNAME sauce ARACHIDE avec MOUTON': 4175, 'FOUFOU IGNAME sauce ARACHIDE avec AKPAMA(PEAU DE BOEUF)': 3675, 'FOUFOU IGNAME sauce ARACHIDE avec AGLAN(CRABE)': 3675, 'FOUFOU IGNAME sauce ARACHIDE avec CREVETTE': 3675, 'FOUFOU IGNAME sauce CHOU avec RIEN ': 3725, 'FOUFOU IGNAME sauce CHOU avec AKPALAN(POISSON FUME)': 4225, 'FOUFOU IGNAME sauce CHOU avec DEUEVI(PETIT POISSON)': 3925, 'FOUFOU IGNAME sauce CHOU avec APKALAN KANAMI(POISSON FRIT)': 4025, 'FOUFOU IGNAME sauce CHOU avec POULET': 4225, 'FOUFOU IGNAME sauce CHOU avec BOEUF': 4725, 'FOUFOU IGNAME sauce CHOU avec MOUTON': 4725, 'FOUFOU IGNAME sauce CHOU avec AKPAMA(PEAU DE BOEUF)': 4225, 'FOUFOU IGNAME sauce CHOU avec AGLAN(CRABE)': 4225, 'FOUFOU IGNAME sauce CHOU avec CREVETTE': 4225, 'FOUFOU IGNAME sauce FETRI POUPOU(GONBO SEC) avec RIEN ': 2975, 'FOUFOU IGNAME sauce FETRI POUPOU(GONBO SEC) avec AKPALAN(POISSON FUME)': 3475, 'FOUFOU IGNAME sauce FETRI POUPOU(GONBO SEC) avec DEUEVI(PETIT POISSON)': 3175, 'FOUFOU IGNAME sauce FETRI POUPOU(GONBO SEC) avec APKALAN KANAMI(POISSON FRIT)': 3275, 'FOUFOU IGNAME sauce FETRI POUPOU(GONBO SEC) avec POULET': 3475, 'FOUFOU IGNAME sauce FETRI POUPOU(GONBO SEC) avec BOEUF': 3975, 'FOUFOU IGNAME sauce FETRI POUPOU(GONBO SEC) avec MOUTON': 3975, 'FOUFOU IGNAME sauce FETRI POUPOU(GONBO SEC) avec AKPAMA(PEAU DE BOEUF)': 3475, 'FOUFOU IGNAME sauce FETRI POUPOU(GONBO SEC) avec AGLAN(CRABE)': 3475, 'FOUFOU IGNAME sauce FETRI POUPOU(GONBO SEC) avec CREVETTE': 3475, 'FOUFOU IGNAME sauce DEKOU(GRAINE) avec RIEN ': 3625, 'FOUFOU IGNAME sauce DEKOU(GRAINE) avec AKPALAN(POISSON FUME)': 4125, 'FOUFOU IGNAME sauce DEKOU(GRAINE) avec DEUEVI(PETIT POISSON)': 3825, 'FOUFOU IGNAME sauce DEKOU(GRAINE) avec APKALAN KANAMI(POISSON FRIT)': 3925, 'FOUFOU IGNAME sauce DEKOU(GRAINE) avec POULET': 4125, 'FOUFOU IGNAME sauce DEKOU(GRAINE) avec BOEUF': 4625, 'FOUFOU IGNAME sauce DEKOU(GRAINE) avec MOUTON': 4625, 'FOUFOU IGNAME sauce DEKOU(GRAINE) avec AKPAMA(PEAU DE BOEUF)': 4125, 'FOUFOU IGNAME sauce DEKOU(GRAINE) avec AGLAN(CRABE)': 4125, 'FOUFOU IGNAME sauce DEKOU(GRAINE) avec CREVETTE': 4125, 'FOUFOU IGNAME sauce EBESSESSI avec RIEN ': 2675, 'FOUFOU IGNAME sauce EBESSESSI avec AKPALAN(POISSON FUME)': 3175, 'FOUFOU IGNAME sauce EBESSESSI avec DEUEVI(PETIT POISSON)': 2875, 'FOUFOU IGNAME sauce EBESSESSI avec APKALAN KANAMI(POISSON FRIT)': 2975, 'FOUFOU IGNAME sauce EBESSESSI avec POULET': 3175, 'FOUFOU IGNAME sauce EBESSESSI avec BOEUF': 3675, 'FOUFOU IGNAME sauce EBESSESSI avec MOUTON': 3675, 'FOUFOU IGNAME sauce EBESSESSI avec AKPAMA(PEAU DE BOEUF)': 3175, 'FOUFOU IGNAME sauce EBESSESSI avec AGLAN(CRABE)': 3175, 'FOUFOU IGNAME sauce EBESSESSI avec CREVETTE': 3175, 'FOUFOU PLANTAIN sauce GBOMA avec RIEN ': 2625, 'FOUFOU PLANTAIN sauce GBOMA avec AKPALAN(POISSON FUME)': 3125, 'FOUFOU PLANTAIN sauce GBOMA avec DEUEVI(PETIT POISSON)': 2825, 'FOUFOU PLANTAIN sauce GBOMA avec APKALAN KANAMI(POISSON FRIT)': 2925, 'FOUFOU PLANTAIN sauce GBOMA avec POULET': 3125, 'FOUFOU PLANTAIN sauce GBOMA avec BOEUF': 3625, 'FOUFOU PLANTAIN sauce GBOMA avec MOUTON': 3625, 'FOUFOU PLANTAIN sauce GBOMA avec AKPAMA(PEAU DE BOEUF)': 3125, 'FOUFOU PLANTAIN sauce GBOMA avec AGLAN(CRABE)': 3125, 'FOUFOU PLANTAIN sauce GBOMA avec CREVETTE': 3125, 'FOUFOU PLANTAIN sauce TOMATE avec RIEN ': 2325, 'FOUFOU PLANTAIN sauce TOMATE avec AKPALAN(POISSON FUME)': 2825, 'FOUFOU PLANTAIN sauce TOMATE avec DEUEVI(PETIT POISSON)': 2525, 'FOUFOU PLANTAIN sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 2625, 'FOUFOU PLANTAIN sauce TOMATE avec POULET': 2825, 'FOUFOU PLANTAIN sauce TOMATE avec BOEUF': 3325, 'FOUFOU PLANTAIN sauce TOMATE avec MOUTON': 3325, 'FOUFOU PLANTAIN sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 2825, 'FOUFOU PLANTAIN sauce TOMATE avec AGLAN(CRABE)': 2825, 'FOUFOU PLANTAIN sauce TOMATE avec CREVETTE': 2825, 'FOUFOU PLANTAIN sauce GOUSSI avec RIEN ': 2325, 'FOUFOU PLANTAIN sauce GOUSSI avec AKPALAN(POISSON FUME)': 2825, 'FOUFOU PLANTAIN sauce GOUSSI avec DEUEVI(PETIT POISSON)': 2525, 'FOUFOU PLANTAIN sauce GOUSSI avec APKALAN KANAMI(POISSON FRIT)': 2625, 'FOUFOU PLANTAIN sauce GOUSSI avec POULET': 2825, 'FOUFOU PLANTAIN sauce GOUSSI avec BOEUF': 3325, 'FOUFOU PLANTAIN sauce GOUSSI avec MOUTON': 3325, 'FOUFOU PLANTAIN sauce GOUSSI avec AKPAMA(PEAU DE BOEUF)': 2825, 'FOUFOU PLANTAIN sauce GOUSSI avec AGLAN(CRABE)': 2825, 'FOUFOU PLANTAIN sauce GOUSSI avec CREVETTE': 2825, 'FOUFOU PLANTAIN sauce ADEME avec RIEN ': 2125, 'FOUFOU PLANTAIN sauce ADEME avec AKPALAN(POISSON FUME)': 2625, 'FOUFOU PLANTAIN sauce ADEME avec DEUEVI(PETIT POISSON)': 2325, 'FOUFOU PLANTAIN sauce ADEME avec APKALAN KANAMI(POISSON FRIT)': 2425, 'FOUFOU PLANTAIN sauce ADEME avec POULET': 2625, 'FOUFOU PLANTAIN sauce ADEME avec BOEUF': 3125, 'FOUFOU PLANTAIN sauce ADEME avec MOUTON': 3125, 'FOUFOU PLANTAIN sauce ADEME avec AKPAMA(PEAU DE BOEUF)': 2625, 'FOUFOU PLANTAIN sauce ADEME avec AGLAN(CRABE)': 2625, 'FOUFOU PLANTAIN sauce ADEME avec CREVETTE': 2625, 'FOUFOU PLANTAIN sauce FETRI(GOMBO) avec RIEN ': 1825, 'FOUFOU PLANTAIN sauce FETRI(GOMBO) avec AKPALAN(POISSON FUME)': 2325, 'FOUFOU PLANTAIN sauce FETRI(GOMBO) avec DEUEVI(PETIT POISSON)': 2025, 'FOUFOU PLANTAIN sauce FETRI(GOMBO) avec APKALAN KANAMI(POISSON FRIT)': 2125, 'FOUFOU PLANTAIN sauce FETRI(GOMBO) avec POULET': 2325, 'FOUFOU PLANTAIN sauce FETRI(GOMBO) avec BOEUF': 2825, 'FOUFOU PLANTAIN sauce FETRI(GOMBO) avec MOUTON': 2825, 'FOUFOU PLANTAIN sauce FETRI(GOMBO) avec AKPAMA(PEAU DE BOEUF)': 2325, 'FOUFOU PLANTAIN sauce FETRI(GOMBO) avec AGLAN(CRABE)': 2325, 'FOUFOU PLANTAIN sauce FETRI(GOMBO) avec CREVETTE': 2325, 'FOUFOU PLANTAIN sauce KODORO avec RIEN ': 1925, 'FOUFOU PLANTAIN sauce KODORO avec AKPALAN(POISSON FUME)': 2425, 'FOUFOU PLANTAIN sauce KODORO avec DEUEVI(PETIT POISSON)': 2125, 'FOUFOU PLANTAIN sauce KODORO avec APKALAN KANAMI(POISSON FRIT)': 2225, 'FOUFOU PLANTAIN sauce KODORO avec POULET': 2425, 'FOUFOU PLANTAIN sauce KODORO avec BOEUF': 2925, 'FOUFOU PLANTAIN sauce KODORO avec MOUTON': 2925, 'FOUFOU PLANTAIN sauce KODORO avec AKPAMA(PEAU DE BOEUF)': 2425, 'FOUFOU PLANTAIN sauce KODORO avec AGLAN(CRABE)': 2425, 'FOUFOU PLANTAIN sauce KODORO avec CREVETTE': 2425, 'FOUFOU PLANTAIN sauce GNATOU avec RIEN ': 2225, 'FOUFOU PLANTAIN sauce GNATOU avec AKPALAN(POISSON FUME)': 2725, 'FOUFOU PLANTAIN sauce GNATOU avec DEUEVI(PETIT POISSON)': 2425, 'FOUFOU PLANTAIN sauce GNATOU avec APKALAN KANAMI(POISSON FRIT)': 2525, 'FOUFOU PLANTAIN sauce GNATOU avec POULET': 2725, 'FOUFOU PLANTAIN sauce GNATOU avec BOEUF': 3225, 'FOUFOU PLANTAIN sauce GNATOU avec MOUTON': 3225, 'FOUFOU PLANTAIN sauce GNATOU avec AKPAMA(PEAU DE BOEUF)': 2725, 'FOUFOU PLANTAIN sauce GNATOU avec AGLAN(CRABE)': 2725, 'FOUFOU PLANTAIN sauce GNATOU avec CREVETTE': 2725, 'FOUFOU PLANTAIN sauce ARACHIDE avec RIEN ': 2175, 'FOUFOU PLANTAIN sauce ARACHIDE avec AKPALAN(POISSON FUME)': 2675, 'FOUFOU PLANTAIN sauce ARACHIDE avec DEUEVI(PETIT POISSON)': 2375, 'FOUFOU PLANTAIN sauce ARACHIDE avec APKALAN KANAMI(POISSON FRIT)': 2475, 'FOUFOU PLANTAIN sauce ARACHIDE avec POULET': 2675, 'FOUFOU PLANTAIN sauce ARACHIDE avec BOEUF': 3175, 'FOUFOU PLANTAIN sauce ARACHIDE avec MOUTON': 3175, 'FOUFOU PLANTAIN sauce ARACHIDE avec AKPAMA(PEAU DE BOEUF)': 2675, 'FOUFOU PLANTAIN sauce ARACHIDE avec AGLAN(CRABE)': 2675, 'FOUFOU PLANTAIN sauce ARACHIDE avec CREVETTE': 2675, 'FOUFOU PLANTAIN sauce CHOU avec RIEN ': 2725, 'FOUFOU PLANTAIN sauce CHOU avec AKPALAN(POISSON FUME)': 3225, 'FOUFOU PLANTAIN sauce CHOU avec DEUEVI(PETIT POISSON)': 2925, 'FOUFOU PLANTAIN sauce CHOU avec APKALAN KANAMI(POISSON FRIT)': 3025, 'FOUFOU PLANTAIN sauce CHOU avec POULET': 3225, 'FOUFOU PLANTAIN sauce CHOU avec BOEUF': 3725, 'FOUFOU PLANTAIN sauce CHOU avec MOUTON': 3725, 'FOUFOU PLANTAIN sauce CHOU avec AKPAMA(PEAU DE BOEUF)': 3225, 'FOUFOU PLANTAIN sauce CHOU avec AGLAN(CRABE)': 3225, 'FOUFOU PLANTAIN sauce CHOU avec CREVETTE': 3225, 'FOUFOU PLANTAIN sauce FETRI POUPOU(GONBO SEC) avec RIEN ': 1975, 'FOUFOU PLANTAIN sauce FETRI POUPOU(GONBO SEC) avec AKPALAN(POISSON FUME)': 2475, 'FOUFOU PLANTAIN sauce FETRI POUPOU(GONBO SEC) avec DEUEVI(PETIT POISSON)': 2175, 'FOUFOU PLANTAIN sauce FETRI POUPOU(GONBO SEC) avec APKALAN KANAMI(POISSON FRIT)': 2275, 'FOUFOU PLANTAIN sauce FETRI POUPOU(GONBO SEC) avec POULET': 2475, 'FOUFOU PLANTAIN sauce FETRI POUPOU(GONBO SEC) avec BOEUF': 2975, 'FOUFOU PLANTAIN sauce FETRI POUPOU(GONBO SEC) avec MOUTON': 2975, 'FOUFOU PLANTAIN sauce FETRI POUPOU(GONBO SEC) avec AKPAMA(PEAU DE BOEUF)': 2475, 'FOUFOU PLANTAIN sauce FETRI POUPOU(GONBO SEC) avec AGLAN(CRABE)': 2475, 'FOUFOU PLANTAIN sauce FETRI POUPOU(GONBO SEC) avec CREVETTE': 2475, 'FOUFOU PLANTAIN sauce DEKOU(GRAINE) avec RIEN ': 2625, 'FOUFOU PLANTAIN sauce DEKOU(GRAINE) avec AKPALAN(POISSON FUME)': 3125, 'FOUFOU PLANTAIN sauce DEKOU(GRAINE) avec DEUEVI(PETIT POISSON)': 2825, 'FOUFOU PLANTAIN sauce DEKOU(GRAINE) avec APKALAN KANAMI(POISSON FRIT)': 2925, 'FOUFOU PLANTAIN sauce DEKOU(GRAINE) avec POULET': 3125, 'FOUFOU PLANTAIN sauce DEKOU(GRAINE) avec BOEUF': 3625, 'FOUFOU PLANTAIN sauce DEKOU(GRAINE) avec MOUTON': 3625, 'FOUFOU PLANTAIN sauce DEKOU(GRAINE) avec AKPAMA(PEAU DE BOEUF)': 3125, 'FOUFOU PLANTAIN sauce DEKOU(GRAINE) avec AGLAN(CRABE)': 3125, 'FOUFOU PLANTAIN sauce DEKOU(GRAINE) avec CREVETTE': 3125, 'FOUFOU PLANTAIN sauce EBESSESSI avec RIEN ': 1675, 'FOUFOU PLANTAIN sauce EBESSESSI avec AKPALAN(POISSON FUME)': 2175, 'FOUFOU PLANTAIN sauce EBESSESSI avec DEUEVI(PETIT POISSON)': 1875, 'FOUFOU PLANTAIN sauce EBESSESSI avec APKALAN KANAMI(POISSON FRIT)': 1975, 'FOUFOU PLANTAIN sauce EBESSESSI avec POULET': 2175, 'FOUFOU PLANTAIN sauce EBESSESSI avec BOEUF': 2675, 'FOUFOU PLANTAIN sauce EBESSESSI avec MOUTON': 2675, 'FOUFOU PLANTAIN sauce EBESSESSI avec AKPAMA(PEAU DE BOEUF)': 2175, 'FOUFOU PLANTAIN sauce EBESSESSI avec AGLAN(CRABE)': 2175, 'FOUFOU PLANTAIN sauce EBESSESSI avec CREVETTE': 2175, 'AKOUME(PATE MAIS) sauce GBOMA avec RIEN ': 2500, 'AKOUME(PATE MAIS) sauce GBOMA avec AKPALAN(POISSON FUME)': 3000, 'AKOUME(PATE MAIS) sauce GBOMA avec DEUEVI(PETIT POISSON)': 2700, 'AKOUME(PATE MAIS) sauce GBOMA avec APKALAN KANAMI(POISSON FRIT)': 2800, 'AKOUME(PATE MAIS) sauce GBOMA avec POULET': 3000, 'AKOUME(PATE MAIS) sauce GBOMA avec BOEUF': 3500, 'AKOUME(PATE MAIS) sauce GBOMA avec MOUTON': 3500, 'AKOUME(PATE MAIS) sauce GBOMA avec AKPAMA(PEAU DE BOEUF)': 3000, 'AKOUME(PATE MAIS) sauce GBOMA avec AGLAN(CRABE)': 3000, 'AKOUME(PATE MAIS) sauce GBOMA avec CREVETTE': 3000, 'AKOUME(PATE MAIS) sauce TOMATE avec RIEN ': 2200, 'AKOUME(PATE MAIS) sauce TOMATE avec AKPALAN(POISSON FUME)': 2700, 'AKOUME(PATE MAIS) sauce TOMATE avec DEUEVI(PETIT POISSON)': 2400, 'AKOUME(PATE MAIS) sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 2500, 'AKOUME(PATE MAIS) sauce TOMATE avec POULET': 2700, 'AKOUME(PATE MAIS) sauce TOMATE avec BOEUF': 3200, 'AKOUME(PATE MAIS) sauce TOMATE avec MOUTON': 3200, 'AKOUME(PATE MAIS) sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 2700, 'AKOUME(PATE MAIS) sauce TOMATE avec AGLAN(CRABE)': 2700, 'AKOUME(PATE MAIS) sauce TOMATE avec CREVETTE': 2700, 'AKOUME(PATE MAIS) sauce GOUSSI avec RIEN ': 2200, 'AKOUME(PATE MAIS) sauce GOUSSI avec AKPALAN(POISSON FUME)': 2700, 'AKOUME(PATE MAIS) sauce GOUSSI avec DEUEVI(PETIT POISSON)': 2400, 'AKOUME(PATE MAIS) sauce GOUSSI avec APKALAN KANAMI(POISSON FRIT)': 2500, 'AKOUME(PATE MAIS) sauce GOUSSI avec POULET': 2700, 'AKOUME(PATE MAIS) sauce GOUSSI avec BOEUF': 3200, 'AKOUME(PATE MAIS) sauce GOUSSI avec MOUTON': 3200, 'AKOUME(PATE MAIS) sauce GOUSSI avec AKPAMA(PEAU DE BOEUF)': 2700, 'AKOUME(PATE MAIS) sauce GOUSSI avec AGLAN(CRABE)': 2700, 'AKOUME(PATE MAIS) sauce GOUSSI avec CREVETTE': 2700, 'AKOUME(PATE MAIS) sauce ADEME avec RIEN ': 2000, 'AKOUME(PATE MAIS) sauce ADEME avec AKPALAN(POISSON FUME)': 2500, 'AKOUME(PATE MAIS) sauce ADEME avec DEUEVI(PETIT POISSON)': 2200, 'AKOUME(PATE MAIS) sauce ADEME avec APKALAN KANAMI(POISSON FRIT)': 2300, 'AKOUME(PATE MAIS) sauce ADEME avec POULET': 2500, 'AKOUME(PATE MAIS) sauce ADEME avec BOEUF': 3000, 'AKOUME(PATE MAIS) sauce ADEME avec MOUTON': 3000, 'AKOUME(PATE MAIS) sauce ADEME avec AKPAMA(PEAU DE BOEUF)': 2500, 'AKOUME(PATE MAIS) sauce ADEME avec AGLAN(CRABE)': 2500, 'AKOUME(PATE MAIS) sauce ADEME avec CREVETTE': 2500, 'AKOUME(PATE MAIS) sauce FETRI(GOMBO) avec RIEN ': 1700, 'AKOUME(PATE MAIS) sauce FETRI(GOMBO) avec AKPALAN(POISSON FUME)': 2200, 'AKOUME(PATE MAIS) sauce FETRI(GOMBO) avec DEUEVI(PETIT POISSON)': 1900, 'AKOUME(PATE MAIS) sauce FETRI(GOMBO) avec APKALAN KANAMI(POISSON FRIT)': 2000, 'AKOUME(PATE MAIS) sauce FETRI(GOMBO) avec POULET': 2200, 'AKOUME(PATE MAIS) sauce FETRI(GOMBO) avec BOEUF': 2700, 'AKOUME(PATE MAIS) sauce FETRI(GOMBO) avec MOUTON': 2700, 'AKOUME(PATE MAIS) sauce FETRI(GOMBO) avec AKPAMA(PEAU DE BOEUF)': 2200, 'AKOUME(PATE MAIS) sauce FETRI(GOMBO) avec AGLAN(CRABE)': 2200, 'AKOUME(PATE MAIS) sauce FETRI(GOMBO) avec CREVETTE': 2200, 'AKOUME(PATE MAIS) sauce KODORO avec RIEN ': 1800, 'AKOUME(PATE MAIS) sauce KODORO avec AKPALAN(POISSON FUME)': 2300, 'AKOUME(PATE MAIS) sauce KODORO avec DEUEVI(PETIT POISSON)': 2000, 'AKOUME(PATE MAIS) sauce KODORO avec APKALAN KANAMI(POISSON FRIT)': 2100, 'AKOUME(PATE MAIS) sauce KODORO avec POULET': 2300, 'AKOUME(PATE MAIS) sauce KODORO avec BOEUF': 2800, 'AKOUME(PATE MAIS) sauce KODORO avec MOUTON': 2800, 'AKOUME(PATE MAIS) sauce KODORO avec AKPAMA(PEAU DE BOEUF)': 2300, 'AKOUME(PATE MAIS) sauce KODORO avec AGLAN(CRABE)': 2300, 'AKOUME(PATE MAIS) sauce KODORO avec CREVETTE': 2300, 'AKOUME(PATE MAIS) sauce GNATOU avec RIEN ': 2100, 'AKOUME(PATE MAIS) sauce GNATOU avec AKPALAN(POISSON FUME)': 2600, 'AKOUME(PATE MAIS) sauce GNATOU avec DEUEVI(PETIT POISSON)': 2300, 'AKOUME(PATE MAIS) sauce GNATOU avec APKALAN KANAMI(POISSON FRIT)': 2400, 'AKOUME(PATE MAIS) sauce GNATOU avec POULET': 2600, 'AKOUME(PATE MAIS) sauce GNATOU avec BOEUF': 3100, 'AKOUME(PATE MAIS) sauce GNATOU avec MOUTON': 3100, 'AKOUME(PATE MAIS) sauce GNATOU avec AKPAMA(PEAU DE BOEUF)': 2600, 'AKOUME(PATE MAIS) sauce GNATOU avec AGLAN(CRABE)': 2600, 'AKOUME(PATE MAIS) sauce GNATOU avec CREVETTE': 2600, 'AKOUME(PATE MAIS) sauce ARACHIDE avec RIEN ': 2050, 'AKOUME(PATE MAIS) sauce ARACHIDE avec AKPALAN(POISSON FUME)': 2550, 'AKOUME(PATE MAIS) sauce ARACHIDE avec DEUEVI(PETIT POISSON)': 2250, 'AKOUME(PATE MAIS) sauce ARACHIDE avec APKALAN KANAMI(POISSON FRIT)': 2350, 'AKOUME(PATE MAIS) sauce ARACHIDE avec POULET': 2550, 'AKOUME(PATE MAIS) sauce ARACHIDE avec BOEUF': 3050, 'AKOUME(PATE MAIS) sauce ARACHIDE avec MOUTON': 3050, 'AKOUME(PATE MAIS) sauce ARACHIDE avec AKPAMA(PEAU DE BOEUF)': 2550, 'AKOUME(PATE MAIS) sauce ARACHIDE avec AGLAN(CRABE)': 2550, 'AKOUME(PATE MAIS) sauce ARACHIDE avec CREVETTE': 2550, 'AKOUME(PATE MAIS) sauce CHOU avec RIEN ': 2600, 'AKOUME(PATE MAIS) sauce CHOU avec AKPALAN(POISSON FUME)': 3100, 'AKOUME(PATE MAIS) sauce CHOU avec DEUEVI(PETIT POISSON)': 2800, 'AKOUME(PATE MAIS) sauce CHOU avec APKALAN KANAMI(POISSON FRIT)': 2900, 'AKOUME(PATE MAIS) sauce CHOU avec POULET': 3100, 'AKOUME(PATE MAIS) sauce CHOU avec BOEUF': 3600, 'AKOUME(PATE MAIS) sauce CHOU avec MOUTON': 3600, 'AKOUME(PATE MAIS) sauce CHOU avec AKPAMA(PEAU DE BOEUF)': 3100, 'AKOUME(PATE MAIS) sauce CHOU avec AGLAN(CRABE)': 3100, 'AKOUME(PATE MAIS) sauce CHOU avec CREVETTE': 3100, 'AKOUME(PATE MAIS) sauce FETRI POUPOU(GONBO SEC) avec RIEN ': 1850, 'AKOUME(PATE MAIS) sauce FETRI POUPOU(GONBO SEC) avec AKPALAN(POISSON FUME)': 2350, 'AKOUME(PATE MAIS) sauce FETRI POUPOU(GONBO SEC) avec DEUEVI(PETIT POISSON)': 2050, 'AKOUME(PATE MAIS) sauce FETRI POUPOU(GONBO SEC) avec APKALAN KANAMI(POISSON FRIT)': 2150, 'AKOUME(PATE MAIS) sauce FETRI POUPOU(GONBO SEC) avec POULET': 2350, 'AKOUME(PATE MAIS) sauce FETRI POUPOU(GONBO SEC) avec BOEUF': 2850, 'AKOUME(PATE MAIS) sauce FETRI POUPOU(GONBO SEC) avec MOUTON': 2850, 'AKOUME(PATE MAIS) sauce FETRI POUPOU(GONBO SEC) avec AKPAMA(PEAU DE BOEUF)': 2350, 'AKOUME(PATE MAIS) sauce FETRI POUPOU(GONBO SEC) avec AGLAN(CRABE)': 2350, 'AKOUME(PATE MAIS) sauce FETRI POUPOU(GONBO SEC) avec CREVETTE': 2350, 'AKOUME(PATE MAIS) sauce DEKOU(GRAINE) avec RIEN ': 2500, 'AKOUME(PATE MAIS) sauce DEKOU(GRAINE) avec AKPALAN(POISSON FUME)': 3000, 'AKOUME(PATE MAIS) sauce DEKOU(GRAINE) avec DEUEVI(PETIT POISSON)': 2700, 'AKOUME(PATE MAIS) sauce DEKOU(GRAINE) avec APKALAN KANAMI(POISSON FRIT)': 2800, 'AKOUME(PATE MAIS) sauce DEKOU(GRAINE) avec POULET': 3000, 'AKOUME(PATE MAIS) sauce DEKOU(GRAINE) avec BOEUF': 3500, 'AKOUME(PATE MAIS) sauce DEKOU(GRAINE) avec MOUTON': 3500, 'AKOUME(PATE MAIS) sauce DEKOU(GRAINE) avec AKPAMA(PEAU DE BOEUF)': 3000, 'AKOUME(PATE MAIS) sauce DEKOU(GRAINE) avec AGLAN(CRABE)': 3000, 'AKOUME(PATE MAIS) sauce DEKOU(GRAINE) avec CREVETTE': 3000, 'AKOUME(PATE MAIS) sauce EBESSESSI avec RIEN ': 1550, 'AKOUME(PATE MAIS) sauce EBESSESSI avec AKPALAN(POISSON FUME)': 2050, 'AKOUME(PATE MAIS) sauce EBESSESSI avec DEUEVI(PETIT POISSON)': 1750, 'AKOUME(PATE MAIS) sauce EBESSESSI avec APKALAN KANAMI(POISSON FRIT)': 1850, 'AKOUME(PATE MAIS) sauce EBESSESSI avec POULET': 2050, 'AKOUME(PATE MAIS) sauce EBESSESSI avec BOEUF': 2550, 'AKOUME(PATE MAIS) sauce EBESSESSI avec MOUTON': 2550, 'AKOUME(PATE MAIS) sauce EBESSESSI avec AKPAMA(PEAU DE BOEUF)': 2050, 'AKOUME(PATE MAIS) sauce EBESSESSI avec AGLAN(CRABE)': 2050, 'AKOUME(PATE MAIS) sauce EBESSESSI avec CREVETTE': 2050, 'EMAKUME(PATE MAIS FERMENTE) sauce GBOMA avec RIEN ': 2700, 'EMAKUME(PATE MAIS FERMENTE) sauce GBOMA avec AKPALAN(POISSON FUME)': 3200, 'EMAKUME(PATE MAIS FERMENTE) sauce GBOMA avec DEUEVI(PETIT POISSON)': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce GBOMA avec APKALAN KANAMI(POISSON FRIT)': 3000, 'EMAKUME(PATE MAIS FERMENTE) sauce GBOMA avec POULET': 3200, 'EMAKUME(PATE MAIS FERMENTE) sauce GBOMA avec BOEUF': 3700, 'EMAKUME(PATE MAIS FERMENTE) sauce GBOMA avec MOUTON': 3700, 'EMAKUME(PATE MAIS FERMENTE) sauce GBOMA avec AKPAMA(PEAU DE BOEUF)': 3200, 'EMAKUME(PATE MAIS FERMENTE) sauce GBOMA avec AGLAN(CRABE)': 3200, 'EMAKUME(PATE MAIS FERMENTE) sauce GBOMA avec CREVETTE': 3200, 'EMAKUME(PATE MAIS FERMENTE) sauce TOMATE avec RIEN ': 2400, 'EMAKUME(PATE MAIS FERMENTE) sauce TOMATE avec AKPALAN(POISSON FUME)': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce TOMATE avec DEUEVI(PETIT POISSON)': 2600, 'EMAKUME(PATE MAIS FERMENTE) sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 2700, 'EMAKUME(PATE MAIS FERMENTE) sauce TOMATE avec POULET': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce TOMATE avec BOEUF': 3400, 'EMAKUME(PATE MAIS FERMENTE) sauce TOMATE avec MOUTON': 3400, 'EMAKUME(PATE MAIS FERMENTE) sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce TOMATE avec AGLAN(CRABE)': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce TOMATE avec CREVETTE': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce GOUSSI avec RIEN ': 2400, 'EMAKUME(PATE MAIS FERMENTE) sauce GOUSSI avec AKPALAN(POISSON FUME)': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce GOUSSI avec DEUEVI(PETIT POISSON)': 2600, 'EMAKUME(PATE MAIS FERMENTE) sauce GOUSSI avec APKALAN KANAMI(POISSON FRIT)': 2700, 'EMAKUME(PATE MAIS FERMENTE) sauce GOUSSI avec POULET': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce GOUSSI avec BOEUF': 3400, 'EMAKUME(PATE MAIS FERMENTE) sauce GOUSSI avec MOUTON': 3400, 'EMAKUME(PATE MAIS FERMENTE) sauce GOUSSI avec AKPAMA(PEAU DE BOEUF)': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce GOUSSI avec AGLAN(CRABE)': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce GOUSSI avec CREVETTE': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce ADEME avec RIEN ': 2200, 'EMAKUME(PATE MAIS FERMENTE) sauce ADEME avec AKPALAN(POISSON FUME)': 2700, 'EMAKUME(PATE MAIS FERMENTE) sauce ADEME avec DEUEVI(PETIT POISSON)': 2400, 'EMAKUME(PATE MAIS FERMENTE) sauce ADEME avec APKALAN KANAMI(POISSON FRIT)': 2500, 'EMAKUME(PATE MAIS FERMENTE) sauce ADEME avec POULET': 2700, 'EMAKUME(PATE MAIS FERMENTE) sauce ADEME avec BOEUF': 3200, 'EMAKUME(PATE MAIS FERMENTE) sauce ADEME avec MOUTON': 3200, 'EMAKUME(PATE MAIS FERMENTE) sauce ADEME avec AKPAMA(PEAU DE BOEUF)': 2700, 'EMAKUME(PATE MAIS FERMENTE) sauce ADEME avec AGLAN(CRABE)': 2700, 'EMAKUME(PATE MAIS FERMENTE) sauce ADEME avec CREVETTE': 2700, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI(GOMBO) avec RIEN ': 1900, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI(GOMBO) avec AKPALAN(POISSON FUME)': 2400, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI(GOMBO) avec DEUEVI(PETIT POISSON)': 2100, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI(GOMBO) avec APKALAN KANAMI(POISSON FRIT)': 2200, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI(GOMBO) avec POULET': 2400, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI(GOMBO) avec BOEUF': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI(GOMBO) avec MOUTON': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI(GOMBO) avec AKPAMA(PEAU DE BOEUF)': 2400, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI(GOMBO) avec AGLAN(CRABE)': 2400, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI(GOMBO) avec CREVETTE': 2400, 'EMAKUME(PATE MAIS FERMENTE) sauce KODORO avec RIEN ': 2000, 'EMAKUME(PATE MAIS FERMENTE) sauce KODORO avec AKPALAN(POISSON FUME)': 2500, 'EMAKUME(PATE MAIS FERMENTE) sauce KODORO avec DEUEVI(PETIT POISSON)': 2200, 'EMAKUME(PATE MAIS FERMENTE) sauce KODORO avec APKALAN KANAMI(POISSON FRIT)': 2300, 'EMAKUME(PATE MAIS FERMENTE) sauce KODORO avec POULET': 2500, 'EMAKUME(PATE MAIS FERMENTE) sauce KODORO avec BOEUF': 3000, 'EMAKUME(PATE MAIS FERMENTE) sauce KODORO avec MOUTON': 3000, 'EMAKUME(PATE MAIS FERMENTE) sauce KODORO avec AKPAMA(PEAU DE BOEUF)': 2500, 'EMAKUME(PATE MAIS FERMENTE) sauce KODORO avec AGLAN(CRABE)': 2500, 'EMAKUME(PATE MAIS FERMENTE) sauce KODORO avec CREVETTE': 2500, 'EMAKUME(PATE MAIS FERMENTE) sauce GNATOU avec RIEN ': 2300, 'EMAKUME(PATE MAIS FERMENTE) sauce GNATOU avec AKPALAN(POISSON FUME)': 2800, 'EMAKUME(PATE MAIS FERMENTE) sauce GNATOU avec DEUEVI(PETIT POISSON)': 2500, 'EMAKUME(PATE MAIS FERMENTE) sauce GNATOU avec APKALAN KANAMI(POISSON FRIT)': 2600, 'EMAKUME(PATE MAIS FERMENTE) sauce GNATOU avec POULET': 2800, 'EMAKUME(PATE MAIS FERMENTE) sauce GNATOU avec BOEUF': 3300, 'EMAKUME(PATE MAIS FERMENTE) sauce GNATOU avec MOUTON': 3300, 'EMAKUME(PATE MAIS FERMENTE) sauce GNATOU avec AKPAMA(PEAU DE BOEUF)': 2800, 'EMAKUME(PATE MAIS FERMENTE) sauce GNATOU avec AGLAN(CRABE)': 2800, 'EMAKUME(PATE MAIS FERMENTE) sauce GNATOU avec CREVETTE': 2800, 'EMAKUME(PATE MAIS FERMENTE) sauce ARACHIDE avec RIEN ': 2250, 'EMAKUME(PATE MAIS FERMENTE) sauce ARACHIDE avec AKPALAN(POISSON FUME)': 2750, 'EMAKUME(PATE MAIS FERMENTE) sauce ARACHIDE avec DEUEVI(PETIT POISSON)': 2450, 'EMAKUME(PATE MAIS FERMENTE) sauce ARACHIDE avec APKALAN KANAMI(POISSON FRIT)': 2550, 'EMAKUME(PATE MAIS FERMENTE) sauce ARACHIDE avec POULET': 2750, 'EMAKUME(PATE MAIS FERMENTE) sauce ARACHIDE avec BOEUF': 3250, 'EMAKUME(PATE MAIS FERMENTE) sauce ARACHIDE avec MOUTON': 3250, 'EMAKUME(PATE MAIS FERMENTE) sauce ARACHIDE avec AKPAMA(PEAU DE BOEUF)': 2750, 'EMAKUME(PATE MAIS FERMENTE) sauce ARACHIDE avec AGLAN(CRABE)': 2750, 'EMAKUME(PATE MAIS FERMENTE) sauce ARACHIDE avec CREVETTE': 2750, 'EMAKUME(PATE MAIS FERMENTE) sauce CHOU avec RIEN ': 2800, 'EMAKUME(PATE MAIS FERMENTE) sauce CHOU avec AKPALAN(POISSON FUME)': 3300, 'EMAKUME(PATE MAIS FERMENTE) sauce CHOU avec DEUEVI(PETIT POISSON)': 3000, 'EMAKUME(PATE MAIS FERMENTE) sauce CHOU avec APKALAN KANAMI(POISSON FRIT)': 3100, 'EMAKUME(PATE MAIS FERMENTE) sauce CHOU avec POULET': 3300, 'EMAKUME(PATE MAIS FERMENTE) sauce CHOU avec BOEUF': 3800, 'EMAKUME(PATE MAIS FERMENTE) sauce CHOU avec MOUTON': 3800, 'EMAKUME(PATE MAIS FERMENTE) sauce CHOU avec AKPAMA(PEAU DE BOEUF)': 3300, 'EMAKUME(PATE MAIS FERMENTE) sauce CHOU avec AGLAN(CRABE)': 3300, 'EMAKUME(PATE MAIS FERMENTE) sauce CHOU avec CREVETTE': 3300, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI POUPOU(GONBO SEC) avec RIEN ': 2050, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI POUPOU(GONBO SEC) avec AKPALAN(POISSON FUME)': 2550, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI POUPOU(GONBO SEC) avec DEUEVI(PETIT POISSON)': 2250, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI POUPOU(GONBO SEC) avec APKALAN KANAMI(POISSON FRIT)': 2350, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI POUPOU(GONBO SEC) avec POULET': 2550, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI POUPOU(GONBO SEC) avec BOEUF': 3050, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI POUPOU(GONBO SEC) avec MOUTON': 3050, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI POUPOU(GONBO SEC) avec AKPAMA(PEAU DE BOEUF)': 2550, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI POUPOU(GONBO SEC) avec AGLAN(CRABE)': 2550, 'EMAKUME(PATE MAIS FERMENTE) sauce FETRI POUPOU(GONBO SEC) avec CREVETTE': 2550, 'EMAKUME(PATE MAIS FERMENTE) sauce DEKOU(GRAINE) avec RIEN ': 2700, 'EMAKUME(PATE MAIS FERMENTE) sauce DEKOU(GRAINE) avec AKPALAN(POISSON FUME)': 3200, 'EMAKUME(PATE MAIS FERMENTE) sauce DEKOU(GRAINE) avec DEUEVI(PETIT POISSON)': 2900, 'EMAKUME(PATE MAIS FERMENTE) sauce DEKOU(GRAINE) avec APKALAN KANAMI(POISSON FRIT)': 3000, 'EMAKUME(PATE MAIS FERMENTE) sauce DEKOU(GRAINE) avec POULET': 3200, 'EMAKUME(PATE MAIS FERMENTE) sauce DEKOU(GRAINE) avec BOEUF': 3700, 'EMAKUME(PATE MAIS FERMENTE) sauce DEKOU(GRAINE) avec MOUTON': 3700, 'EMAKUME(PATE MAIS FERMENTE) sauce DEKOU(GRAINE) avec AKPAMA(PEAU DE BOEUF)': 3200, 'EMAKUME(PATE MAIS FERMENTE) sauce DEKOU(GRAINE) avec AGLAN(CRABE)': 3200, 'EMAKUME(PATE MAIS FERMENTE) sauce DEKOU(GRAINE) avec CREVETTE': 3200, 'EMAKUME(PATE MAIS FERMENTE) sauce EBESSESSI avec RIEN ': 1750, 'EMAKUME(PATE MAIS FERMENTE) sauce EBESSESSI avec AKPALAN(POISSON FUME)': 2250, 'EMAKUME(PATE MAIS FERMENTE) sauce EBESSESSI avec DEUEVI(PETIT POISSON)': 1950, 'EMAKUME(PATE MAIS FERMENTE) sauce EBESSESSI avec APKALAN KANAMI(POISSON FRIT)': 2050, 'EMAKUME(PATE MAIS FERMENTE) sauce EBESSESSI avec POULET': 2250, 'EMAKUME(PATE MAIS FERMENTE) sauce EBESSESSI avec BOEUF': 2750, 'EMAKUME(PATE MAIS FERMENTE) sauce EBESSESSI avec MOUTON': 2750, 'EMAKUME(PATE MAIS FERMENTE) sauce EBESSESSI avec AKPAMA(PEAU DE BOEUF)': 2250, 'EMAKUME(PATE MAIS FERMENTE) sauce EBESSESSI avec AGLAN(CRABE)': 2250, 'EMAKUME(PATE MAIS FERMENTE) sauce EBESSESSI avec CREVETTE': 2250, 'Riz sauce GBOMA avec RIEN ': 2375, 'Riz sauce GBOMA avec AKPALAN(POISSON FUME)': 2875, 'Riz sauce GBOMA avec DEUEVI(PETIT POISSON)': 2575, 'Riz sauce GBOMA avec APKALAN KANAMI(POISSON FRIT)': 2675, 'Riz sauce GBOMA avec POULET': 2875, 'Riz sauce GBOMA avec BOEUF': 3375, 'Riz sauce GBOMA avec MOUTON': 3375, 'Riz sauce GBOMA avec AKPAMA(PEAU DE BOEUF)': 2875, 'Riz sauce GBOMA avec AGLAN(CRABE)': 2875, 'Riz sauce GBOMA avec CREVETTE': 2875, 'Riz sauce TOMATE avec RIEN ': 2075, 'Riz sauce TOMATE avec AKPALAN(POISSON FUME)': 2575, 'Riz sauce TOMATE avec DEUEVI(PETIT POISSON)': 2275, 'Riz sauce TOMATE avec APKALAN KANAMI(POISSON FRIT)': 2375, 'Riz sauce TOMATE avec POULET': 2575, 'Riz sauce TOMATE avec BOEUF': 3075, 'Riz sauce TOMATE avec MOUTON': 3075, 'Riz sauce TOMATE avec AKPAMA(PEAU DE BOEUF)': 2575, 'Riz sauce TOMATE avec AGLAN(CRABE)': 2575, 'Riz sauce TOMATE avec CREVETTE': 2575, 'Riz sauce GOUSSI avec RIEN ': 2075, 'Riz sauce GOUSSI avec AKPALAN(POISSON FUME)': 2575, 'Riz sauce GOUSSI avec DEUEVI(PETIT POISSON)': 2275, 'Riz sauce GOUSSI avec APKALAN KANAMI(POISSON FRIT)': 2375, 'Riz sauce GOUSSI avec POULET': 2575, 'Riz sauce GOUSSI avec BOEUF': 3075, 'Riz sauce GOUSSI avec MOUTON': 3075, 'Riz sauce GOUSSI avec AKPAMA(PEAU DE BOEUF)': 2575, 'Riz sauce GOUSSI avec AGLAN(CRABE)': 2575, 'Riz sauce GOUSSI avec CREVETTE': 2575, 'Riz sauce ADEME avec RIEN ': 1875, 'Riz sauce ADEME avec AKPALAN(POISSON FUME)': 2375, 'Riz sauce ADEME avec DEUEVI(PETIT POISSON)': 2075, 'Riz sauce ADEME avec APKALAN KANAMI(POISSON FRIT)': 2175, 'Riz sauce ADEME avec POULET': 2375, 'Riz sauce ADEME avec BOEUF': 2875, 'Riz sauce ADEME avec MOUTON': 2875, 'Riz sauce ADEME avec AKPAMA(PEAU DE BOEUF)': 2375, 'Riz sauce ADEME avec AGLAN(CRABE)': 2375, 'Riz sauce ADEME avec CREVETTE': 2375, 'Riz sauce FETRI(GOMBO) avec RIEN ': 1575, 'Riz sauce FETRI(GOMBO) avec AKPALAN(POISSON FUME)': 2075, 'Riz sauce FETRI(GOMBO) avec DEUEVI(PETIT POISSON)': 1775, 'Riz sauce FETRI(GOMBO) avec APKALAN KANAMI(POISSON FRIT)': 1875, 'Riz sauce FETRI(GOMBO) avec POULET': 2075, 'Riz sauce FETRI(GOMBO) avec BOEUF': 2575, 'Riz sauce FETRI(GOMBO) avec MOUTON': 2575, 'Riz sauce FETRI(GOMBO) avec AKPAMA(PEAU DE BOEUF)': 2075, 'Riz sauce FETRI(GOMBO) avec AGLAN(CRABE)': 2075, 'Riz sauce FETRI(GOMBO) avec CREVETTE': 2075, 'Riz sauce KODORO avec RIEN ': 1675, 'Riz sauce KODORO avec AKPALAN(POISSON FUME)': 2175, 'Riz sauce KODORO avec DEUEVI(PETIT POISSON)': 1875, 'Riz sauce KODORO avec APKALAN KANAMI(POISSON FRIT)': 1975, 'Riz sauce KODORO avec POULET': 2175, 'Riz sauce KODORO avec BOEUF': 2675, 'Riz sauce KODORO avec MOUTON': 2675, 'Riz sauce KODORO avec AKPAMA(PEAU DE BOEUF)': 2175, 'Riz sauce KODORO avec AGLAN(CRABE)': 2175, 'Riz sauce KODORO avec CREVETTE': 2175, 'Riz sauce GNATOU avec RIEN ': 1975, 'Riz sauce GNATOU avec AKPALAN(POISSON FUME)': 2475, 'Riz sauce GNATOU avec DEUEVI(PETIT POISSON)': 2175, 'Riz sauce GNATOU avec APKALAN KANAMI(POISSON FRIT)': 2275, 'Riz sauce GNATOU avec POULET': 2475, 'Riz sauce GNATOU avec BOEUF': 2975, 'Riz sauce GNATOU avec MOUTON': 2975, 'Riz sauce GNATOU avec AKPAMA(PEAU DE BOEUF)': 2475, 'Riz sauce GNATOU avec AGLAN(CRABE)': 2475, 'Riz sauce GNATOU avec CREVETTE': 2475, 'Riz sauce ARACHIDE avec RIEN ': 1925, 'Riz sauce ARACHIDE avec AKPALAN(POISSON FUME)': 2425, 'Riz sauce ARACHIDE avec DEUEVI(PETIT POISSON)': 2125, 'Riz sauce ARACHIDE avec APKALAN KANAMI(POISSON FRIT)': 2225, 'Riz sauce ARACHIDE avec POULET': 2425, 'Riz sauce ARACHIDE avec BOEUF': 2925, 'Riz sauce ARACHIDE avec MOUTON': 2925, 'Riz sauce ARACHIDE avec AKPAMA(PEAU DE BOEUF)': 2425, 'Riz sauce ARACHIDE avec AGLAN(CRABE)': 2425, 'Riz sauce ARACHIDE avec CREVETTE': 2425, 'Riz sauce CHOU avec RIEN ': 2475, 'Riz sauce CHOU avec AKPALAN(POISSON FUME)': 2975, 'Riz sauce CHOU avec DEUEVI(PETIT POISSON)': 2675, 'Riz sauce CHOU avec APKALAN KANAMI(POISSON FRIT)': 2775, 'Riz sauce CHOU avec POULET': 2975, 'Riz sauce CHOU avec BOEUF': 3475, 'Riz sauce CHOU avec MOUTON': 3475, 'Riz sauce CHOU avec AKPAMA(PEAU DE BOEUF)': 2975, 'Riz sauce CHOU avec AGLAN(CRABE)': 2975, 'Riz sauce CHOU avec CREVETTE': 2975, 'Riz sauce FETRI POUPOU(GONBO SEC) avec RIEN ': 1725, 'Riz sauce FETRI POUPOU(GONBO SEC) avec AKPALAN(POISSON FUME)': 2225, 'Riz sauce FETRI POUPOU(GONBO SEC) avec DEUEVI(PETIT POISSON)': 1925, 'Riz sauce FETRI POUPOU(GONBO SEC) avec APKALAN KANAMI(POISSON FRIT)': 2025, 'Riz sauce FETRI POUPOU(GONBO SEC) avec POULET': 2225, 'Riz sauce FETRI POUPOU(GONBO SEC) avec BOEUF': 2725, 'Riz sauce FETRI POUPOU(GONBO SEC) avec MOUTON': 2725, 'Riz sauce FETRI POUPOU(GONBO SEC) avec AKPAMA(PEAU DE BOEUF)': 2225, 'Riz sauce FETRI POUPOU(GONBO SEC) avec AGLAN(CRABE)': 2225, 'Riz sauce FETRI POUPOU(GONBO SEC) avec CREVETTE': 2225, 'Riz sauce DEKOU(GRAINE) avec RIEN ': 2375, 'Riz sauce DEKOU(GRAINE) avec AKPALAN(POISSON FUME)': 2875, 'Riz sauce DEKOU(GRAINE) avec DEUEVI(PETIT POISSON)': 2575, 'Riz sauce DEKOU(GRAINE) avec APKALAN KANAMI(POISSON FRIT)': 2675, 'Riz sauce DEKOU(GRAINE) avec POULET': 2875, 'Riz sauce DEKOU(GRAINE) avec BOEUF': 3375, 'Riz sauce DEKOU(GRAINE) avec MOUTON': 3375, 'Riz sauce DEKOU(GRAINE) avec AKPAMA(PEAU DE BOEUF)': 2875, 'Riz sauce DEKOU(GRAINE) avec AGLAN(CRABE)': 2875, 'Riz sauce DEKOU(GRAINE) avec CREVETTE': 2875, 'Riz sauce EBESSESSI avec RIEN ': 1425, 'Riz sauce EBESSESSI avec AKPALAN(POISSON FUME)': 1925, 'Riz sauce EBESSESSI avec DEUEVI(PETIT POISSON)': 1625, 'Riz sauce EBESSESSI avec APKALAN KANAMI(POISSON FRIT)': 1725, 'Riz sauce EBESSESSI avec POULET': 1925, 'Riz sauce EBESSESSI avec BOEUF': 2425, 'Riz sauce EBESSESSI avec MOUTON': 2425, 'Riz sauce EBESSESSI avec AKPAMA(PEAU DE BOEUF)': 1925, 'Riz sauce EBESSESSI avec AGLAN(CRABE)': 1925, 'Riz sauce EBESSESSI avec CREVETTE': 1925, 'DEGUE': 1500, 'TAPIOCA ZOGBON': 1325, 'ATTIEKE POISSON': 1600, 'SPAGHETTI BLANC': 800, 'SALADE': 3975, 'HARICO HUIL ROUGE': 1525, 'HARICO HUIL ARACHIDE': 1375}

lis3 = {}
bases2a1 = {
    "TEKON(IGNAME BOULLIE)": {"igname": 1500, "sel": 25},
    "ABLO": {
        "farine de mais": 900,
        "farine de riz": 900,
        "sucre": 300,
        "sel": 25,
        "levure boulanger": 500
    },
    "DJINKOUME": {"farine mais": 900},
    "COUSCOUS": {"couscou": 1200, "huil": 300, "sel": 25},
    "KOLIKO": {"igname": 1500, "huil": 300, "sel": 25},
    "TIMBANI": {"haricos": 500, "sel": 25},
    "RIZ": {"riz": 750, "sel": 25},
    "AMANDA(ALLOCO)": {"bananes plantain": 1000, "huil": 300, "sel": 25},
    "AYIMOLOU": {"haricot": 500, "riz": 750, "potasse": 50},
    "SPAGHETTI": {"spaghetti": 350, "sel": 25}
}
proteines2a1 = {
    "RIEN ": {},
    "AKPALAN(POISSON FUME)": {"AKPALAN(POISSON FUME)": 500},
    "DEUEVI(PETIT POISSON)": {"DEUEVI(PETIT POISSON)": 200},
    "APKALAN KANAMI(POISSON FRIT)": {"APKALAN KANAMI(POISSON FRIT)": 300},
    "POULET": {"VIANDE DE POULET": 500},
    "BOEUF": {"VIANDE DE BOEUF": 1000},
    "MOUTON": {"VIANDE DE MOUTON": 1000},
    "AKPAMA(PEAU DE BOEUF)": {"AKPAMA(PEAU DE BOEUF)": 500},
    "AGLAN(CRABE)": {"AGLAN(CRABE)": 500},
    "CREVETTE": {"CREVETTE": 500}
}
sauces2a1 = {
    "TOMATE": {
        "TOMATE FRAIS": 200,
        "TOMATE CONCENTRE": 250,
        "HUIL VEGETAL": 300,
        "OIGNON": 100,
        "CUBE": 25,
        "SEL": 25,
        "AIL": 50,
        "PIMENT FRAIS": 100,
        "PIMENT EN POUDRE": 100,
        "POTASE": 50
    }
}
basesa1 = {
    "FOUFOU IGNAME": {"igname": 2000, "sel": 25},
    "FOUFOU PLANTAIN": {"bananas plantains": 1000, "sel": 25},
    "AKOUME(PATE MAIS)": {"Farine de mais": 900},
    "EMAKUME(PATE MAIS FERMENTE)": {
        "Farine de mais": 900,
        "pate de mais fermenter": 200
    },
    "Riz": {"riz": 750, "sel": 25}
}
saucesa1 = {
    "GBOMA": {
        "oignon": 100,
        "gingembre": 50,
        " ail": 50,
        "Tomate frais": 200,
        "piment frais": 100,
        "tomate concentre": 350,
        "huil rouge": 200,
        "sel": 25,
        "feuille de gboma": 500,
        "cube": 25
    },
    "TOMATE": {
        "TOMATE FRAIS": 200,
        "TOMATE CONCENTRE": 350,
        "HUIL VEGETAL": 300,
        "OIGNON": 100,
        "CUBE": 25,
        "SEL": 25,
        "AIL": 50,
        "PIMENT FRAIS": 100,
        "PIMENT EN POUDRE": 100,
        "POTASE": 50
    },
    "GOUSSI": {
        "sel": 25,
        "oignon": 100,
        "Graine de courge": 500,
        "tomate frais": 200,
        "piment frais": 100,
        "Tomate concentre": 350,
        "cube": 25
    },
    "ADEME": {
        "feuilles ademe": 400,
        "gingembre": 50,
        "oignon": 100,
        "piment frais": 100,
        "huile rouge": 200,
        "sel": 25,
        "potasse": 50,
        "poisson fermente": 150,
        "cube": 25
    },
    "FETRI(GOMBO)": {
        "gombo": 300,
        "tomate frais": 200,
        "oignon": 100,
        "piment frais": 100,
        "sel": 25,
        "gingembre": 50,
        "cube": 25
    },
    "KODORO": {
        "oignon": 100,
        "gingembre": 100,
        "ail": 50,
        "piment frais": 100,
        "sel": 25,
        " Afiti": 100,
        "Feuille de baobab": 400,
        "cube": 25
    },
    "GNATOU": {
        "Feuille de gnatou": 400,
        "Huil rouge": 200,
        "pate d´arachide": 200,
        "piment frais": 100,
        "oignon": 100,
        "cube": 25,
        "sel": 25,
        "afiti": 100,
        "ail": 50
    },
    "ARACHIDE": {
        "oignon": 100,
        "ail": 50,
        "gingembre": 100,
        "pate d´arachide": 200,
        "tomate frais": 200,
        "piment frais": 100,
        "sel": 25,
        "tomate concentre": 350,
        "cube": 25
    },
    "CHOU": {
        "TOMATE FRAIS": 200,
        "TOMATE CONCENTRE": 350,
        "HUIL VEGETAL": 300,
        "OIGNON": 100,
        "CUBE": 25,
        "SEL": 25,
        "AIL": 50,
        "PIMENT FRAIS": 100,
        "PIMENT EN POUDRE": 100,
        "POTASE": 50,
        "choux": 400
    },
    "FETRI POUPOU(GONBO SEC)": {
        "gombo sec": 300,
        "tomate frais": 200,
        "oignon": 100,
        "piment frais": 100,
        "piment en poudre": 100,
        "sel": 25,
        "gingembre": 100,
        "cube": 25
    },
    "DEKOU(GRAINE)": {
        "gingembre": 100,
        "oignon": 100,
        "ail": 50,
        "Sel": 25,
        "tomate frais": 200,
        "piment frais": 100,
        "Noi de palme": 1000,
        "cube": 25
    },
    "EBESSESSI": {
        "piment frais": 100,
        "oignon": 100,
        "tomate": 300,
        "sel": 25,
        "gingembre": 100,
        "cube": 25
    }
}
dica1 = {
    "DEGUE(ARACHIDE)": {
        "lait": 500,
        "couscous": 500,
        "sucre": 100,
        "glace": 100,
        "arachide": 300
    },"DEGUE SIMPLE": {
        "lait": 500,
        "couscous": 500,
        "sucre": 100,
        "glace": 100,
    },
    "TAPIOCA ZOGBON": {
        "tapioca": 500,
        "sel": 25,
        "sucre": 300,
        "lait en poudre": 500
    },
    "ATTIEKE POISSON": {
        "poisson frais": 500,
        "attieke": 500,
        "oignon": 100,
        "ail": 50,
        "piment frai": 100,
        "huile d´arachide": 300,
        "sel": 25,
        "cube": 25

    },
    "SPAGHETTI BLANC": {"spagheti": 350, "sel": 25, "piment frais": 100, "huil": 300, "cube": 25, },
    "SALADE": {
        "Laitue": 300,
        "Tomate": 200,
        "oignon": 100,
        "Beterave": 300,
        "Carotte": 300,
        "Concombre": 300,
        "Mayonnaise": 500,
        "cube": 25,
        "sardine": 300,
        "oeuf": 200,
        "spagheti": 350,
        "huil": 300,
        "vinaigre": 500,
        "pain": 300
    },
    "HARICO HUIL ROUGE ": {
        "harico": 500,
        "sel": 25,
        "potasse": 50,
        "oignon": 100,
        "ail": 50,
        "huil rouge": 500,
        "Gari": 300
    },
    "HARICO HUIL ARACHIDE 1": {
        "harico": 500,
        "sel": 25,
        "potasse": 100,
        "oignon": 100,
        "ail": 50,
        "huil d´arachide": 300,
        "Gari": 300
    },
    "HARICO HUIL ARACHIDE 2": {
        "harico": 500,
        "sel": 25,
        "potasse":50,
        "oignon": 100,
        "huil d´arachide": 300,
        "Gari": 300
    }
}
def calculer_tarifs(nb):
    # --- Fonction de calcul universelle ---
    def calculer_prix_total(base_dict, sauce_dict, prot_dict, nom_b, nom_s, nom_p):
        p_base = sum(base_dict.get(nom_b, {}).values())
        p_sauce = sum(sauce_dict.get(nom_s, {}).values())
        p_prot = sum(prot_dict.get(nom_p, {}).values())
        return p_base + p_sauce + p_prot

    # --- 1. Traitement des combinaisons 2a1 (Bases 2a1 + Sauce Tomate + Protéines) ---
    for plat in bases2a1:
        for sauce in sauces2a1:
            for prot in proteines2a1:
                nom_complet = f"{plat} sauce {sauce} avec {prot}"
                prix = calculer_prix_total(bases2a1, sauces2a1, proteines2a1, plat, sauce, prot)
                lis1[nom_complet] = prix
                lis2[nom_complet] = round((int(prix) / 3) * int(nb))

    # --- 2. Traitement des combinaisons a1 (Bases a1 + Toutes Sauces a1 + Protéines) ---
    for plat in basesa1:
        for sauce in saucesa1:
            for prot in proteines2a1:
                nom_complet = f"{plat} sauce {sauce} avec {prot}"
                prix = calculer_prix_total(basesa1, saucesa1, proteines2a1, plat, sauce, prot)
                lis1[nom_complet] = prix
                lis2[nom_complet] = round((int(prix) / 3) * int(nb))

    # --- 3. Traitement des plats directs (dica1) ---
    for plat, ingredients in dica1.items():
        prix = sum(ingredients.values())
        lis1[plat] = prix
        lis2[plat] = round(prix/3)*nb




    #---------------------------------------------------------------------

PLATS_PETIT_COMITE = lis1
PLATS_FAMILLE = lis2



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
    calculer_tarifs(nb)
    """Sélectionne dynamiquement le dictionnaire selon le nombre de convives."""
    if nb<=3:
        return PLATS_PETIT_COMITE, "Solo/Duo"
    elif nb>3:
        return PLATS_FAMILLE,"famille"



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
    # Configuration de la page
    # 1. Configuration de la page
    page.title = "Cliexe"
    page.theme_mode = ft.ThemeMode.LIGHT

    # 2. L'icône de la FENÊTRE (le fichier doit être accessible)
    # Assurez-vous que logo.png est à la racine de votre projet
    page.window_icon = "logo.png"

    # 3. Forcer la mise à jour pour que le système prenne en compte l'icône
    page.update()

    # Si vous voulez afficher l'icône DANS la page (Header)
    logo_display = ft.Image(
        src="logo.png",
        width=50,
        height=50,

    )

    page.add(logo_display, ft.Text("Bienvenue sur Fidelia"))

    # Correction de la variable test (si c'est un dictionnaire ou un objet)
    # En Python, on ne peut pas appeler un entier comme une fonction.
    # J'imagine que vous vouliez stocker ces infos :
    app_info = {
        "points": 21,
        "nom": "Cliexe",
        "logo": "logo.png",
        "icon": "logo.png"
    }
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

        import json


        import json
        import os

        def register(e):
            # 1. Vérification des champs
            nom = nom_in.value.strip() if nom_in.value else ""
            email = email_in.value.strip().lower() if email_in.value else ""
            password = pass_in.value.strip() if pass_in.value else ""
            tel = tel_in.value.strip() if tel_in.value else ""

            if not all([nom, email, password, tel]):
                err_msg.value = "Veuillez remplir tous les champs obligatoires."
                page.update()
                return

            # 2. Validation du numéro
            digits_only = "".join(filter(str.isdigit, tel))
            if len(digits_only) < 8:
                err_msg.value = "Numéro invalide (8 chiffres min)."
                page.update()
                return

            # 3. Feedback visuel
            btn_reg.disabled = True
            btn_reg.content = ft.ProgressRing(width=20, height=20, color="white", stroke_width=2)
            page.update()

            try:
                # 4. Préparation des données
                # Utilisation de .get() pour localId pour éviter le crash


                user_data = {
                    "nom": nom,
                    "email": email,
                    "tel": digits_only,
                    "ville": ville_in.value if ville_in.value else "",
                    "quartier": quartier_in.value if quartier_in.value else "",

                }

                # 5. Sauvegarde JSON avec encodage FORCÉ
                # On utilise 'w' et encoding='utf-8' pour éviter l'erreur 0x8a
                try:
                    with open("session_utilisateur.json", "w", encoding="utf-8") as f:
                        json.dump(user_data, f, ensure_ascii=False, indent=4)
                except Exception as file_err:
                    print(f"Erreur écriture fichier: {file_err}")

                # 6. Redirection
                render_home()

            except Exception as error:
                print(f"Erreur inscription: {error}")
                err_msg.value = "Erreur: Problème réseau ou compte déjà utilisé."
                btn_reg.disabled = False
                btn_reg.content = ft.Text("CRÉER MON COMPTE", weight="bold")
                page.update()

        # --- BOUTON PRINCIPAL ---
        btn_reg = ft.ElevatedButton(
            content=ft.Text("CRÉER MON COMPTE", weight="bold"),
            bgcolor=CP, color="white",  height=55, width=400,
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
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE
        )

        page.add(ft.Container(padding=20, content=formulaire))
        page.update()

    def no_compte(ns):
        # Palette de couleurs (assurez-vous que CP et CERR sont définis)
        CP = "#5D8A66"

        def go_to_auth(e):
            dlg.open = False
            page.update()
            go_to_signup()  # Appelle votre fonction de connexion existante

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

            if os.path.exists("session_utilisateur.json"):

                def confirm_logout(e):
                    try:
                        if os.path.exists("session_utilisateur.json"):
                            os.remove("session_utilisateur.json")  # Suppression effective
                        dlg.open = False
                        page.update()
                        go_to_signup()  # Retour à la page de connexion
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
        SESSION_FILE = "session_utilisateur.json"

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
                    """Récupère les infos de l'utilisateur de manière ultra-sécurisée"""
                    SESSION_FILE = "session_utilisateur.json"
                    default = {"nom": "Client Inconnu", "tel": "Non spécifié", "ville": "", "quartier": ""}

                    if not os.path.exists(SESSION_FILE):
                        return default

                    try:
                        with open(SESSION_FILE, "r", encoding="utf-8") as f:
                            data = json.load(f)

                        # On force le retour d'un dictionnaire même si le JSON est corrompu
                        if isinstance(data, dict):
                            return data
                        else:
                            return {"nom": str(data), "tel": "Non spécifié"}
                    except:
                        return default

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
                    envoi_reussi = envoyer_commande_marche()


                # ============ FIREBASE SEND ============
                import urllib.parse

                def envoyer_commande_marche():
                    try:
                        # 1. Infos utilisateur
                        user_info = get_user_session()
                        nom_client = user_info.get("nom", "Client")
                        tel_client = user_info.get("tel", "Inconnu")

                        # 2. Construction du panier texte pour WhatsApp
                        # Votre cart_items est un dictionnaire : { "Nom": {"qty": 2, "price": 500 ...} }
                        details_panier = ""
                        for name, data in cart_items.items():
                            qte = data.get("qty", 1)
                            details_panier += f"- {name} (x{qte})\n"

                        # 3. Message WhatsApp formaté
                        date_actuelle = datetime.now().strftime("%d/%m/%Y %H:%M")
                        message_whatsapp = (
                            f"🛒 *NOUVELLE COMMANDE MARCHÉ*\n\n"
                            f"👤 *Client:* {nom_client}\n"
                            f"📞 *Tel:* {tel_client}\n"
                            f"📍 *Lieu:* {user_info.get('ville', '')}, {user_info.get('quartier', '')}\n\n"
                            f"📦 *ARTICLES :*\n{details_panier}\n"
                            f"💰 *TOTAL :* {total_view.value}\n"
                            f"⏰ *Date:* {date_actuelle}"
                        )

                        # 4. Envoi et Redirection
                        msg_encoded = urllib.parse.quote(message_whatsapp)
                        num="22871075241"
                        # Remplacez par le numéro du commerçant
                        whatsapp_url = f"whatsapp://send?phone={num}&text={msg_encoded}"
                        page.launch_url(whatsapp_url)

                        render_final_view()  # Ou render_home() selon ton besoin
                        page.update()

                        return True  # Pour déclencher le dialogue de confirmation

                    except Exception as e:
                        print(f"Erreur envoi marché: {e}")
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
        SESSION_FILE = "session_utilisateur.json"

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

            import urllib.parse


            def envoyer_demande_pret(e):
                try:
                    # 1. Feedback visuel immédiat
                    btn_submit.disabled = True
                    btn_submit.content = ft.ProgressRing(width=20, height=20, color="white", stroke_width=2)
                    page.update()

                    # 2. Vérification connexion
                    try:
                        requests.get('https://www.google.com', timeout=3)
                    except:
                        raise Exception("Pas de connexion")

                    # 3. Récupération des données
                    user_info = get_user_session()  # Ta fonction de session corrigée
                    nom_client = user_info.get("nom", "Client")
                    tel_client = user_info.get("tel", "Inconnu")

                    montant_pret = f"{int(amt_slider.value):,} FCFA"
                    duree_pret = f"{int(duration_slider.value)} mois"
                    date_actuelle = datetime.now().strftime("%d/%m/%Y %H:%M")

                    # 4. ENREGISTREMENT SQLITE LOCAL (Historique des prêts)
                    conn = None
                    try:
                        conn = sqlite3.connect("prets.db")
                        cursor = conn.cursor()
                        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS demandes_pret 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, montant TEXT, duree TEXT, date TEXT)
                        ''')
                        cursor.execute('''
                            INSERT INTO demandes_pret (nom, montant, duree, date)
                            VALUES (?, ?, ?, ?)
                        ''', (nom_client, montant_pret, duree_pret, date_actuelle))
                        conn.commit()
                    except Exception as db_err:
                        print(f"Erreur SQLite Prêt: {db_err}")
                    finally:
                        if conn:
                            conn.close()  # Important pour éviter le RuntimeWarning

                    # 5. PRÉPARATION DU MESSAGE WHATSAPP
                    message_whatsapp = (
                        f"🏦 *NOUVELLE DEMANDE DE PRÊT ALIMENTAIRE*\n\n"
                        f"👤 *Client:* {nom_client}\n"
                        f"📞 *Tel:* {tel_client}\n"
                        f"📍 *Ville:* {user_info.get('ville', 'Non précisée')}\n\n"
                        f"💰 *Montant souhaité:* {montant_pret}\n"
                        f"📅 *Durée de remboursement:* {duree_pret}\n"
                        f"⏰ *Date:* {date_actuelle}\n\n"
                        f"👉 _Merci de me recontacter pour l'étude de mon dossier._"
                    )

                    # Encodage et lien
                    msg_encoded = urllib.parse.quote(message_whatsapp)
                    numero_service_finance = "22871075241"  # REMPLACE PAR TON NUMÉRO
                    whatsapp_url = f"https://wa.me/{numero_service_finance}?text={msg_encoded}"

                    # 6. LANCEMENT ET REDIRECTION
                    page.launch_url(whatsapp_url)

                    # Retour à l'écran précédent ou accueil
                    if 'on_back_callback' in locals() or 'on_back_callback' in globals():
                        on_back_callback()

                    page.update()

                except Exception as error:
                    print(f"Erreur Prêt: {error}")
                    # En cas d'erreur, on réactive le bouton
                    btn_submit.disabled = False
                    btn_submit.content = ft.Text("SOUMETTRE MA DEMANDE", weight="bold")
                    page.update()
                    if 'no_connexion' in globals(): no_connexion()

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
        SESSION_FILE = "session_utilisateur.json"
        if os.path.exists(SESSION_FILE):
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

                import urllib.parse

                def envoyer_commande_kit(e):
                    try:
                        # 1. Vérification rapide de la connexion
                        requests.get('https://www.google.com', timeout=5)

                        # 2. Feedback visuel sur le bouton
                        btn_kit.disabled = True
                        btn_kit.content = ft.ProgressRing(width=20, height=20, color="white")
                        page.update()

                        # 3. Récupération des données utilisateur (via ta fonction de session)
                        user_info = get_user_session()
                        date_actuelle = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        nom_client = user_info.get("nom", "Client")
                        tel_client = user_info.get("tel", "Inconnu")
                        ville = user_info.get("ville", "Non précisée")
                        quartier = user_info.get("quartier", "Non précisé")

                        # Nettoyage du prix
                        prix_clean = "".join(filter(str.isdigit, total_txt.value))
                        prix_numerique = int(prix_clean) if prix_clean else 0

                        # 4. ENREGISTREMENT SQLITE LOCAL (Historique & Fidélité)
                        try:
                            # Table des commandes
                            conn = sqlite3.connect("commandes.db")
                            cursor = conn.cursor()
                            cursor.execute('''
                                INSERT INTO commandes (date_commande, nom_plat, prix_total, ingredients)
                                VALUES (?, ?, ?, ?)
                            ''', (date_actuelle, plat_name, prix_numerique, ", ".join(panier_kit)))
                            conn.commit()
                            conn.close()

                            # Table Fidélité (+1 point)
                            conn_f = sqlite3.connect('fidelite.db')
                            cursor_f = conn_f.cursor()
                            cursor_f.execute('INSERT OR IGNORE INTO clients (nom, points) VALUES (?, 0)', (nom_client,))
                            cursor_f.execute('UPDATE clients SET points = points + 1 WHERE nom = ?', (nom_client,))
                            conn_f.commit()
                            conn_f.close()
                        except Exception as ex:
                            print(f"Erreur base de données local : {ex}")

                        # 5. PRÉPARATION DU MESSAGE WHATSAPP
                        liste_ingredients = "\n- ".join(panier_kit)
                        message_whatsapp = (
                            f"🔔 *NOUVELLE COMMANDE KIT CUISINE*\n\n"
                            f"👤 *Client:* {nom_client}\n"
                            f"📞 *Tel:* {tel_client}\n"
                            f"📍 *Lieu:* {ville}, {quartier}\n\n"
                            f"🍳 *Plat:* {plat_name}\n"
                            f"📦 *Ingrédients:* \n- {liste_ingredients}\n\n"
                            f"💰 *Total:* {total_txt.value}\n"
                            f"⏰ *Date:* {date_actuelle}"
                        )

                        # Encodage pour l'URL
                        msg= urllib.parse.quote(message_whatsapp)
                        numero= "22871075241"  # REMPLACE PAR TON NUMÉRO (ex: 22990000000)
                       

                        # 6. ACTION FINALE : Lancement de WhatsApp et redirection vers l'accueil

                        url_app = f"whatsapp://send?phone={numero}&text={msg}"
                        url_web = f"https://wa.me/{numero}?text={msg}"

                        try:
                            page.launch_url(url_app)
                        except:
                            page.launch_url(url_web)
                        render_final_view()
                        page.update()

                    except requests.RequestException:
                        # Erreur connexion : on restaure le bouton
                        btn_kit.disabled = False
                        btn_kit.content = ft.Text("COMMANDER LE KIT", weight="bold")
                        page.update()
                        if 'no_connexion' in globals(): no_connexion()

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



    def render_splash(page: ft.Page):

        #import time

        # 3. Simulation du temps de chargement (ou lecture de votre DB)
        #time.sleep(3)  # Laisse le logo 3 secondes

        # 4. Retirer le splash et lancer la vue principale
        page.splash = None
        render_final_view()  # Appelle votre fonction
        page.update()
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
        if os.path.exists("session_utilisateur.json"):
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
                go_to_signup(page)
        else:
            print("Aucun fichier de session trouvé.")
            go_to_signup(page)

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
        options_repas = sorted(list(PLATS_PETIT_COMITE.keys()))

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
    def render_final_view(e=None):
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
        conn = sqlite3.connect('fidelite.db')
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

        # On récupère ses points
        cursor.execute('SELECT points FROM clients WHERE nom = ?', (nom_utilisateur,))
        resultat = cursor.fetchone()
        points_actuels = resultat[0] if resultat else 0
        conn.close()

        points_actuels = resultat[0]

        with open("liste.json", "r") as f:
            ELEMENTS_VALUES = json.load(f)

        # 1. Préparation des dates
        today_iso = datetime.now().strftime("%Y-%m-%d")
        tomorrow_iso = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        rows = []

        # 2. Récupération sécurisée du planning
        try:
            conn = sqlite3.connect("repas_db.sqlite")
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
                    requests.get('https://www.google.com')

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
                    render_final_view()
                    page.update()

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
        if os.path.exists("session_utilisateur.json"):
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
                ], spacing=5, alignment=ft.Alignment(0,0)),
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
            ], alignment="spaceBetween"),  # Utilisation de string pour éviter les erreurs
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
            ], alignment="spaceBetween")
        )

        page.add(header, fidelia_badge, lv)
        page.update()

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
            # On supprime la logique du Timer pour une réponse instantanée
            try:
                # 1. On nettoie les résultats actuels
                search_results.controls = []

                # 2. On récupère les données (assure-toi que cette fonction est rapide)
                nb = float(guests_input.value or 1)
                dico, _ = get_active_dict(nb)

                query_lower = query.lower().strip()

                # 3. Filtrage ultra-rapide par la première lettre (début du mot)
                if query_lower == "":
                    all_items = [(k, v) for k, v in dico.items() if v <= 2000]
                else:
                    # Recherche instantanée par le début
                    all_items = [(k, v) for k, v in dico.items() if k.lower().startswith(query_lower)]

                # 4. Tri rapide par prix
                all_items.sort(key=lambda x: x[1])

                # 5. Création des contrôles (Limité à 15 pour la vitesse de rendu)
                new_controls = []
                for n, p in all_items[:15]:
                    # Attribution rapide de la couleur
                    if p <= 2000:
                        clr = ft.Colors.GREEN_400
                    elif p <= 7000:
                        clr = ft.Colors.ORANGE_400
                    else:
                        clr = ft.Colors.PURPLE_400

                    new_controls.append(
                        ft.Container(
                            content=ft.ListTile(
                                leading=ft.Icon(ft.Icons.RESTAURANT_MENU, color=clr, size=20),
                                title=ft.Text(n, weight="w500", size=14),
                                subtitle=ft.Text(f"{p} FCFA", size=12),
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

                # 6. Mise à jour immédiate
                search_results.controls = new_controls
                page.update()

            except Exception as e:
                print(f"Erreur recherche instantanée : {e}")

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

