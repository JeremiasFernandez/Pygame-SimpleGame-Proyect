"""
Script para generar un ícono .ico para el ejecutable del juego
Convierte una imagen PNG a formato ICO con múltiples resoluciones
"""

from PIL import Image
import os

def create_game_icon():
    """
    Crea un archivo .ico a partir de una imagen existente o genera uno básico
    """
    
    # Buscar imagen existente para usar como ícono
    possible_icons = [
        os.path.join("..", "assets", "Sprites", "Boss_Virus_1.png"),
        os.path.join("..", "assets", "Sprites", "player_cara.png"),
        os.path.join("..", "assets", "Sprites", "mas_sprites", "player_cara.png"),
    ]
    
    source_image = None
    for icon_path in possible_icons:
        if os.path.exists(icon_path):
            source_image = icon_path
            break
    
    if source_image:
        print(f"📷 Usando imagen: {source_image}")
        try:
            img = Image.open(source_image)
            
            # Convertir a RGBA si no lo está
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Crear ícono con múltiples tamaños (requerido por Windows)
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            
            # Redimensionar y guardar
            img.save(
                'game_icon.ico',
                format='ICO',
                sizes=icon_sizes
            )
            
            print("✅ Ícono 'game_icon.ico' creado exitosamente con múltiples resoluciones")
            return True
            
        except Exception as e:
            print(f"⚠️ Error al procesar imagen: {e}")
    
    # Si no hay imagen, crear un ícono básico
    print("📦 Creando ícono básico...")
    try:
        # Crear imagen base de 256x256
        img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
        
        # Crear un diseño simple (círculo rojo representando el virus)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        
        # Fondo oscuro circular
        draw.ellipse([20, 20, 236, 236], fill=(40, 40, 60, 255))
        
        # Círculo rojo (virus)
        draw.ellipse([50, 50, 206, 206], fill=(220, 50, 50, 255))
        
        # Círculo interno más oscuro
        draw.ellipse([90, 90, 166, 166], fill=(150, 30, 30, 255))
        
        # Punto central
        draw.ellipse([118, 118, 138, 138], fill=(255, 100, 100, 255))
        
        # Guardar como .ico con múltiples tamaños
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        img.save(
            'game_icon.ico',
            format='ICO',
            sizes=icon_sizes
        )
        
        print("✅ Ícono básico 'game_icon.ico' creado exitosamente")
        return True
        
    except Exception as e:
        print(f"❌ Error al crear ícono básico: {e}")
        return False

if __name__ == "__main__":
    print("🎨 Generador de Ícono para Bossfight: El Troyano")
    print("=" * 60)
    create_game_icon()
