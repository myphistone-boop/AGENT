#!/bin/bash

# Exemple d'utilisation du générateur Gemini
# ==========================================

echo "🎨 Générateur de Templates avec Gemini AI"
echo "=========================================="
echo ""

# Vérifier la clé API
if [ -z "$GEMINI_API_KEY" ]; then
    echo "⚠️  GEMINI_API_KEY non définie"
    echo ""
    echo "Pour obtenir une clé API:"
    echo "1. Aller sur: https://makersuite.google.com/app/apikey"
    echo "2. Créer une clé API"
    echo "3. Exporter: export GEMINI_API_KEY='votre_clé'"
    echo ""
    exit 1
fi

echo "✅ Clé API Gemini détectée"
echo ""

# Exemple 1: Site de thérapeute
echo "📝 Exemple 1: Génération d'un site de thérapeute"
echo "================================================"
echo ""
echo "URL source: https://www.psychologue-exemple.fr"
echo "Thème: thérapeute"
echo ""

read -p "Lancer la génération ? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    python -m scripts.gemini_template_generator \
        --url "https://www.psychologue-exemple.fr" \
        --theme "thérapeute" \
        --preview
fi

echo ""
echo "✅ Terminé !"
echo ""
echo "📂 Résultats dans: outputs/gemini_templates/"
echo ""

# Autres exemples commentés
echo "💡 Autres exemples à essayer:"
echo ""
echo "# Coach sportif"
echo "python -m scripts.gemini_template_generator --url 'https://...' --theme 'coach sportif' --preview"
echo ""
echo "# Yoga"
echo "python -m scripts.gemini_template_generator --url 'https://...' --theme 'yoga' --preview"
echo ""
echo "# Photographe"
echo "python -m scripts.gemini_template_generator --url 'https://...' --theme 'photographe' --preview"
echo ""
