"""
Analyseur de sites web - Évalue si un site est moderne ou daté
"""
import re
from bs4 import BeautifulSoup
from scripts.utils.logger import setup_logger

logger = setup_logger("website_analyzer")


class WebsiteAnalyzer:
    """Analyse la qualité et modernité d'un site web"""

    def __init__(self):
        self.score = 0
        self.max_score = 100
        self.issues = []
        self.strengths = []

    def analyze(self, html_content, site_data):
        """
        Analyse complète d'un site web

        Args:
            html_content: Code HTML du site
            site_data: Données extraites par le scraper

        Returns:
            dict: Rapport d'analyse avec score et recommandations
        """
        logger.info("🔍 Analyse du site web...")

        soup = BeautifulSoup(html_content, 'html.parser')

        # Réinitialiser
        self.score = 0
        self.issues = []
        self.strengths = []

        # Critères d'évaluation
        self._analyze_html_structure(soup)
        self._analyze_responsive_design(soup)
        self._analyze_colors_and_design(soup, site_data)
        self._analyze_content_quality(site_data)
        self._analyze_modern_features(soup)
        self._analyze_performance(soup)

        # Calcul score final
        final_score = min(self.score, self.max_score)

        # Déterminer si le site est daté
        is_outdated = final_score < 60
        quality = self._get_quality_label(final_score)

        report = {
            'score': final_score,
            'quality': quality,
            'is_outdated': is_outdated,
            'issues': self.issues,
            'strengths': self.strengths,
            'recommendation': self._get_recommendation(final_score)
        }

        logger.info(f"📊 Score: {final_score}/100 - {quality}")
        logger.info(f"   Daté: {'OUI ⚠️' if is_outdated else 'NON ✅'}")

        return report

    def _analyze_html_structure(self, soup):
        """Évalue la structure HTML moderne"""
        # HTML5 semantic tags
        semantic_tags = ['header', 'nav', 'main', 'section', 'article', 'aside', 'footer']
        found_semantic = sum(1 for tag in semantic_tags if soup.find(tag))

        if found_semantic >= 5:
            self.score += 10
            self.strengths.append("Structure HTML5 sémantique")
        elif found_semantic >= 3:
            self.score += 5
        else:
            self.issues.append("Structure HTML obsolète (pas de tags sémantiques)")

        # Meta viewport (responsive)
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        if viewport:
            self.score += 5
            self.strengths.append("Meta viewport présent (responsive)")
        else:
            self.issues.append("Pas de meta viewport (site non-responsive)")

        # Doctype HTML5
        doctype = str(soup).lower()
        if '<!doctype html>' in doctype:
            self.score += 5
        else:
            self.issues.append("Doctype obsolète")

    def _analyze_responsive_design(self, soup):
        """Évalue le design responsive"""
        # Media queries dans CSS
        style_tags = soup.find_all('style')
        link_tags = soup.find_all('link', rel='stylesheet')

        has_media_queries = False
        for style in style_tags:
            if '@media' in str(style):
                has_media_queries = True
                break

        if has_media_queries:
            self.score += 10
            self.strengths.append("Media queries CSS (design responsive)")
        else:
            self.issues.append("Pas de media queries (design fixe)")

        # Grid/Flexbox
        page_text = str(soup)
        if 'display: grid' in page_text or 'display:grid' in page_text:
            self.score += 5
            self.strengths.append("CSS Grid utilisé")
        if 'display: flex' in page_text or 'display:flex' in page_text:
            self.score += 5
            self.strengths.append("Flexbox utilisé")

    def _analyze_colors_and_design(self, soup, site_data):
        """Évalue les couleurs et le design visuel"""
        page_text = str(soup).lower()

        # Gradients modernes
        if 'linear-gradient' in page_text or 'radial-gradient' in page_text:
            self.score += 5
            self.strengths.append("Dégradés modernes utilisés")

        # Animations CSS
        if '@keyframes' in page_text or 'animation:' in page_text:
            self.score += 5
            self.strengths.append("Animations CSS présentes")

        # Shadows/depth
        if 'box-shadow' in page_text or 'text-shadow' in page_text:
            self.score += 5
            self.strengths.append("Effets d'ombre (profondeur)")

        # Fonts modernes
        if 'google' in page_text and 'fonts' in page_text:
            self.score += 5
            self.strengths.append("Google Fonts utilisé")

        # Vérifier si le design semble vieux (tables layout, frames)
        if soup.find('table', attrs={'width': True, 'height': True}):
            self.issues.append("Layout en tables (très obsolète)")
            self.score -= 10

        if soup.find('frame') or soup.find('frameset'):
            self.issues.append("Frames utilisés (obsolète depuis 1990s)")
            self.score -= 15

    def _analyze_content_quality(self, site_data):
        """Évalue la qualité du contenu"""
        # Logo
        if site_data.get('logo'):
            self.score += 5
            self.strengths.append("Logo présent")
        else:
            self.issues.append("Pas de logo identifiable")

        # Images
        images = site_data.get('images', [])
        if len(images) >= 3:
            self.score += 5
            self.strengths.append(f"{len(images)} images de qualité")
        elif len(images) == 0:
            self.issues.append("Aucune image (site vide)")
            self.score -= 5

        # Textes
        texts = site_data.get('texts', [])
        if len(texts) >= 3:
            self.score += 5
        else:
            self.issues.append("Peu de contenu textuel")

        # Description/slogan
        if site_data.get('description'):
            self.score += 5
        else:
            self.issues.append("Pas de description/slogan")

    def _analyze_modern_features(self, soup):
        """Évalue les fonctionnalités modernes"""
        page_text = str(soup).lower()

        # JavaScript frameworks modernes
        if 'react' in page_text or 'vue' in page_text or 'angular' in page_text:
            self.score += 10
            self.strengths.append("Framework JS moderne détecté")

        # CDN moderne
        if 'cdn' in page_text:
            self.score += 3

        # Icons modernes (Font Awesome, etc.)
        if 'fontawesome' in page_text or 'material-icons' in page_text:
            self.score += 3
            self.strengths.append("Bibliothèque d'icônes moderne")

        # Lazy loading images
        if 'loading="lazy"' in page_text:
            self.score += 5
            self.strengths.append("Lazy loading images")

    def _analyze_performance(self, soup):
        """Évalue la performance"""
        # Scripts inline (mauvaise pratique)
        inline_scripts = soup.find_all('script', src=None)
        if len(inline_scripts) > 5:
            self.issues.append(f"Trop de scripts inline ({len(inline_scripts)})")
            self.score -= 3

        # Trop de requêtes externes
        external_scripts = soup.find_all('script', src=True)
        external_styles = soup.find_all('link', rel='stylesheet')
        total_external = len(external_scripts) + len(external_styles)

        if total_external > 20:
            self.issues.append(f"Trop de ressources externes ({total_external})")
            self.score -= 5

    def _get_quality_label(self, score):
        """Retourne le label de qualité selon le score"""
        if score >= 80:
            return "Excellent (moderne)"
        elif score >= 60:
            return "Correct (quelques améliorations possibles)"
        elif score >= 40:
            return "Moyen (design daté)"
        else:
            return "Faible (très daté, refonte nécessaire)"

    def _get_recommendation(self, score):
        """Retourne une recommandation"""
        if score >= 80:
            return "Site moderne, juste quelques optimisations mineures"
        elif score >= 60:
            return "Site correct, mais pourrait bénéficier d'une modernisation visuelle"
        elif score >= 40:
            return "Site daté, refonte visuelle recommandée"
        else:
            return "Site très obsolète, refonte complète nécessaire"


def main():
    """Test de l'analyseur"""
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description='Analyseur de site web')
    parser.add_argument('--html', type=str, required=True, help='Fichier HTML à analyser')

    args = parser.parse_args()

    # Lire le fichier
    html_path = Path(args.html)
    if not html_path.exists():
        print(f"❌ Fichier introuvable: {args.html}")
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Analyser
    analyzer = WebsiteAnalyzer()
    report = analyzer.analyze(html_content, {})

    # Afficher le rapport
    print(f"\n{'='*60}")
    print(f"📊 ANALYSE DU SITE WEB")
    print(f"{'='*60}\n")
    print(f"Score: {report['score']}/100")
    print(f"Qualité: {report['quality']}")
    print(f"Site daté: {'OUI ⚠️' if report['is_outdated'] else 'NON ✅'}")
    print(f"\n{report['recommendation']}")

    if report['strengths']:
        print(f"\n✅ Points forts:")
        for strength in report['strengths']:
            print(f"   • {strength}")

    if report['issues']:
        print(f"\n⚠️  Problèmes détectés:")
        for issue in report['issues']:
            print(f"   • {issue}")


if __name__ == "__main__":
    main()
