"""
Générateur de templates avec Gemini AI
Scrape un site existant et génère un nouveau site créatif du même thème
"""
import os
import json
import argparse
import google.generativeai as genai
from pathlib import Path
from scripts.modules.website_scraper import WebsiteScraper
from scripts.utils.logger import setup_logger
from scripts.utils.file_manager import FileManager

logger = setup_logger("gemini_generator")


class GeminiTemplateGenerator:
    """Générateur de templates avec Gemini"""

    def __init__(self, theme: str, source_url: str, api_key: str = None):
        """
        Args:
            theme: Type de template (ex: "thérapeute", "coach", "yoga")
            source_url: URL du site à scraper
            api_key: Clé API Gemini (ou via GEMINI_API_KEY env var)
        """
        self.theme = theme
        self.source_url = source_url
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')

        if not self.api_key:
            raise ValueError("❌ Clé API Gemini manquante (GEMINI_API_KEY env var)")

        # Configuration Gemini
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')

        # File manager
        self.file_manager = FileManager()

        # Génération d'un ID unique pour ce projet
        self.project_id = f"gemini_{theme.lower().replace(' ', '_')}"
        self.output_dir = None

    def generate(self):
        """
        Pipeline complet : Scrape → Gemini → HTML/CSS/JS

        Returns:
            dict: Résultats avec paths des fichiers générés
        """
        logger.info(f"🎨 Génération d'un template '{self.theme}' depuis {self.source_url}")

        # 1. Scraper le site source
        logger.info("📥 Étape 1/3: Scraping du site source...")
        scraped_data = self._scrape_source()
        if not scraped_data:
            logger.error("❌ Échec du scraping")
            return None

        # 2. Générer avec Gemini
        logger.info("🤖 Étape 2/3: Génération créative avec Gemini...")
        generated_code = self._generate_with_gemini(scraped_data)
        if not generated_code:
            logger.error("❌ Échec de la génération Gemini")
            return None

        # 3. Sauvegarder les fichiers
        logger.info("💾 Étape 3/3: Sauvegarde des fichiers...")
        output_paths = self._save_output(generated_code, scraped_data)

        logger.info(f"✅ Template généré avec succès !")
        logger.info(f"📂 Fichiers dans: {self.output_dir}")

        return {
            'output_dir': str(self.output_dir),
            'html_file': output_paths['html'],
            'data_file': output_paths['data'],
            'scraped_data': scraped_data
        }

    def _scrape_source(self):
        """Scrape le site source"""
        scraper = WebsiteScraper(self.project_id, self.source_url)
        data = scraper.scrape()

        if data:
            logger.info(f"✓ Site scrappé: {data.get('title', 'N/A')}")
            logger.info(f"  - {len(data.get('images', []))} images")
            logger.info(f"  - {len(data.get('texts', []))} paragraphes")
            logger.info(f"  - Logo: {'✓' if data.get('logo') else '✗'}")

        return data

    def _generate_with_gemini(self, scraped_data):
        """Génère le code HTML/CSS/JS avec Gemini"""

        # Construire le prompt créatif
        prompt = self._build_creative_prompt(scraped_data)

        try:
            # Appel à Gemini
            logger.info("🔮 Appel à Gemini Pro...")
            response = self.model.generate_content(prompt)

            # Extraire le code
            code = response.text

            # Parser les blocs de code
            html_code = self._extract_code_block(code, 'html')

            if not html_code:
                # Si pas de bloc markdown, prendre tout le contenu
                html_code = code

            logger.info(f"✓ Code généré ({len(html_code)} caractères)")
            return html_code

        except Exception as e:
            logger.error(f"❌ Erreur Gemini: {str(e)}")
            return None

    def _build_creative_prompt(self, scraped_data):
        """Construit un prompt créatif pour Gemini"""

        # Préparer les données
        title = scraped_data.get('title', 'Mon Site')
        description = scraped_data.get('description', '')
        headings = scraped_data.get('headings', [])[:5]
        texts = scraped_data.get('texts', [])[:8]
        phone = scraped_data.get('phone', '')
        email = scraped_data.get('email', '')

        prompt = f"""Tu es un designer web créatif et talentueux.

Je veux que tu crées un site web MODERNE, ÉLÉGANT et CRÉATIF pour un·e {self.theme}.

DONNÉES DU CLIENT (à utiliser dans le site):
- Titre/Nom: {title}
- Description: {description}
- Téléphone: {phone}
- Email: {email}

SECTIONS/TITRES à intégrer:
{chr(10).join(f'- {h}' for h in headings)}

TEXTES à utiliser:
{chr(10).join(f'- {t[:150]}...' for t in texts[:5])}

INSTRUCTIONS CRÉATIVES:

1. DESIGN VISUEL:
   - Utilise une palette de couleurs PROFESSIONNELLE et HARMONIEUSE pour un·e {self.theme}
   - Design moderne avec beaucoup d'espace blanc (whitespace)
   - Typographie élégante (Google Fonts)
   - Animations subtiles et fluides
   - Dégradés et effets visuels modernes

2. STRUCTURE:
   - Hero section impactante avec titre accrocheur
   - Section "À propos" / présentation
   - Section services/offres
   - Section témoignages (invente 2-3 témoignages crédibles pour un·e {self.theme})
   - Section contact avec formulaire
   - Footer professionnel

3. INTERACTIVITÉ:
   - Animations au scroll (fade-in, slide-in)
   - Boutons avec hover effects
   - Navigation smooth scroll
   - Formulaire de contact fonctionnel (action vers formspree.io ou email)

4. TECHNOLOGIE:
   - Site ONE-PAGE en HTML pur (tout dans un seul fichier)
   - CSS moderne (flexbox, grid, animations CSS)
   - JavaScript vanilla pour interactions
   - Responsive mobile-first
   - Optimisé pour la performance

5. CONTENU:
   - Utilise TOUS les textes fournis ci-dessus
   - Réorganise-les de manière cohérente
   - Améliore la présentation si nécessaire
   - Garde le même message et les mêmes informations

6. IMAGES:
   - Utilise des placeholders élégants (via https://placehold.co/WIDTHxHEIGHT/BGCOLOR/TEXTCOLOR ou unsplash.com)
   - Choisir des images pertinentes pour un·e {self.theme}

IMPORTANT:
- Génère UN SEUL FICHIER HTML complet (avec CSS et JS inline)
- Code propre et bien commenté
- Prêt à être déployé immédiatement
- Design qui WOW

Génère le code HTML complet maintenant:
"""

        return prompt

    def _extract_code_block(self, text, language='html'):
        """Extrait un bloc de code markdown"""
        import re

        # Pattern pour ```html ... ```
        pattern = rf'```{language}\s*\n(.*?)```'
        match = re.search(pattern, text, re.DOTALL)

        if match:
            return match.group(1).strip()

        # Essayer sans langage spécifié
        pattern = r'```\s*\n(.*?)```'
        match = re.search(pattern, text, re.DOTALL)

        if match:
            return match.group(1).strip()

        return None

    def _save_output(self, html_code, scraped_data):
        """Sauvegarde les fichiers générés"""

        # Créer le dossier de sortie
        self.output_dir = Path('outputs') / 'gemini_templates' / self.project_id
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Sauvegarder le HTML
        html_file = self.output_dir / 'index.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_code)

        logger.info(f"✓ HTML: {html_file}")

        # Sauvegarder les données scrappées (pour référence)
        data_file = self.output_dir / 'scraped_data.json'
        with open(data_file, 'w', encoding='utf-8') as f:
            # Copie sans les paths (pour avoir un JSON propre)
            data_clean = {
                k: v for k, v in scraped_data.items()
                if not k.endswith('_path') and k != 'screenshot_original'
            }
            json.dump(data_clean, f, ensure_ascii=False, indent=2)

        logger.info(f"✓ Data: {data_file}")

        # Créer un README pour la validation
        readme_file = self.output_dir / 'README.md'
        readme_content = f"""# Template {self.theme.title()}

Généré automatiquement avec Gemini AI

## Source
- URL: {self.source_url}
- Thème: {self.theme}

## Fichiers
- `index.html` - Site complet (HTML/CSS/JS)
- `scraped_data.json` - Données extraites du site source

## Validation manuelle

1. Ouvrir `index.html` dans un navigateur
2. Vérifier le design et les contenus
3. Tester sur mobile (responsive)
4. Valider les informations (textes, contact, etc.)

## Prochaines étapes

Si le template est validé:
- Déployer sur un hébergement
- Personnaliser davantage si nécessaire
- Intégrer des analytics

Si modifications nécessaires:
- Régénérer avec Gemini
- Éditer manuellement le HTML
"""

        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)

        logger.info(f"✓ README: {readme_file}")

        return {
            'html': str(html_file),
            'data': str(data_file),
            'readme': str(readme_file)
        }

    def preview_in_browser(self):
        """Ouvre le template dans le navigateur pour validation"""
        import webbrowser

        if self.output_dir:
            html_file = self.output_dir / 'index.html'
            if html_file.exists():
                logger.info(f"🌐 Ouverture dans le navigateur...")
                webbrowser.open(f'file://{html_file.absolute()}')
                return True

        return False


