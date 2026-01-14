"""
Générateur de templates avec Gemini AI
Scrape un site existant et génère un nouveau site créatif du même thème
"""
import os
import json
import argparse
import ssl
import google.generativeai as genai
from pathlib import Path
from scripts.modules.website_scraper import WebsiteScraper
from scripts.utils.logger import setup_logger
from scripts.utils.file_manager import FileManager

# ============================================================================
# CONFIGURATION SSL - Désactivée par défaut pour proxy d'entreprise
# ============================================================================
# Ceci permet de contourner les erreurs de certificats auto-signés
# dans les environnements d'entreprise avec proxy HTTPS

# Désactiver la vérification SSL pour Python
os.environ['PYTHONHTTPSVERIFY'] = '0'
os.environ['GRPC_ENABLE_FORK_SUPPORT'] = '1'
os.environ['GRPC_VERBOSITY'] = 'ERROR'  # Réduire les logs gRPC

# Forcer l'utilisation de contexte SSL non vérifié
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except:
    pass

# Tenter d'utiliser certifi si disponible, sinon ignorer
try:
    import certifi
    os.environ['GRPC_DEFAULT_SSL_ROOTS_FILE_PATH'] = certifi.where()
except ImportError:
    pass

# Désactiver les warnings SSL
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    pass

logger = setup_logger("gemini_generator")


