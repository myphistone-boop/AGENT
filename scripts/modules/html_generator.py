"""
Générateur de HTML à partir de templates
"""
import random
from pathlib import Path
from scripts.utils.logger import setup_logger
from scripts.utils.file_manager import FileManager
from config import settings

logger = setup_logger("html_generator")


class HTMLGenerator:
    """Générateur de pages HTML depuis templates"""

    def __init__(self):
        self.file_manager = FileManager()
        self.templates_path = settings.TEMPLATES_PATH

    def generate(self, client_id, sector, data, colors=None):
        """
        Génère le HTML pour un client

        Args:
            client_id: ID du client
            sector: Secteur d'activité (beaute, artisan, etc.)
            data: Données du client (nom, textes, images, etc.)
            colors: Palette de couleurs (optionnel)

        Returns:
            str: Chemin vers le fichier HTML généré
        """
        logger.info(f"🎨 Génération HTML pour client {client_id} - Secteur: {sector}")

        # Sélectionner un template
        template_path = self._select_template(sector)

        if not template_path:
            logger.error(f"❌ Pas de template trouvé pour secteur: {sector}")
            return None

        # Charger le template
        with open(template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Appliquer les couleurs
        if colors:
            html_content = self._apply_colors(html_content, colors)
        else:
            # Couleurs par défaut
            default_colors = settings.DEFAULT_COLORS.get(sector, settings.DEFAULT_COLORS['commerce'])
            html_content = self._apply_colors(html_content, default_colors)

        # Remplacer les variables
        html_content = self._replace_variables(html_content, data)

        # Sauvegarder
        client_dir = self.file_manager.create_client_temp_dir(client_id)
        output_path = client_dir / "website_generated.html"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"✅ HTML généré: {output_path}")
        return str(output_path)

    def _select_template(self, sector):
        """Sélectionne un template pour un secteur"""
        sector_dir = self.templates_path / sector

        if not sector_dir.exists():
            logger.warning(f"⚠️  Dossier secteur inexistant: {sector}, utilisation 'commerce'")
            sector_dir = self.templates_path / "commerce"

        # Lister les templates disponibles
        templates = list(sector_dir.glob("template_*.html"))

        if not templates:
            logger.error(f"❌ Aucun template dans: {sector_dir}")
            return None

        # Choisir aléatoirement
        chosen = random.choice(templates)
        logger.info(f"📄 Template choisi: {chosen.name}")

        return chosen

    def _apply_colors(self, html, colors):
        """Applique les couleurs au template"""
        logger.debug("🎨 Application des couleurs...")

        # Remplacer les variables CSS
        html = html.replace('--primary-color: #default;', f"--primary-color: {colors['primary']};")
        html = html.replace('--secondary-color: #default;', f"--secondary-color: {colors['secondary']};")
        html = html.replace('--accent-color: #default;', f"--accent-color: {colors['accent']};")

        return html

    def _replace_variables(self, html, data):
        """Remplace les variables dans le template"""
        logger.debug("📝 Remplacement des variables...")

        # Mapping des variables
        replacements = {
            '{{CLIENT_NAME}}': data.get('name', 'Entreprise'),
            '{{HERO_TITLE}}': data.get('hero_title', data.get('name', 'Bienvenue')),
            '{{HERO_SUBTITLE}}': data.get('hero_subtitle', data.get('description', '')),
            '{{SLOGAN}}': data.get('slogan', ''),

            # Contact
            '{{PHONE}}': data.get('phone', ''),
            '{{EMAIL}}': data.get('email', ''),
            '{{ADDRESS}}': data.get('address', ''),

            # Images
            '{{LOGO_URL}}': data.get('logo', ''),
            '{{IMAGE_1}}': data.get('images', [''])[0] if data.get('images') else '',
            '{{IMAGE_2}}': data.get('images', ['', ''])[1] if data.get('images', []) and len(data.get('images', [])) > 1 else '',
            '{{IMAGE_3}}': data.get('images', ['', '', ''])[2] if data.get('images', []) and len(data.get('images', [])) > 2 else '',

            # CTA
            '{{CTA_TEXT}}': data.get('cta', 'Nous contacter'),
        }

        # Services (si disponibles)
        services = data.get('services', [])
        for i in range(1, 4):
            if i <= len(services):
                replacements[f'{{{{SERVICE_{i}_TITLE}}}}'] = services[i-1].get('title', '')
                replacements[f'{{{{SERVICE_{i}_DESCRIPTION}}}}'] = services[i-1].get('description', '')
            else:
                replacements[f'{{{{SERVICE_{i}_TITLE}}}}'] = ''
                replacements[f'{{{{SERVICE_{i}_DESCRIPTION}}}}'] = ''

        # About
        replacements['{{ABOUT_TEXT}}'] = data.get('about', '')

        # Textes supplémentaires
        texts = data.get('texts', [])
        for i in range(1, 6):
            if i <= len(texts):
                replacements[f'{{{{TEXT_{i}}}}}'] = texts[i-1]
            else:
                replacements[f'{{{{TEXT_{i}}}}}'] = ''

        # Appliquer les remplacements
        for placeholder, value in replacements.items():
            if value is None:
                value = ''
            html = html.replace(placeholder, str(value))

        return html


def main():
    """Test du générateur HTML"""
    import argparse
    import json

    parser = argparse.ArgumentParser(description='Générateur HTML')
    parser.add_argument('--sector', type=str, default='beaute', help='Secteur (beaute, artisan, etc.)')
    parser.add_argument('--client-id', type=str, default='test', help='ID client')

    args = parser.parse_args()

    # Données de test
    test_data = {
        'name': 'Salon Test',
        'hero_title': 'Bienvenue chez Salon Test',
        'hero_subtitle': 'Votre beauté, notre passion',
        'slogan': 'L\'élégance au quotidien',
        'phone': '01 23 45 67 89',
        'email': 'contact@salontest.fr',
        'address': '123 rue de la Paix, Paris',
        'services': [
            {'title': 'Coupe', 'description': 'Coupe adaptée à votre style'},
            {'title': 'Coloration', 'description': 'Techniques modernes'},
            {'title': 'Soins', 'description': 'Traitements capillaires'}
        ],
        'about': 'Salon Test vous accueille dans un cadre chaleureux pour sublimer votre beauté.',
        'cta': 'Prendre rendez-vous'
    }

    # Couleurs de test
    test_colors = {
        'primary': '#e91e63',
        'secondary': '#9c27b0',
        'accent': '#f8bbd0'
    }

    generator = HTMLGenerator()
    output_path = generator.generate(args.client_id, args.sector, test_data, test_colors)

    if output_path:
        print(f"\n{'='*60}")
        print(f"✅ HTML GÉNÉRÉ")
        print(f"{'='*60}\n")

        print(f"Fichier: {output_path}")
        print(f"Secteur: {args.sector}")

        print(f"\n👁️  Ouvrez ce fichier dans votre navigateur pour voir le résultat:")
        print(f"   file://{Path(output_path).absolute()}")

    else:
        print("❌ Échec de la génération")


if __name__ == "__main__":
    main()
