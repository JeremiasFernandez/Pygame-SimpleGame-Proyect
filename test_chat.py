"""
Script de prueba para verificar que el chat funciona
Ejecuta esto para ver si la tecla C está siendo detectada
"""
import pygame
import sys
import os

# Agregar path para importar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Juego', 'Codigo'))

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

print("\n" + "="*50)
print("🧪 TEST DE DETECCIÓN DE TECLA C")
print("="*50)
print("Presiona la tecla C para probar")
print("Presiona ESC para salir")
print("="*50 + "\n")

running = True
c_pressed_before = False

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_c:
                print("✅ ¡Tecla C detectada por evento!")
    
    keys = pygame.key.get_pressed()
    c_pressed_now = keys[pygame.K_c]
    
    # Detectar presión única
    if c_pressed_now and not c_pressed_before:
        print("✅ ¡Tecla C detectada por get_pressed()!")
    
    c_pressed_before = c_pressed_now
    
    screen.fill((0, 0, 0))
    
    # Mostrar estado
    font = pygame.font.Font(None, 36)
    if keys[pygame.K_c]:
        text = font.render("C PRESIONADA", True, (0, 255, 0))
    else:
        text = font.render("Presiona C", True, (255, 255, 255))
    
    rect = text.get_rect(center=(400, 300))
    screen.blit(text, rect)
    
    pygame.display.flip()

pygame.quit()
print("\n✅ Test finalizado")
