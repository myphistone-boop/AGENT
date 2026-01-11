"""
Générateur de PDF pour les propositions
"""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image
from scripts.utils.logger import setup_logger
from scripts.utils.file_manager import FileManager

logger = setup_logger("pdf_generator")


class PDFGenerator:
    """Générateur de PDF avec screenshots"""

    def __init__(self):
        self.file_manager = FileManager()
        self.page_width, self.page_height = A4

    def generate_proposal(self, client_id, business_data, screenshots, has_website=True):
        """
        Génère le PDF de proposition

        Args:
            client_id: ID du client
            business_data: Données de l'entreprise (nom, note, etc.)
            screenshots: Dictionnaire avec les chemins des screenshots
            has_website: True si le client a déjà un site (AVANT/APRÈS), False sinon

        Returns:
            str: Chemin vers le PDF généré
        """
        logger.info(f"📄 Génération PDF pour client {client_id}")

        pdf_path = self.file_manager.get_output_path(
            'pdf',
            f"proposition_client_{client_id}.pdf"
        )

        try:
            c = canvas.Canvas(str(pdf_path), pagesize=A4)

            # PAGE 1
            if has_website:
                self._create_comparison_page(c, business_data, screenshots)
            else:
                self._create_new_website_page(c, business_data, screenshots)

            c.showPage()

            # PAGE 2
            self._create_details_page(c, screenshots)
            c.showPage()

            # PAGE 3
            self._create_benefits_page(c, business_data, has_website)
            c.showPage()

            # Finaliser
            c.save()

            logger.info(f"✅ PDF créé: {pdf_path}")
            return str(pdf_path)

        except Exception as e:
            logger.error(f"❌ Erreur génération PDF: {str(e)}")
            return None

    def _create_comparison_page(self, c, data, screenshots):
        """Page 1 : Comparaison AVANT/APRÈS (pour clients avec site)"""
        w, h = self.page_width, self.page_height

        # Titre
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, h - 50, f"{data['name']}")

        c.setFont("Helvetica", 14)
        c.drawString(50, h - 75, "Votre site web réinventé")

        # Labels AVANT / APRÈS
        c.setFont("Helvetica-Bold", 16)

        # AVANT (gauche)
        c.drawString(80, h - 120, "AVANT")
        if 'screenshot_original' in screenshots and screenshots['screenshot_original']:
            self._draw_image(c, screenshots['screenshot_original'], 50, h - 500, 220, 350)

        # APRÈS (droite)
        c.setFillColor(colors.HexColor('#4CAF50'))
        c.drawString(350, h - 120, "APRÈS")
        c.setFillColor(colors.black)

        if 'desktop' in screenshots and screenshots['desktop']:
            self._draw_image(c, screenshots['desktop'], 320, h - 500, 220, 350)

        # Footer
        c.setFont("Helvetica", 10)
        c.drawString(50, 50, f"Proposition pour {data['name']}")

    def _create_new_website_page(self, c, data, screenshots):
        """Page 1 : Proposition pour client SANS site"""
        w, h = self.page_width, self.page_height

        # Titre
        c.setFont("Helvetica-Bold", 24)
        c.drawString(50, h - 50, f"{data['name']}")

        c.setFont("Helvetica", 14)
        c.drawString(50, h - 75, "Votre futur site web")

        # Message
        c.setFont("Helvetica", 12)
        text = "Vous n'avez pas encore de site web. Voici ce que je vous propose :"
        c.drawString(50, h - 110, text)

        # Screenshot du nouveau design
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.HexColor('#4CAF50'))
        c.drawString(50, h - 145, "VOTRE NOUVEAU SITE")
        c.setFillColor(colors.black)

        if 'desktop' in screenshots and screenshots['desktop']:
            self._draw_image(c, screenshots['desktop'], 50, h - 570, 500, 400)

        # Note/avis si disponibles
        if data.get('rating'):
            c.setFont("Helvetica", 10)
            c.drawString(50, h - 590, f"⭐ Note actuelle sur Google : {data['rating']}")
            if data.get('reviews_count'):
                c.drawString(50, h - 605, f"   {data['reviews_count']} avis")

        # Footer
        c.setFont("Helvetica", 10)
        c.drawString(50, 50, f"Proposition pour {data['name']}")

    def _create_details_page(self, c, screenshots):
        """Page 2 : Détails (desktop + mobile)"""
        w, h = self.page_width, self.page_height

        # Titre
        c.setFont("Helvetica-Bold", 20)
        c.drawString(50, h - 50, "Aperçu détaillé")

        # Desktop
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, h - 85, "Vue desktop (ordinateur)")

        if 'desktop' in screenshots and screenshots['desktop']:
            self._draw_image(c, screenshots['desktop'], 50, h - 380, 500, 280)

        # Mobile
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, h - 420, "Vue mobile (smartphone)")

        c.setFont("Helvetica", 10)
        c.drawString(50, h - 435, "100% responsive, parfait sur tous les appareils")

        if 'mobile' in screenshots and screenshots['mobile']:
            self._draw_image(c, screenshots['mobile'], 150, h - 780, 200, 330)

        # Footer
        c.setFont("Helvetica", 10)
        c.drawString(50, 50, "Design moderne et responsive")

    def _create_benefits_page(self, c, data, has_website):
        """Page 3 : Bénéfices + CTA"""
        w, h = self.page_width, self.page_height

        # Titre
        c.setFont("Helvetica-Bold", 22)

        if has_website:
            c.drawString(50, h - 50, "Ce qui change :")
        else:
            c.drawString(50, h - 50, "Pourquoi avoir un site web en 2025 ?")

        # Bénéfices
        c.setFont("Helvetica", 13)
        y = h - 100

        if has_website:
            benefits = [
                "✓ Design moderne qui inspire confiance",
                "✓ Navigation intuitive et fluide",
                "✓ Optimisé pour mobile (80% de vos visiteurs)",
                "✓ Temps de chargement ultra-rapide",
                "✓ Formulaire de contact optimisé",
                "✓ SEO amélioré pour meilleure visibilité Google"
            ]
        else:
            benefits = [
                "✓ 78% des clients cherchent en ligne avant de visiter",
                "✓ Disponible 24/7 pour prendre des rendez-vous",
                "✓ Meilleure visibilité sur Google",
                "✓ Crédibilité professionnelle renforcée",
                "✓ Vos concurrents en ont déjà un !",
                "✓ Automatisation de la prise de contact"
            ]

        for benefit in benefits:
            c.drawString(70, y, benefit)
            y -= 30

        # CTA
        y -= 50
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, y, "INTÉRESSÉ ?")

        c.setFont("Helvetica", 13)
        y -= 35
        c.drawString(50, y, "Répondez simplement à l'email et je vous montre")
        y -= 20
        c.drawString(50, y, "la version interactive en live.")

        # Stats supplémentaires
        if not has_website:
            y -= 80
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(colors.HexColor('#FF5722'))
            c.drawString(50, y, "📊 Le saviez-vous ?")
            c.setFillColor(colors.black)

            c.setFont("Helvetica", 11)
            y -= 25
            c.drawString(70, y, "• 97% des consommateurs cherchent en ligne avant d'acheter")
            y -= 20
            c.drawString(70, y, "• Un site professionnel augmente la crédibilité de 75%")
            y -= 20
            c.drawString(70, y, "• 60% des clients ne contactent pas une entreprise sans site")

        # Footer
        c.setFont("Helvetica", 10)
        c.drawString(50, 50, f"Proposition personnalisée pour {data['name']}")

    def _draw_image(self, c, img_path, x, y, max_width, max_height):
        """Dessine une image redimensionnée pour tenir dans les limites"""
        try:
            img = Image.open(img_path)
            img_width, img_height = img.size

            # Calculer le ratio
            ratio = min(max_width / img_width, max_height / img_height)

            new_width = img_width * ratio
            new_height = img_height * ratio

            # Dessiner
            c.drawImage(img_path, x, y, width=new_width, height=new_height, preserveAspectRatio=True)

        except Exception as e:
            logger.warning(f"⚠️  Impossible de dessiner l'image: {str(e)}")
            # Dessiner un rectangle de substitution
            c.setStrokeColor(colors.grey)
            c.rect(x, y, max_width, max_height)
            c.setFont("Helvetica", 10)
            c.drawString(x + 10, y + max_height/2, "Image non disponible")


