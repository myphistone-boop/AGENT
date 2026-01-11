"""
Générateur de screenshots (desktop et mobile)
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from scripts.utils.logger import setup_logger
from scripts.utils.file_manager import FileManager
from config import settings

logger = setup_logger("screenshot")


class ScreenshotMaker:
    """Générateur de screenshots"""

    def __init__(self):
        self.file_manager = FileManager()

    def capture_website(self, html_path, client_id, output_prefix="generated"):
        """
        Capture des screenshots d'un fichier HTML

        Args:
            html_path: Chemin vers le fichier HTML
            client_id: ID du client
            output_prefix: Préfixe pour les fichiers de sortie

        Returns:
            dict: Chemins vers les screenshots (desktop, mobile)
        """
        html_path = Path(html_path)

        if not html_path.exists():
            logger.error(f"❌ Fichier HTML introuvable: {html_path}")
            return None

        logger.info(f"📸 Capture screenshots: {html_path.name}")

        # Créer les chemins de sortie
        desktop_path = self.file_manager.get_output_path(
            'screenshot',
            f"client_{client_id}_{output_prefix}_desktop.png"
        )

        mobile_path = self.file_manager.get_output_path(
            'screenshot',
            f"client_{client_id}_{output_prefix}_mobile.png"
        )

        try:
            playwright = sync_playwright().start()

            browser_args = {
                "headless": True,
                "args": ['--disable-blink-features=AutomationControlled']
            }

            # Proxy si configuré
            if settings.HTTP_PROXY or settings.HTTPS_PROXY:
                proxy_url = settings.HTTPS_PROXY or settings.HTTP_PROXY
                browser_args["proxy"] = {"server": proxy_url}

            browser = playwright.chromium.launch(**browser_args)

            context_args = {}
            if not settings.VERIFY_SSL:
                context_args["ignore_https_errors"] = True

            context = browser.new_context(**context_args)
            page = context.new_page()

            # Charger le fichier HTML
            file_url = f"file://{html_path.absolute()}"
            page.goto(file_url, wait_until="networkidle", timeout=30000)

            # Screenshot DESKTOP
            logger.debug("📸 Screenshot desktop...")
            page.set_viewport_size({"width": 1920, "height": 1080})
            page.screenshot(path=str(desktop_path), full_page=True)

            # Screenshot MOBILE
            logger.debug("📸 Screenshot mobile...")
            page.set_viewport_size({"width": 375, "height": 812})
            page.screenshot(path=str(mobile_path), full_page=True)

            browser.close()
            playwright.stop()

            logger.info(f"✅ Screenshots créés")

            return {
                'desktop': str(desktop_path),
                'mobile': str(mobile_path)
            }

        except Exception as e:
            logger.error(f"❌ Erreur capture: {str(e)}")
            return None

    def create_comparison_image(self, original_path, new_path, output_path):
        """
        Crée une image de comparaison AVANT/APRÈS

        Args:
            original_path: Screenshot du site original
            new_path: Screenshot du nouveau design
            output_path: Chemin de sortie

        Returns:
            str: Chemin de l'image de comparaison
        """
        try:
            from PIL import Image, ImageDraw, ImageFont

            logger.info("🖼️  Création image comparaison...")

            # Charger les images
            img_original = Image.open(original_path)
            img_new = Image.open(new_path)

            # Redimensionner pour avoir la même hauteur
            target_height = 800
            aspect_original = img_original.width / img_original.height
            aspect_new = img_new.width / img_new.height

            new_width_original = int(target_height * aspect_original)
            new_width_new = int(target_height * aspect_new)

            img_original = img_original.resize((new_width_original, target_height))
            img_new = img_new.resize((new_width_new, target_height))

            # Créer l'image combinée
            gap = 40  # Espace entre les images
            total_width = new_width_original + gap + new_width_new
            total_height = target_height + 100  # +100 pour les labels

            combined = Image.new('RGB', (total_width, total_height), 'white')

            # Coller les images
            combined.paste(img_original, (0, 80))
            combined.paste(img_new, (new_width_original + gap, 80))

            # Ajouter les labels
            draw = ImageDraw.Draw(combined)

            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
            except:
                font = ImageFont.load_default()

            # Label AVANT
            draw.text((new_width_original // 2 - 60, 20), "AVANT", fill='black', font=font)

            # Label APRÈS
            draw.text((new_width_original + gap + new_width_new // 2 - 60, 20), "APRÈS", fill='#4CAF50', font=font)

            # Sauvegarder
            combined.save(output_path)

            logger.info(f"✅ Image comparaison créée: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"❌ Erreur création comparaison: {str(e)}")
            return None


def main():
    """Test du screenshot maker"""
    import argparse

    parser = argparse.ArgumentParser(description='Générateur de screenshots')
    parser.add_argument('--html', type=str, required=True, help='Chemin vers le fichier HTML')
    parser.add_argument('--client-id', type=str, default='test', help='ID client')

    args = parser.parse_args()

    maker = ScreenshotMaker()
    screenshots = maker.capture_website(args.html, args.client_id)

    if screenshots:
        print(f"\n{'='*60}")
        print(f"✅ SCREENSHOTS CRÉÉS")
        print(f"{'='*60}\n")

        print(f"Desktop: {screenshots['desktop']}")
        print(f"Mobile:  {screenshots['mobile']}")

    else:
        print("❌ Échec de la capture")


if __name__ == "__main__":
    main()
