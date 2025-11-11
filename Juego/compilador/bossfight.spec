# -*- mode: python ; coding: utf-8 -*-
"""
Archivo de configuración para PyInstaller
Crea un ejecutable standalone del juego Bossfight: El Troyano
EJECUTAR DESDE: Juego/compilador/
"""

import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Rutas del proyecto
block_cipher = None
codigo_path = os.path.join(os.path.dirname(os.path.abspath('.')), 'Codigo')
assets_path = os.path.join(os.path.dirname(os.path.abspath('.')), 'assets')

# Recolectar todos los archivos de assets con la estructura correcta "Juego/assets"
datas = [
    (os.path.join(assets_path, 'Sounds'), 'Juego/assets/Sounds'),
    (os.path.join(assets_path, 'Soundtrack'), 'Juego/assets/Soundtrack'),
    (os.path.join(assets_path, 'Sprites'), 'Juego/assets/Sprites'),
]

# Módulos ocultos necesarios
hiddenimports = [
    'pygame',
    'PIL',
    'PIL.Image',
    'openai',
    'Const',
    'characters.player',
    'characters.boss',
    'characters.bullet',
    'characters.border',
    'screens.menu',
    'screens.intro',
    'screens.combat',
    'screens.practice',
    'screens.victory',
    'screens.gameover',
    'screens.play_select',
    'screens.options',
    'screens.credits',
]

a = Analysis(
    [os.path.join(codigo_path, 'main.py')],
    pathex=[codigo_path],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Bossfight_ElTroyano',
    debug=False,  # Modo release sin debug
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin consola en modo release
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='game_icon.ico',  # Ícono del ejecutable
)

# Crear COLLECT para mover el .exe a la carpeta raíz del proyecto
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Bossfight_ElTroyano',
)

# Copiar el ejecutable a la raíz del proyecto
import shutil
import os
root_path = os.path.join(os.path.dirname(base_path), '..', '..')
exe_source = os.path.join('dist', 'Bossfight_ElTroyano.exe')
exe_dest = os.path.join(root_path, 'Bossfight_ElTroyano.exe')
if os.path.exists(exe_source):
    shutil.copy2(exe_source, exe_dest)
    print(f"✅ Ejecutable copiado a: {exe_dest}")