def main():
    """Test du générateur PDF"""
    import argparse

    parser = argparse.ArgumentParser(description='Générateur de PDF')
    parser.add_argument('--client-id', type=str, default='test', help='ID client')
    parser.add_argument('--desktop', type=str, required=True, help='Screenshot desktop')
    parser.add_argument('--mobile', type=str, help='Screenshot mobile')
    parser.add_argument('--original', type=str, help='Screenshot original (AVANT)')
    parser.add_argument('--name', type=str, default='Entreprise Test', help='Nom entreprise')

    args = parser.parse_args()

    business_data = {
        'name': args.name,
        'rating': '4.5',
        'reviews_count': '87'
    }

    screenshots = {
        'desktop': args.desktop,
        'mobile': args.mobile,
        'screenshot_original': args.original
    }

    has_website = bool(args.original)

    generator = PDFGenerator()
    pdf_path = generator.generate_proposal(
        args.client_id,
        business_data,
        screenshots,
        has_website
    )

    if pdf_path:
        print(f"\n{'='*60}")
        print(f"✅ PDF CRÉÉ")
        print(f"{'='*60}\n")

        print(f"Fichier: {pdf_path}")
        print(f"Type: {'Avant/Après' if has_website else 'Nouveau site'}")

    else:
        print("❌ Échec de la génération")


if __name__ == "__main__":
    main()
