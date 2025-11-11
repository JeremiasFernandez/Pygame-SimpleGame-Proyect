# 🤖 Chat con IA en Combate - Resumen Rápido

## ✅ Implementación Completa

Se ha agregado un sistema de chat con IA (OpenAI) durante el combate.

### 📦 Archivos Modificados:

1. **`Juego/Codigo/Const.py`**
   - ✅ Agregadas variables `OPENAI_API_KEY` y `OPENAI_PROMPT`
   - Aquí debes poner tu API key de OpenAI

2. **`Juego/Codigo/screens/combat.py`**
   - ✅ Sistema completo de chat con OpenAI
   - ✅ Interfaz visual dentro de la caja de combate
   - ✅ Manejo de input de texto
   - ✅ Threading para no bloquear el juego

3. **`Juego/Codigo/main.py`**
   - ✅ Integración de eventos de chat
   - ✅ Manejo de teclado cuando el chat está activo

## 🚀 Pasos para Activar:

### 1. Instalar OpenAI
```bash
pip install openai
```

### 2. Conseguir API Key
1. Ve a https://platform.openai.com/api-keys
2. Crea una cuenta (¡te dan crédito gratis!)
3. Crea una API key
4. Cópiala (empieza con `sk-...`)

### 3. Configurar
Abre `Juego/Codigo/Const.py` y pega tu API key:

```python
OPENAI_API_KEY = "sk-tu-key-aqui"  # ⚠️ Pon tu key aquí
```

### 4. ¡Jugar!
- Entra en combate
- Presiona **C** en el menú de combate
- Escribe y presiona **ENTER**
- ¡El virus te responde!
- Presiona **ESC** para cerrar

## 🎨 Personalizar la IA

Edita `OPENAI_PROMPT` en `Const.py` para cambiar la personalidad:

```python
OPENAI_PROMPT = """Tu personalidad aquí..."""
```

Ejemplos:
- Virus ruso amenazante (por defecto)
- IA amigable y torpe
- Filósofo digital
- Hacker de los 90s
- ¡Lo que quieras!

## 📖 Documentación Completa

Ver: **`CHAT_IA_INSTRUCCIONES.md`** para:
- Guía detallada de instalación
- Solución de problemas
- Personalización avanzada
- Ejemplos de prompts creativos
- Información sobre costos
- Consejos técnicos

## 🎮 Controles

| Tecla | Acción |
|-------|--------|
| **C** | Abrir chat (en menú de combate) |
| **Escribir** | Cualquier tecla |
| **BACKSPACE** | Borrar |
| **ENTER** | Enviar mensaje |
| **ESC** | Cerrar chat |

## ⚠️ Importante

- **OpenAI NO es gratis** después del crédito inicial (~$5-18)
- Cada mensaje cuesta ~$0.002 (muy barato)
- Necesitas conexión a internet
- El juego sigue funcionando mientras espera respuesta

## ✨ Características

✅ No bloquea el juego (threading asíncrono)  
✅ Word wrapping automático  
✅ Cursor parpadeante  
✅ Manejo de errores robusto  
✅ Interfaz limpia dentro de la caja de combate  
✅ Prompt 100% personalizable  
✅ Funciona en modo normal y práctica  

---

**¡Diviértete chateando con el virus! 🦠💬**