def main():
    """CLI pour générer un template"""
    parser = argparse.ArgumentParser(
        description='Générateur de templates avec Gemini AI'
    )

    parser.add_argument(
        '--url',
        type=str,
        required=True,
        help='URL du site à scraper'
    )

    parser.add_argument(
        '--theme',
        type=str,
        required=True,
        help='Thème du template (ex: thérapeute, coach, yoga)'
    )

    parser.add_argument(
        '--api-key',
        type=str,
        help='Clé API Gemini (ou utiliser GEMINI_API_KEY env var)'
    )

    parser.add_argument(
        '--preview',
        action='store_true',
        help='Ouvrir dans le navigateur après génération'
    )

    args = parser.parse_args()

    try:
        # Créer le générateur
        generator = GeminiTemplateGenerator(
            theme=args.theme,
            source_url=args.url,
            api_key=args.api_key
        )

        # Générer
        result = generator.generate()

        if result:
            print("\n" + "="*70)
            print("✅ TEMPLATE GÉNÉRÉ AVEC SUCCÈS")
            print("="*70)
            print(f"\n📂 Dossier: {result['output_dir']}")
            print(f"\n📄 Fichiers:")
            print(f"   - {result['html_file']}")
            print(f"   - {result['data_file']}")

            print(f"\n🔍 VALIDATION MANUELLE:")
            print(f"   1. Ouvrir {result['html_file']} dans un navigateur")
            print(f"   2. Vérifier le design et les contenus")
            print(f"   3. Valider sur mobile (responsive)")

            # Preview automatique
            if args.preview:
                generator.preview_in_browser()
            else:
                print(f"\n💡 Pour prévisualiser: python -m scripts.gemini_template_generator --url {args.url} --theme \"{args.theme}\" --preview")

            print()
        else:
            print("\n❌ Échec de la génération")

    except Exception as e:
        logger.error(f"❌ Erreur: {str(e)}")
        raise


if __name__ == "__main__":
    main()
