"""
Module d'envoi d'emails via Gmail SMTP
"""
import smtplib
import time
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from scripts.utils.logger import setup_logger
from config import settings

logger = setup_logger("email_sender")


class EmailSender:
    """Envoyeur d'emails via Gmail SMTP"""

    def __init__(self):
        # Vérifier la configuration Gmail
        if not settings.GMAIL_ADDRESS:
            logger.error("❌ GMAIL_ADDRESS manquante dans .env")
            self.configured = False
        elif not settings.GMAIL_APP_PASSWORD:
            logger.error("❌ GMAIL_APP_PASSWORD manquante dans .env")
            self.configured = False
        else:
            self.configured = True
            logger.info(f"✅ Gmail initialisé ({settings.GMAIL_ADDRESS})")

    def send_proposal(self, to_email, business_data, pdf_path, screenshot_path=None, has_website=True):
        """
        Envoie l'email de proposition

        Args:
            to_email: Email du destinataire
            business_data: Données de l'entreprise (nom, etc.)
            pdf_path: Chemin vers le PDF
            screenshot_path: Chemin vers screenshot de comparaison (optionnel)
            has_website: True si client a déjà un site

        Returns:
            bool: True si envoyé avec succès
        """
        if not self.configured:
            logger.error("❌ Gmail non configuré")
            return False

        logger.info(f"📧 Envoi email à: {to_email}")

        try:
            # Créer le message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{settings.FROM_NAME} <{settings.GMAIL_ADDRESS}>"
            msg['To'] = to_email
            msg['Subject'] = self._generate_subject(business_data, has_website)

            # Corps HTML
            html_content = self._generate_html_body(business_data, has_website)
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)

            # Attacher le PDF
            self._attach_pdf(msg, pdf_path, business_data['name'])

            # Se connecter au serveur Gmail
            logger.debug("📡 Connexion au serveur Gmail...")

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Sécuriser la connexion

                # Connexion avec mot de passe d'application
                server.login(settings.GMAIL_ADDRESS, settings.GMAIL_APP_PASSWORD)

                # Envoyer
                server.send_message(msg)

            logger.info(f"✅ Email envoyé avec succès via Gmail")

            # Délai pour éviter rate limiting
            time.sleep(settings.DELAY_BETWEEN_EMAILS)

            return True

        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"❌ Erreur d'authentification Gmail: {str(e)}")
            logger.error("💡 Vérifiez que vous utilisez un 'Mot de passe d'application' et non votre mot de passe Gmail")
            logger.error("💡 Guide: https://support.google.com/accounts/answer/185833")
            return False

        except smtplib.SMTPException as e:
            logger.error(f"❌ Erreur SMTP: {str(e)}")
            return False

        except Exception as e:
            logger.error(f"❌ Erreur envoi email: {str(e)}")
            return False

    def _generate_subject(self, data, has_website):
        """Génère le sujet de l'email"""
        name = data['name']

        if has_website:
            return f"Une nouvelle vision pour {name}"
        else:
            return f"{name} - Votre entreprise mérite un site web"

    def _generate_html_body(self, data, has_website):
        """Génère le corps HTML de l'email"""
        name = data['name']
        first_name = name.split()[0] if name else "Bonjour"

        if has_website:
            # Email pour client AVEC site
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        h2 {{
            color: #2c3e50;
        }}
        .highlight {{
            color: #4CAF50;
            font-weight: bold;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <p>Bonjour,</p>

        <p>Je suis tombé sur <strong>{name}</strong> en cherchant dans votre secteur,
        et votre entreprise m'a inspiré un petit projet créatif.</p>

        <p>J'ai repris vos contenus et vos visuels pour imaginer à quoi pourrait
        ressembler votre site web avec un design plus <span class="highlight">moderne et responsive</span>.</p>

        <p>Je me suis dit que ça pourrait vous intéresser.</p>

        <p>📎 <strong>Le PDF ci-joint</strong> contient la comparaison avant/après,
        avec des vues desktop et mobile.</p>

        <p>Si le concept vous plaît, <strong>répondez-moi</strong> et je vous montre
        la version interactive en live.</p>

        <p>Bien à vous,</p>
        <p><strong>{settings.FROM_NAME}</strong><br>
        {settings.GMAIL_ADDRESS}</p>

        <div class="footer">
            <p><em>P.S. : Aucune obligation, c'était juste un exercice créatif
            qui me semblait valoir le partage 😊</em></p>
        </div>
    </div>
</body>
</html>
"""
        else:
            # Email pour client SANS site
            rating_text = ""
            if data.get('rating'):
                rating_text = f"<p>Avec une note de <strong>{data['rating']}⭐</strong>"
                if data.get('reviews_count'):
                    rating_text += f" ({data['reviews_count']} avis)"
                rating_text += ", vous méritez une vitrine en ligne à la hauteur !</p>"

            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        h2 {{
            color: #2c3e50;
        }}
        .highlight {{
            color: #FF5722;
            font-weight: bold;
        }}
        .stat {{
            background: #f5f5f5;
            padding: 15px;
            border-left: 4px solid #4CAF50;
            margin: 20px 0;
        }}
        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            font-size: 0.9em;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <p>Bonjour,</p>

        <p>J'ai remarqué <strong>{name}</strong> sur Google Maps et j'ai constaté
        que vous n'avez pas encore de site web.</p>

        {rating_text}

        <div class="stat">
            <strong>Le saviez-vous ?</strong><br>
            <span class="highlight">78% des clients</span> cherchent en ligne avant
            de visiter un établissement. Sans site web, vous passez à côté d'opportunités.
        </div>

        <p>Je me suis permis de créer une <strong>proposition de site web</strong>
        pour vous, en utilisant vos photos Google Maps et en créant un design
        adapté à votre activité.</p>

        <p>📎 <strong>Le PDF ci-joint</strong> vous montre le résultat.</p>

        <p>Si ça vous parle, <strong>répondez-moi</strong> et je vous montre
        la version interactive en live.</p>

        <p>Bien à vous,</p>
        <p><strong>{settings.FROM_NAME}</strong><br>
        {settings.GMAIL_ADDRESS}</p>

        <div class="footer">
            <p><em>P.S. : Aucune obligation, juste une opportunité à saisir
            avant vos concurrents ! 🚀</em></p>
        </div>
    </div>
</body>
</html>
"""

        return html

    def _attach_pdf(self, message, pdf_path, business_name):
        """Attache le PDF au message"""
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            logger.warning(f"⚠️  PDF introuvable: {pdf_path}")
            return

        # Lire le PDF
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()

        # Créer l'attachment
        part = MIMEBase('application', 'pdf')
        part.set_payload(pdf_data)
        encoders.encode_base64(part)

        # Nom de fichier propre
        safe_name = "".join(c for c in business_name if c.isalnum() or c in (' ', '-', '_'))
        filename = f"{safe_name}_nouveau_site.pdf"

        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {filename}'
        )

        message.attach(part)
        logger.debug(f"📎 PDF attaché: {filename}")


def main():
    """Test de l'envoyeur d'email"""
    import argparse

    parser = argparse.ArgumentParser(description='Test envoi email via Gmail')
    parser.add_argument('--to', type=str, required=True, help='Email destinataire')
    parser.add_argument('--pdf', type=str, required=True, help='Chemin vers PDF')
    parser.add_argument('--name', type=str, default='Entreprise Test', help='Nom entreprise')
    parser.add_argument('--has-website', action='store_true', help='Client a déjà un site')

    args = parser.parse_args()

    business_data = {
        'name': args.name,
        'rating': '4.5',
        'reviews_count': '87'
    }

    sender = EmailSender()
    success = sender.send_proposal(
        args.to,
        business_data,
        args.pdf,
        has_website=args.has_website
    )

    if success:
        print(f"\n✅ Email envoyé avec succès à {args.to}")
    else:
        print(f"\n❌ Échec de l'envoi")


if __name__ == "__main__":
    main()
