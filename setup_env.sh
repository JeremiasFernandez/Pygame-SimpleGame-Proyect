#!/bin/bash
# =============================================================
# Crear y activar entorno virtual para Bossfight: El Troyano
# Uso: bash setup_env.sh
# =============================================================

VENV_DIR=".venv"

if [ -d "$VENV_DIR" ]; then
  echo "[INFO] Entorno virtual ya existe: $VENV_DIR"
else
  echo "[INFO] Creando entorno virtual..."
  python3 -m venv "$VENV_DIR" || { echo "[ERROR] Fallo creando entorno"; exit 1; }
fi

source "$VENV_DIR/bin/activate" || { echo "[ERROR] No se pudo activar el entorno"; exit 1; }

echo "[INFO] Actualizando pip..."
pip install --upgrade pip >/dev/null 2>&1

echo "[INFO] Instalando dependencias del juego..."
pip install -r requirements.txt || { echo "[ERROR] Fallo instalando dependencias"; exit 1; }

echo ""
echo "============================================================="
echo "Entorno listo. Para ejecutar el juego:" 
echo "    source $VENV_DIR/bin/activate"
echo "    python Juego/Codigo/main.py"
echo "============================================================="

echo -n "¿Ejecutar ahora? (S/N): "
read RUNNOW
if [ "$RUNNOW" = "S" ] || [ "$RUNNOW" = "s" ]; then
  python Juego/Codigo/main.py
fi
