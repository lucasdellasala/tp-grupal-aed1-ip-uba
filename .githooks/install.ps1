# Hacer ejecutables los hooks (en Windows esto no es necesario)
icacls .githooks/commit-msg /grant Everyone:F
icacls .githooks/pre-commit /grant Everyone:F

# Configurar Git para usar esta carpeta de hooks
git config core.hooksPath .githooks

Write-Host "Hooks instalados correctamente!" 