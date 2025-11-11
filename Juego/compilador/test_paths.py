"""
Script de prueba para verificar las rutas de assets en el ejecutable
"""
import sys
import os

print("=" * 60)
print("VERIFICACIÓN DE RUTAS DE ASSETS")
print("=" * 60)
print()

# Verificar si estamos en ejecutable
if getattr(sys, 'frozen', False):
    print("✅ Ejecutándose como .exe compilado")
    print(f"📁 sys._MEIPASS = {sys._MEIPASS}")
    base_path = sys._MEIPASS
else:
    print("⚠️  Ejecutándose como script Python")
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"📁 Base path = {base_path}")

print()
print("Verificando estructura de archivos:")
print("-" * 60)

# Cambiar al directorio base si es ejecutable
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
    print(f"✅ Cambiado a: {os.getcwd()}")

# Verificar rutas críticas
paths_to_check = [
    "Juego/assets",
    "Juego/assets/Sprites",
    "Juego/assets/Sounds",
    "Juego/assets/Soundtrack",
    "Juego/assets/Sprites/Boss_Virus_1.png",
    "Juego/assets/Sounds/menu_select.wav",
    "Juego/assets/Soundtrack/phase2.mp3",
]

print()
for path in paths_to_check:
    exists = os.path.exists(path)
    symbol = "✅" if exists else "❌"
    print(f"{symbol} {path}")

print()
print("=" * 60)
print("Contenido del directorio actual:")
print("-" * 60)

for item in os.listdir('.'):
    item_type = "📁" if os.path.isdir(item) else "📄"
    print(f"{item_type} {item}")

if os.path.exists('Juego'):
    print()
    print("Contenido de 'Juego/':")
    for item in os.listdir('Juego'):
        item_type = "📁" if os.path.isdir(os.path.join('Juego', item)) else "📄"
        print(f"  {item_type} {item}")
        
    if os.path.exists('Juego/assets'):
        print()
        print("Contenido de 'Juego/assets/':")
        for item in os.listdir('Juego/assets'):
            item_type = "📁" if os.path.isdir(os.path.join('Juego/assets', item)) else "📄"
            count = ""
            if os.path.isdir(os.path.join('Juego/assets', item)):
                count = f" ({len(os.listdir(os.path.join('Juego/assets', item)))} archivos)"
            print(f"  {item_type} {item}{count}")

print()
print("=" * 60)
input("Presiona Enter para salir...")
