#!/bin/sh

# Hacer ejecutables los hooks
chmod +x .githooks/commit-msg
chmod +x .githooks/pre-commit

# Configurar Git para usar esta carpeta de hooks
git config core.hooksPath .githooks

echo "Hooks instalados correctamente!" 