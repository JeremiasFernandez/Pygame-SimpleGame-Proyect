"""
Script para quitar emojis de archivos Python
"""
import os
import re

# Mapeo de emojis a reemplazos
EMOJI_REPLACEMENTS = {
    "⚠️": "[WARNING]",
    "🎵": "[MUSIC]",
    "⭐": "[STAR]",
    "ℹ️": "[INFO]",
    "🟢": "[OK]",
    "✓": "[OK]",
}

def remove_emojis_from_file(filepath):
    """Remueve emojis de un archivo Python"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        for emoji, replacement in EMOJI_REPLACEMENTS.items():
            content = content.replace(emoji, replacement)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ {filepath}")
            return True
        return False
    except Exception as e:
        print(f"Error en {filepath}: {e}")
        return False

def process_directory(directory):
    """Procesa todos los archivos .py en un directorio recursivamente"""
    modified_count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                if remove_emojis_from_file(filepath):
                    modified_count += 1
    return modified_count

if __name__ == "__main__":
    # Procesar la carpeta Codigo
    codigo_path = os.path.join("..", "Codigo")
    print("Removiendo emojis de archivos Python...")
    count = process_directory(codigo_path)
    print(f"\nArchivos modificados: {count}")
