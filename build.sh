#!/usr/bin/env bash
# Sortie en cas d'erreur
set -o errexit

echo "📦 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

echo "🗄️ Application des migrations..."
python manage.py migrate

echo "👤 Création du superutilisateur (si non existant)..."
python manage.py createsuperuser --no-input || echo "Superuser existe déjà ou erreur ignorée"

echo "✅ Build terminé avec succès !"