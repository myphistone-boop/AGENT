"""
Gestion des fichiers et dossiers
"""
import shutil
from pathlib import Path
from datetime import datetime
from scripts.utils.logger import setup_logger

logger = setup_logger("file_manager")


class FileManager:
    """Gestionnaire de fichiers pour le projet"""

    def __init__(self, base_dir=None):
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(__file__).resolve().parent.parent.parent

        self.temp_dir = self.base_dir / "temp"
        self.output_dir = self.base_dir / "outputs"
        self.data_dir = self.base_dir / "data"

    def create_client_temp_dir(self, client_id):
        """Crée un dossier temporaire pour un client"""
        client_dir = self.temp_dir / f"client_{client_id}"
        client_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Dossier créé: {client_dir}")
        return client_dir

    def cleanup_client_temp(self, client_id):
        """Nettoie le dossier temporaire d'un client"""
        client_dir = self.temp_dir / f"client_{client_id}"
        if client_dir.exists():
            shutil.rmtree(client_dir)
            logger.debug(f"Dossier nettoyé: {client_dir}")

    def cleanup_all_temp(self):
        """Nettoie tous les fichiers temporaires"""
        if self.temp_dir.exists():
            for item in self.temp_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            logger.info("✅ Tous les fichiers temporaires nettoyés")

    def get_output_path(self, output_type, filename):
        """Retourne le chemin pour un fichier de sortie"""
        output_map = {
            'screenshot': self.output_dir / "screenshots",
            'pdf': self.output_dir / "pdfs",
            'report': self.output_dir / "reports"
        }

        output_folder = output_map.get(output_type, self.output_dir)
        output_folder.mkdir(parents=True, exist_ok=True)

        return output_folder / filename

    def get_prospects_file(self, date=None):
        """Retourne le chemin du fichier prospects pour une date"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        prospects_dir = self.data_dir / "prospects"
        prospects_dir.mkdir(parents=True, exist_ok=True)

        return prospects_dir / f"prospects_{date}.csv"

    def archive_old_files(self, days=30):
        """Archive les fichiers de plus de X jours"""
        # TODO: implémenter archivage si besoin
        pass


if __name__ == "__main__":
    # Test du FileManager
    fm = FileManager()
    print(f"Base dir: {fm.base_dir}")
    print(f"Temp dir: {fm.temp_dir}")

    # Test création dossier client
    client_dir = fm.create_client_temp_dir("001")
    print(f"Client dir créé: {client_dir}")

    # Test cleanup
    fm.cleanup_client_temp("001")
    print("Client dir nettoyé")
