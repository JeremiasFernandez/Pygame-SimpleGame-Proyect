#!/bin/bash
################################################################################
# Bossfight: El Troyano - Launcher Universal (Linux/Mac)
################################################################################
# Este script ejecuta el juego desde cualquier ubicacion del sistema
# No importa donde este instalado el proyecto
################################################################################

echo ""
echo "========================================"
echo "  Bossfight: El Troyano"
echo "  Iniciando juego..."
echo "========================================"
echo ""

# Obtener la ubicacion de este script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navegar a la carpeta Juego/Codigo (relativa a este script)
cd "$SCRIPT_DIR/Juego/Codigo"

# Verificar que Python esta disponible
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "[ERROR] Python 3 no esta instalado"
    echo ""
    echo "Instala Python 3 desde:"
    echo "  - Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  - macOS: brew install python3"
    echo "  - o desde https://www.python.org/"
    echo ""
    read -p "Presiona Enter para salir..."
    exit 1
fi

# Verificar que las dependencias estan instaladas
python3 -c "import pygame" 2>/dev/null
if [ $? -ne 0 ]; then
    echo ""
    echo "[ADVERTENCIA] pygame no esta instalado"
    echo ""
    echo "Instalando dependencias automaticamente..."
    echo ""
    
    # Volver a la raiz para usar requirements.txt
    cd "$SCRIPT_DIR"
    pip3 install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "[ERROR] No se pudieron instalar las dependencias"
        echo "Por favor ejecuta manualmente: pip3 install pygame pillow"
        echo ""
        read -p "Presiona Enter para salir..."
        exit 1
    fi
    
    # Volver a Juego/Codigo
    cd "$SCRIPT_DIR/Juego/Codigo"
    echo ""
    echo "[OK] Dependencias instaladas correctamente"
    echo ""
fi

# Ejecutar el juego
echo "Iniciando Bossfight: El Troyano..."
echo ""
python3 main.py

# Si hubo error, pausar para ver el mensaje
if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] El juego se cerro con un error"
    echo ""
    read -p "Presiona Enter para salir..."
fi
