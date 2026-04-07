[app]

# (str) Title of your application
title = CLIEXE

# (str) Package name
package.name = cliexeapp

# (str) Package domain (needed for android/ios packaging)
package.domain = org.votre.nom

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 0.1

# (list) Application requirements
# IMPORTANT : On ajoute flet ici pour que l'APK reconnaisse tes commandes
requirements = python3, flet, urllib3

# (list) Permissions
# On autorise l'app à aller sur le net et à ouvrir d'autres apps
android.permissions = INTERNET, ACTION_VIEW

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (int) Target Android API (33 est la norme actuelle)
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# --- LA LIGNE MAGIQUE POUR WHATSAPP ---
# Indispensable pour Android 11, 12, 13+
android.manifest.queries = com.whatsapp

# (bool) Indique si l'écran doit rester allumé
android.wakelock = False

# (str) Android logcat filters
android.logcat_filters = *:S python:D

[buildozer]

# (int) Log level (2 = debug pour voir les erreurs de compilation sur GitHub)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
