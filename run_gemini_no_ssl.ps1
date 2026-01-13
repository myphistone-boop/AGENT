# Script PowerShell pour lancer le générateur Gemini sans vérification SSL
# À utiliser si vous avez des problèmes de certificats (proxy d'entreprise)

Write-Host "⚠️  MODE SANS VÉRIFICATION SSL (pour proxy d'entreprise)" -ForegroundColor Yellow
Write-Host "=" * 60

# Désactiver la vérification SSL pour Python
$env:PYTHONHTTPSVERIFY = "0"
$env:GRPC_ENABLE_FORK_SUPPORT = "1"
$env:GRPC_VERBOSITY = "ERROR"
$env:SSL_CERT_FILE = ""
$env:REQUESTS_CA_BUNDLE = ""

# Vérifier les arguments
if ($args.Count -lt 4) {
    Write-Host "Usage: .\run_gemini_no_ssl.ps1 --url 'URL' --theme 'THEME'" -ForegroundColor Red
    Write-Host "Exemple: .\run_gemini_no_ssl.ps1 --url 'https://exemple.com' --theme 'thérapeute'" -ForegroundColor Cyan
    exit 1
}

# Lancer le générateur avec les arguments fournis
Write-Host ""
Write-Host "Lancement du générateur..." -ForegroundColor Green
python -m scripts.gemini_template_generator $args
