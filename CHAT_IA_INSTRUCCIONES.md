# 🤖 Chat con IA durante el Combate

## 📋 Características

Durante el menú de combate, ahora puedes:
- **Presionar C** para abrir el chat con el virus
- **Escribir mensajes** y recibir respuestas de una IA (OpenAI GPT)
- **Personalizar el prompt** del sistema para cambiar la personalidad de la IA
- La interfaz aparece dentro de la caja de combate con un diseño limpio

## 🔧 Configuración

### 1. Instalar OpenAI (REQUERIDO)

Primero necesitas instalar la librería de OpenAI:

```bash
pip install openai
```

### 2. Obtener API Key de OpenAI

1. Ve a https://platform.openai.com/api-keys
2. Inicia sesión o crea una cuenta
3. Crea una nueva API key
4. Copia la key (empieza con `sk-...`)

⚠️ **IMPORTANTE**: Esta API key es sensible. No la compartas públicamente ni la subas a GitHub.

### 3. Configurar en el juego

Abre el archivo `Juego/Codigo/Const.py` y busca la sección:

```python
# --- OpenAI Chat Configuration ---
OPENAI_API_KEY = ""  # ⚠️ IMPORTANTE: Agrega tu API key aquí
```

Pega tu API key entre las comillas:

```python
OPENAI_API_KEY = "sk-tu-api-key-aqui"
```

### 4. Personalizar el Prompt (OPCIONAL)

En el mismo archivo `Const.py`, puedes personalizar cómo responde la IA:

```python
OPENAI_PROMPT = """Eres un virus maligno dentro de una computadora que está peleando contra el jugador. 
Hablas de forma sarcástica, burlona y amenazante. 
Eres ruso, mencionas a veces la tecnología rusa y el ciberespacio. 
Respondes de forma corta (máximo 3 líneas). 
Nunca sales del personaje."""
```

Puedes cambiar este texto por cualquier personalidad que quieras. Por ejemplo:

```python
# Virus amigable
OPENAI_PROMPT = """Eres un virus torpe y amigable que accidentalmente infectó la computadora. 
Pides disculpas constantemente y das consejos útiles. 
Hablas de forma tímida y educada."""

# Hacker elite
OPENAI_PROMPT = """Eres un hacker elite de los años 90. 
Hablas en l33tspeak mezclado con español. 
Das consejos de programación mientras luchas."""

# Filósofo digital
OPENAI_PROMPT = """Eres una entidad digital filosófica. 
Cuestionas la naturaleza de la existencia mientras peleas. 
Citas a Nietzsche y Matrix."""
```

## 🎮 Cómo Usar

1. **Entra en combate** (modo normal o práctica)
2. **Espera al menú de combate** (cuando aparezcan las opciones ATACAR/CURARSE)
3. **Presiona C** para abrir el chat
4. **Escribe tu mensaje** (hasta 100 caracteres)
5. **Presiona ENTER** para enviar
6. **Espera la respuesta** (aparecerá "Esperando respuesta...")
7. **Lee la respuesta** del virus
8. **Presiona ESC** para cerrar el chat y volver al combate

### Controles del Chat

- **C**: Abrir chat (solo en menú de combate)
- **Escribir**: Cualquier letra, número, símbolo
- **BACKSPACE**: Borrar último carácter
- **ENTER**: Enviar mensaje
- **ESC**: Cerrar chat y volver al combate

## 💰 Costos de OpenAI

⚠️ **ADVERTENCIA**: La API de OpenAI **NO ES GRATIS** después de tu crédito inicial.

- Modelo usado: `gpt-3.5-turbo` (el más económico)
- Costo aproximado: ~$0.002 por mensaje (muy barato)
- OpenAI suele dar $5-18 de crédito gratis al crear cuenta nueva
- Con crédito gratis puedes hacer ~2500 mensajes

Para monitorear tu uso: https://platform.openai.com/usage

## 🔍 Solución de Problemas

### "OpenAI no está configurado"

**Causa**: No instalaste la librería o no pusiste la API key.

**Solución**:
```bash
pip install openai
```
Y verifica que `OPENAI_API_KEY` en `Const.py` tenga tu key.

---

### "Error: Incorrect API key provided"

**Causa**: La API key es incorrecta o está mal copiada.

**Solución**: 
- Ve a https://platform.openai.com/api-keys
- Verifica que la key sea válida
- Cópiala de nuevo completa (empieza con `sk-`)