class GeminiTemplateGenerator:
    """Générateur de templates avec Gemini"""

    def __init__(self, theme: str, source_url: str = None, api_key: str = None):
        """
        Args:
            theme: Type de template (ex: "thérapeute", "coach", "yoga")
            source_url: URL du site à scraper (optionnel si utilisation de données existantes)
            api_key: Clé API Gemini (ou via GEMINI_API_KEY env var)
        """
        self.theme = theme
        self.source_url = source_url
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')

        if not self.api_key:
            raise ValueError("❌ Clé API Gemini manquante (GEMINI_API_KEY env var)")

        # Configuration Gemini
        # Note: La vérification SSL est désactivée par défaut (voir en-tête du fichier)
        # pour permettre l'utilisation derrière des proxies d'entreprise
        genai.configure(api_key=self.api_key)

        # Configuration du modèle avec timeout étendu pour environnements proxy
        self.model = genai.GenerativeModel('gemini-1.5-pro')

        # Configuration de génération avec timeout étendu
        self.generation_config = {
            'temperature': 0.9,  # Créativité élevée pour le design
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 8192,  # Permet de générer un site complet
        }

        # File manager
        self.file_manager = FileManager()

        # Génération d'un ID unique pour ce projet
        self.project_id = f"gemini_{theme.lower().replace(' ', '_')}"
        self.output_dir = None

    def generate(self, existing_data=None):
        """
        Pipeline complet : Scrape → Gemini → HTML/CSS/JS

        Args:
            existing_data: Données déjà scrapées (optionnel, skip la phase de scraping)

        Returns:
            dict: Résultats avec paths des fichiers générés
        """
        # Si données existantes fournies, skip le scraping
        if existing_data:
            logger.info(f"🎨 Génération d'un template '{self.theme}' depuis données existantes")
            logger.info(f"⏭️  Phase de scraping ignorée (utilisation de données pré-scrapées)")
            scraped_data = existing_data

            # Afficher un résumé des données
            logger.info(f"📊 Données chargées:")
            logger.info(f"   - Titre: {scraped_data.get('title', 'N/A')}")
            logger.info(f"   - {len(scraped_data.get('structure', []))} sections")
            logger.info(f"   - {len(scraped_data.get('image_urls', []))} images URLs")

        else:
            # Pipeline normal avec scraping
            logger.info(f"🎨 Génération d'un template '{self.theme}' depuis {self.source_url}")

            # 1. Scraper le site source
            logger.info("📥 Étape 1/3: Scraping du site source...")
            scraped_data = self._scrape_source()
            if not scraped_data:
                logger.error("❌ Échec du scraping")
                return None

        # 2. Générer avec Gemini
        step_num = "2/2" if existing_data else "2/3"
        logger.info(f"🤖 Étape {step_num}: Génération créative avec Gemini...")
        generated_code = self._generate_with_gemini(scraped_data)
        if not generated_code:
            logger.error("❌ Échec de la génération Gemini")
            return None

        # 3. Sauvegarder les fichiers
        step_num = "3/3" if not existing_data else "2/2"
        logger.info(f"💾 Étape {step_num}: Sauvegarde des fichiers...")
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
            logger.info(f"  - {len(data.get('structure', []))} sections extraites")
            logger.info(f"  - {len(data.get('image_urls', []))} images URLs")
            logger.info(f"  - Logo URL: {'✓' if data.get('logo_url') else '✗'}")

            # Compter le contenu total
            total_items = sum(len(s.get('content', [])) for s in data.get('structure', []))
            logger.info(f"  - {total_items} éléments de contenu (titres, paragraphes, listes)")

        return data

    def _generate_with_gemini(self, scraped_data):
        """Génère le code HTML/CSS/JS avec Gemini"""
        import time

        # Construire le prompt créatif
        prompt = self._build_creative_prompt(scraped_data)

        # Retry logic pour gérer les problèmes de réseau/proxy
        max_retries = 3
        retry_delay = 5  # secondes

        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    logger.info(f"🔄 Tentative {attempt + 1}/{max_retries}...")
                    time.sleep(retry_delay)

                # Appel à Gemini avec API REST (au lieu de gRPC qui peut être bloqué)
                logger.info("🔮 Appel à Gemini Pro (API REST)...")

                # Essayer d'abord l'API REST (plus compatible avec firewalls)
                code = self._generate_with_rest_api(prompt)

                if code:
                    # Parser les blocs de code
                    html_code = self._extract_code_block(code, 'html')

                    if not html_code:
                        # Si pas de bloc markdown, prendre tout le contenu
                        html_code = code

                    logger.info(f"✓ Code généré ({len(html_code)} caractères)")
                    return html_code

            except Exception as e:
                error_msg = str(e)
                logger.error(f"❌ Erreur Gemini (tentative {attempt + 1}/{max_retries}): {error_msg}")

                # Si c'est la dernière tentative, abandonner
                if attempt == max_retries - 1:
                    logger.error("❌ Échec après toutes les tentatives")
                    logger.error("💡 Vérifiez:")
                    logger.error("   - Votre connexion internet")
                    logger.error("   - Configuration du proxy (HTTP_PROXY, HTTPS_PROXY)")
                    logger.error("   - Que l'API Gemini est accessible depuis votre réseau")
                    return None

                # Sinon, attendre avant de réessayer
                logger.info(f"⏳ Nouvelle tentative dans {retry_delay} secondes...")

        return None

    def _generate_with_rest_api(self, prompt):
        """Appel direct à l'API REST Gemini (évite gRPC qui peut être bloqué)"""
        import requests

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent"

        headers = {
            'Content-Type': 'application/json',
        }

        payload = {
            'contents': [{
                'parts': [{
                    'text': prompt
                }]
            }],
            'generationConfig': {
                'temperature': self.generation_config['temperature'],
                'topP': self.generation_config['top_p'],
                'topK': self.generation_config['top_k'],
                'maxOutputTokens': self.generation_config['max_output_tokens'],
            }
        }

        params = {
            'key': self.api_key
        }

        # Timeout plus long pour les réseaux lents
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            params=params,
            timeout=180  # 3 minutes
        )

        response.raise_for_status()

        result = response.json()

        # Extraire le texte de la réponse
        if 'candidates' in result and len(result['candidates']) > 0:
            candidate = result['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                parts = candidate['content']['parts']
                if len(parts) > 0 and 'text' in parts[0]:
                    return parts[0]['text']

        raise Exception("Réponse API invalide: pas de texte généré")


    def _build_creative_prompt(self, scraped_data):
        """Construit un prompt créatif pour Gemini"""

        # Préparer les données
        title = scraped_data.get('title', 'Mon Site')
        description = scraped_data.get('description', '')
        phone = scraped_data.get('phone', '')
        email = scraped_data.get('email', '')
        logo_url = scraped_data.get('logo_url', '')
        image_urls = scraped_data.get('image_urls', [])
        structure = scraped_data.get('structure', [])

        # Formatter la structure pour le prompt
        structure_text = self._format_structure_for_prompt(structure, image_urls)

        prompt = f"""Tu es un designer web créatif et talentueux.

MISSION: Recrée ce site web avec un DESIGN MODERNE et ÉLÉGANT, tout en préservant EXACTEMENT la même structure et les mêmes contenus.

Le client veut reconnaître son site (même squelette, mêmes textes) mais avec un visuel PROFESSIONNEL et MODERNE.

════════════════════════════════════════════════════════════════

INFORMATIONS DU CLIENT:
- Type: {self.theme}
- Titre/Nom: {title}
- Description: {description}
- Logo: {logo_url if logo_url else 'Pas de logo'}
- Téléphone: {phone}
- Email: {email}

════════════════════════════════════════════════════════════════

STRUCTURE EXACTE À REPRODUIRE:

{structure_text}

════════════════════════════════════════════════════════════════

INSTRUCTIONS STRICTES:

1. STRUCTURE & CONTENU (À PRÉSERVER EXACTEMENT):
   ✓ Garde le MÊME ORDRE des sections
   ✓ Garde les MÊMES TITRES (texte identique)
   ✓ Garde les MÊMES PARAGRAPHES (texte identique)
   ✓ Garde les MÊMES LISTES (texte identique)
   ✓ NE MODIFIE PAS les textes du client
   ✓ NE CHANGE PAS l'ordre des sections
   ✓ NE SUPPRIME AUCUN contenu

2. DESIGN VISUEL (À MODERNISER):
   ✓ Palette de couleurs MODERNE et HARMONIEUSE pour un·e {self.theme}
   ✓ Typographie élégante (Google Fonts - choisis 2 fonts complémentaires)
   ✓ Layout moderne avec whitespace généreux
   ✓ Design cards/sections avec ombres subtiles et border-radius
   ✓ Dégradés et effets visuels modernes
   ✓ Hero section impactante en haut

3. IMAGES:
   ✓ Utilise les URLs d'images indiquées dans la structure
   ✓ Si pas assez d'images, utilise des placeholders de unsplash.com pertinents pour {self.theme}
   ✓ Intègre-les de manière élégante (object-fit: cover, aspect-ratio, lazy loading)

4. INTERACTIVITÉ:
   ✓ Animations au scroll (fade-in, slide-up avec Intersection Observer)
   ✓ Hover effects sur boutons et cards
   ✓ Navigation smooth scroll
   ✓ Formulaire de contact si section contact (action: formspree.io ou mailto:{email})

5. TECHNOLOGIE:
   ✓ UN SEUL FICHIER HTML (CSS et JS inline dans <style> et <script>)
   ✓ CSS moderne (flexbox, grid, variables CSS, animations)
   ✓ JavaScript vanilla (pas de frameworks)
   ✓ Responsive mobile-first
   ✓ Performance optimisée

6. NAVIGATION:
   ✓ Ajoute une navigation fixe en haut avec liens vers chaque section
   ✓ Liens basés sur les titres de sections

════════════════════════════════════════════════════════════════

RÉSULTAT ATTENDU:
Le client doit dire "C'est mon site mais en mieux !" - même contenu, design professionnel.

Génère maintenant le code HTML complet:
"""

        return prompt

    def _format_structure_for_prompt(self, structure, image_urls):
        """Formate la structure extraite pour le prompt Gemini"""
        if not structure:
            return "Aucune structure trouvée - crée une structure basique"

        formatted = []
        image_index = 0

        for section in structure:
            section_title = section.get('title', 'Section sans titre')
            formatted.append(f"\n--- {section_title.upper()} ---\n")

            for item in section.get('content', []):
                item_type = item.get('type')

                if item_type == 'heading':
                    level = item.get('level', 'h2')
                    text = item.get('text', '')
                    formatted.append(f"{level.upper()}: {text}")

                elif item_type == 'paragraph':
                    text = item.get('text', '')
                    formatted.append(f"Paragraphe: {text}")

                elif item_type == 'list':
                    is_ordered = item.get('ordered', False)
                    items = item.get('items', [])
                    list_type = "Liste ordonnée" if is_ordered else "Liste à puces"
                    formatted.append(f"{list_type}:")
                    for list_item in items:
                        formatted.append(f"  - {list_item}")

                elif item_type == 'quote':
                    text = item.get('text', '')
                    formatted.append(f'Citation: "{text}"')

            # Ajouter une image à cette section si disponible
            if image_index < len(image_urls):
                formatted.append(f"[IMAGE: {image_urls[image_index]}]")
                image_index += 1

            formatted.append("")  # Ligne vide entre sections

        return "\n".join(formatted)

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
        '--data-file',
        type=str,
        help='Chemin vers un fichier scraped_data.json existant (skip le scraping)'
    )

    parser.add_argument(
        '--preview',
        action='store_true',
        help='Ouvrir dans le navigateur après génération'
    )

    args = parser.parse_args()

    # Validation: soit --url soit --data-file doit être fourni
    if not args.url and not args.data_file:
        parser.error("❌ Vous devez fournir soit --url soit --data-file")

    if args.url and args.data_file:
        parser.error("❌ Utilisez soit --url soit --data-file, pas les deux")

    try:
        # Charger les données existantes si --data-file fourni
        existing_data = None
        if args.data_file:
            logger.info(f"📂 Chargement des données depuis: {args.data_file}")
            try:
                with open(args.data_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                logger.info(f"✓ Données chargées avec succès")
            except FileNotFoundError:
                logger.error(f"❌ Fichier introuvable: {args.data_file}")
                print(f"\n💡 Vérifiez que le chemin est correct.")
                print(f"💡 Exemple: temp_files/gemini_therapeute/scraped_data.json")
                return
            except json.JSONDecodeError as e:
                logger.error(f"❌ Erreur JSON: {e}")
                print(f"\n💡 Le fichier n'est pas un JSON valide")
                return

        # Créer le générateur
        generator = GeminiTemplateGenerator(
            theme=args.theme,
            source_url=args.url,  # Peut être None si --data-file
            api_key=args.api_key
        )

        # Générer avec ou sans données existantes
        result = generator.generate(existing_data=existing_data)

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
                if args.data_file:
                    print(f"\n💡 Pour prévisualiser: python -m scripts.gemini_template_generator --data-file {args.data_file} --theme \"{args.theme}\" --preview")
                else:
                    print(f"\n💡 Pour prévisualiser: python -m scripts.gemini_template_generator --url {args.url} --theme \"{args.theme}\" --preview")

            # Info sur la régénération sans rescraping
            if not args.data_file and result.get('data_file'):
                print(f"\n♻️  Pour régénérer sans rescraper:")
                print(f"   python -m scripts.gemini_template_generator --data-file {result['data_file']} --theme \"{args.theme}\"")

            print()
        else:
            print("\n❌ Échec de la génération")

    except Exception as e:
        logger.error(f"❌ Erreur: {str(e)}")
        raise


if __name__ == "__main__":
    main()
