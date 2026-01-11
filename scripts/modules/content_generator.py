"""
Générateur de contenu avec Claude AI
Pour les clients sans site web
"""
import json
from anthropic import Anthropic
from scripts.utils.logger import setup_logger
from config import settings

logger = setup_logger("content_generator")


class ContentGenerator:
    """Générateur de contenu IA pour sites web"""

    def __init__(self):
        self.client = None

        if settings.ANTHROPIC_API_KEY:
            self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            logger.info("✅ Claude AI initialisé")
        else:
            logger.warning("⚠️  Clé Claude API manquante - génération IA désactivée")

    def generate_website_content(self, business_name, category, city):
        """
        Génère le contenu complet pour un site web

        Args:
            business_name: Nom de l'entreprise
            category: Type d'activité (ex: "Salon de coiffure")
            city: Ville

        Returns:
            dict: Contenu généré (slogan, services, textes, etc.)
        """
        if not self.client:
            logger.error("❌ Claude AI non disponible")
            return self._get_fallback_content(business_name, category)

        logger.info(f"🤖 Génération contenu pour: {business_name}")

        prompt = self._build_prompt(business_name, category, city)

        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1500,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            # Extraire le JSON de la réponse
            content_text = response.content[0].text

            # Parser le JSON
            content = json.loads(content_text)

            logger.info("✅ Contenu généré avec succès")
            return content

        except json.JSONDecodeError as e:
            logger.error(f"❌ Erreur parsing JSON: {str(e)}")
            logger.debug(f"Réponse brute: {content_text}")
            return self._get_fallback_content(business_name, category)

        except Exception as e:
            logger.error(f"❌ Erreur génération IA: {str(e)}")
            return self._get_fallback_content(business_name, category)

    def _build_prompt(self, business_name, category, city):
        """Construit le prompt pour Claude"""
        return f"""Tu es un rédacteur web expert spécialisé dans la création de contenu pour sites web de petites entreprises.

Crée le contenu complet pour la page d'accueil d'un site web avec ces informations :

**Nom de l'entreprise :** {business_name}
**Type d'activité :** {category}
**Localisation :** {city}

Génère un contenu professionnel, engageant et adapté au secteur d'activité.

Retourne UNIQUEMENT un objet JSON valide avec cette structure exacte (sans texte avant ou après) :

{{
  "slogan": "Un slogan accrocheur de 5-8 mots",
  "hero_subtitle": "Une phrase d'accroche engageante de 10-15 mots",
  "services": [
    {{
      "title": "Nom du service 1",
      "description": "Description courte du service (20-30 mots)"
    }},
    {{
      "title": "Nom du service 2",
      "description": "Description courte du service (20-30 mots)"
    }},
    {{
      "title": "Nom du service 3",
      "description": "Description courte du service (20-30 mots)"
    }}
  ],
  "about": "Texte de présentation de l'entreprise (40-60 mots, ton chaleureux et professionnel)",
  "cta": "Texte du call-to-action (2-3 mots)"
}}

Règles importantes :
- Utilise un ton professionnel mais chaleureux
- Adapte le vocabulaire au secteur d'activité
- Mets en avant les bénéfices pour le client
- Le slogan doit être mémorable et unique
- Les services doivent être concrets et pertinents
- Le CTA doit inciter à l'action

Retourne UNIQUEMENT le JSON, rien d'autre."""

    def _get_fallback_content(self, business_name, category):
        """Contenu de secours si l'IA ne fonctionne pas"""
        logger.info("📝 Utilisation contenu de secours")

        return {
            "slogan": f"Bienvenue chez {business_name}",
            "hero_subtitle": f"Votre spécialiste {category} à votre service",
            "services": [
                {
                    "title": "Service de qualité",
                    "description": "Nous offrons des services professionnels adaptés à vos besoins"
                },
                {
                    "title": "Expertise reconnue",
                    "description": "Notre équipe expérimentée vous garantit un travail soigné"
                },
                {
                    "title": "Satisfaction client",
                    "description": "Votre satisfaction est notre priorité absolue"
                }
            ],
            "about": f"{business_name} vous accueille pour vous offrir des services de qualité. "
                     f"Notre équipe met son expertise à votre service pour vous garantir satisfaction.",
            "cta": "Contactez-nous"
        }

    def improve_text(self, original_text, context=""):
        """
        Améliore un texte existant (pour clients avec site)

        Args:
            original_text: Texte original
            context: Contexte (optionnel)

        Returns:
            str: Texte amélioré
        """
        if not self.client:
            return original_text

        logger.info("✨ Amélioration de texte...")

        prompt = f"""Tu es un rédacteur web expert.

Réécris ce texte de manière plus percutante et engageante, tout en gardant le même message :

"{original_text}"

{f'Contexte : {context}' if context else ''}

Règles :
- Garde le même sens
- Maximum 15 mots
- Ton professionnel mais chaleureux
- Plus dynamique et accrocheur

Retourne UNIQUEMENT le texte réécrit, sans guillemets ni explications."""

        try:
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",  # Haiku pour coût réduit
                max_tokens=100,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            improved = response.content[0].text.strip()
            logger.info("✅ Texte amélioré")
            return improved

        except Exception as e:
            logger.error(f"❌ Erreur amélioration: {str(e)}")
            return original_text


def main():
    """Test du générateur"""
    import argparse

    parser = argparse.ArgumentParser(description='Générateur de contenu IA')
    parser.add_argument('--name', type=str, required=True, help='Nom entreprise')
    parser.add_argument('--category', type=str, required=True, help='Catégorie')
    parser.add_argument('--city', type=str, default='Paris', help='Ville')

    args = parser.parse_args()

    generator = ContentGenerator()
    content = generator.generate_website_content(args.name, args.category, args.city)

    print(f"\n{'='*60}")
    print(f"🤖 CONTENU GÉNÉRÉ POUR: {args.name}")
    print(f"{'='*60}\n")

    print(f"Slogan: {content['slogan']}")
    print(f"Subtitle: {content['hero_subtitle']}")
    print(f"\nServices:")
    for i, service in enumerate(content['services'], 1):
        print(f"  {i}. {service['title']}")
        print(f"     {service['description']}")
    print(f"\nÀ propos:\n{content['about']}")
    print(f"\nCTA: {content['cta']}")

    # Sauvegarder
    from pathlib import Path
    output_file = Path('outputs/reports/generated_content.json')
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Sauvegardé: {output_file}")


if __name__ == "__main__":
    main()