---

### "Error: You exceeded your current quota"

**Causa**: Te quedaste sin crédito en tu cuenta de OpenAI.

**Solución**:
- Ve a https://platform.openai.com/account/billing
- Agrega una tarjeta de crédito o compra créditos
- O espera si tienes límite de rate (límites por minuto)

---

### "OpenAI no instalado"

**Causa**: La librería no está instalada o estás usando un entorno virtual diferente.

**Solución**:
```bash
# Verificar que pip instale en el Python correcto
python -m pip install openai

# O si usas Python 3 específicamente
python3 -m pip install openai
```

---

### El chat no responde / se queda en "Esperando respuesta..."

**Causas posibles**:
1. Sin conexión a internet
2. API key inválida
3. Límite de rate de OpenAI (demasiadas peticiones)
4. Problema con OpenAI (raro)

**Solución**:
- Verifica tu conexión a internet
- Revisa la consola/terminal para ver mensajes de error
- Espera 1 minuto e intenta de nuevo
- Verifica el estado de OpenAI: https://status.openai.com/

---

### Mensajes de error en rojo en la caja de chat

El juego mostrará el error en pantalla. Los errores comunes:
- `"Error: Invalid API key"` → Revisa tu OPENAI_API_KEY
- `"Error: Insufficient quota"` → Sin crédito en OpenAI
- `"Error: Rate limit"` → Esperando demasiado rápido, espera 1 min

## 🎨 Personalización Avanzada

### Cambiar colores del chat

En `combat.py`, busca:

```python
self.chat_prompt_color = (100, 255, 100)      # Tu texto (verde)
self.chat_response_color = (255, 100, 100)    # Respuesta IA (rojo)
```

### Cambiar modelo de IA

En `combat.py`, método `_call_openai_api`, línea con `model=`:

```python
model="gpt-3.5-turbo",  # Rápido y económico
# model="gpt-4",         # Más inteligente pero más caro (~15x)
# model="gpt-4-turbo",   # Balance entre 3.5 y 4
```

### Cambiar longitud de respuesta

En `combat.py`, método `_call_openai_api`:

```python
max_tokens=150,  # Máximo ~3 líneas
# max_tokens=300, # Para respuestas más largas
```

### Cambiar creatividad

En `combat.py`, método `_call_openai_api`:

```python
temperature=0.9  # 0.0 = predecible, 2.0 = muy creativo
```

## 📝 Ejemplos de Prompts Creativos

```python
# Detective noir
OPENAI_PROMPT = """Eres un detective cibernético de película noir. 
Hablas con metáforas oscuras sobre la ciudad digital. 
Cada respuesta es como un monólogo interno."""

# IA kawaii
OPENAI_PROMPT = """Eres una IA kawaii que usa muchos emoticones ^_^ 
Hablas con entusiasmo pero eres torpe. 
Mezclas español con palabras japonesas. Nya~!"""

# Gladiador romano
OPENAI_PROMPT = """Eres un virus que se cree gladiador romano. 
Hablas como César, mencionas al Coliseo y a los dioses. 
"¡Por Júpiter!" es tu muletilla."""

# Científico loco
OPENAI_PROMPT = """Eres un científico loco obsesionado con experimentos. 
Explicas teorías absurdas sobre computación cuántica. 
Ríes malvadamente: "¡MUAHAHAHA!" """

# Poeta melancólico
OPENAI_PROMPT = """Eres un virus poeta y melancólico. 
Hablas en versos sobre la soledad del código. 
Citas a Bécquer y Neruda."""
```

## 🚀 Características Técnicas

- **Async Threading**: Las llamadas a OpenAI no bloquean el juego
- **Word Wrapping**: Texto se ajusta automáticamente al ancho de la caja
- **Input Buffer**: Hasta 100 caracteres por mensaje
- **Cursor Parpadeante**: Indicador visual de input activo
- **Error Handling**: Manejo robusto de errores de API
- **Fallback**: Si OpenAI no está disponible, muestra mensaje claro

## 📞 Contacto

Si tienes problemas o ideas:
- Revisa la consola/terminal para logs detallados
- Cada acción del chat imprime mensajes de debug
- Los errores de OpenAI se muestran en pantalla y consola

---

**¡Diviértete hablando con el virus! 🦠💬🤖**
