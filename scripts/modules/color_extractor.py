"""
Extraction de palette de couleurs depuis une image (logo)
"""
from pathlib import Path
from colorthief import ColorThief
from PIL import Image
from scripts.utils.logger import setup_logger
from config import settings

logger = setup_logger("color_extractor")


class ColorExtractor:
    """Extracteur de palette de couleurs"""

    def __init__(self):
        pass

    def extract_from_logo(self, logo_path, num_colors=5):
        """
        Extrait la palette de couleurs d'un logo

        Args:
            logo_path: Chemin vers le logo
            num_colors: Nombre de couleurs à extraire

        Returns:
            dict: Palette avec couleurs primaires, secondaires, accent
        """
        logo_path = Path(logo_path)

        if not logo_path.exists():
            logger.warning(f"⚠️  Logo introuvable: {logo_path}")
            return None

        logger.info(f"🎨 Extraction couleurs de: {logo_path.name}")

        try:
            # Vérifier que l'image est valide
            img = Image.open(logo_path)

            # Convertir en RGB si nécessaire
            if img.mode != 'RGB':
                # Créer fond blanc pour transparence
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)

                # Sauvegarder temporairement
                temp_path = logo_path.parent / f"temp_{logo_path.name}"
                rgb_img.save(temp_path, 'PNG')
                logo_path = temp_path

            # Extraire les couleurs dominantes
            color_thief = ColorThief(str(logo_path))
            palette = color_thief.get_palette(color_count=num_colors, quality=1)

            # Filtrer les couleurs trop claires ou trop sombres
            palette = self._filter_colors(palette)

            if len(palette) < 3:
                logger.warning("⚠️  Pas assez de couleurs, utilisation palette par défaut")
                return None

            # Construire la palette CSS
            colors = {
                'primary': self._rgb_to_hex(palette[0]),
                'secondary': self._rgb_to_hex(palette[1]),
                'accent': self._rgb_to_hex(palette[2] if len(palette) > 2 else palette[1])
            }

            logger.info(f"✅ Palette extraite: {colors}")
            return colors

        except Exception as e:
            logger.error(f"❌ Erreur extraction couleurs: {str(e)}")
            return None

    def _filter_colors(self, palette):
        """Filtre les couleurs trop claires ou trop sombres"""
        filtered = []

        for color in palette:
            r, g, b = color

            # Calculer la luminosité
            luminosity = (0.299 * r + 0.587 * g + 0.114 * b)

            # Garder seulement si ni trop sombre ni trop clair
            if 30 < luminosity < 240:
                filtered.append(color)

        return filtered if filtered else palette  # Si tout filtré, garder original

    def _rgb_to_hex(self, rgb):
        """Convertit RGB en HEX"""
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

    def get_default_palette(self, sector):
        """Retourne la palette par défaut pour un secteur"""
        palette = settings.DEFAULT_COLORS.get(sector, settings.DEFAULT_COLORS['commerce'])
        logger.info(f"🎨 Palette par défaut ({sector}): {palette}")
        return palette


def main():
    """Test de l'extracteur"""
    import argparse

    parser = argparse.ArgumentParser(description='Extracteur de couleurs')
    parser.add_argument('--logo', type=str, required=True, help='Chemin vers le logo')
    parser.add_argument('--colors', type=int, default=5, help='Nombre de couleurs')

    args = parser.parse_args()

    extractor = ColorExtractor()
    colors = extractor.extract_from_logo(args.logo, args.colors)

    if colors:
        print(f"\n{'='*60}")
        print(f"🎨 PALETTE EXTRAITE")
        print(f"{'='*60}\n")

        print(f"Primary:   {colors['primary']}")
        print(f"Secondary: {colors['secondary']}")
        print(f"Accent:    {colors['accent']}")

        # Générer un aperçu HTML
        html = f"""
        <div style="display: flex; gap: 20px;">
            <div style="width: 100px; height: 100px; background: {colors['primary']};"></div>
            <div style="width: 100px; height: 100px; background: {colors['secondary']};"></div>
            <div style="width: 100px; height: 100px; background: {colors['accent']};"></div>
        </div>
        """

        preview_file = Path('outputs/reports/color_preview.html')
        preview_file.parent.mkdir(parents=True, exist_ok=True)
        preview_file.write_text(html, encoding='utf-8')

        print(f"\n👁️  Aperçu généré: {preview_file}")

    else:
        print("❌ Impossible d'extraire les couleurs")


if __name__ == "__main__":
    main()
