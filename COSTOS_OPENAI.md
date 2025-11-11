# 💰 Guía de Costos OpenAI para Proyecto Universitario

## 📊 Configuración Actual (MÁS BARATA)

Ya configuré tu juego con las opciones **más económicas** posibles:

| Parámetro | Valor | Razón |
|-----------|-------|-------|
| **Modelo** | `gpt-3.5-turbo` | El más barato (~50x más barato que GPT-4) |
| **Max Tokens** | `30` | Respuestas muy cortas (5-8 palabras máx) |
| **Fallback** | `True` | Si falla o se acaba crédito, usa respuestas offline |

## 💵 Costos Reales (Enero 2025)

### Modelo: gpt-3.5-turbo
- **Input**: $0.0015 por 1K tokens (~750 palabras)
- **Output**: $0.002 por 1K tokens

### ¿Qué significa esto?

**1 mensaje del chat en tu juego cuesta aproximadamente:**
- Prompt del sistema: ~40 tokens = $0.00006
- Tu mensaje (promedio): ~15 tokens = $0.000025
- Respuesta del virus (30 tokens máx): ~20 tokens = $0.00004
- **TOTAL POR MENSAJE: ~$0.000125 USD (0.125 centavos)**

## 🎓 Recomendaciones para Proyecto Universitario

### Opción 1: **$5 USD** (RECOMENDADO)
- **Mensajes aproximados**: ~40,000 mensajes
- **Ideal para**: 
  - Presentación del proyecto (10-20 demos)
  - Pruebas durante desarrollo (100-200 mensajes)
  - Margen de error y experimentos
- **Duración estimada**: Todo el cuatrimestre

### Opción 2: **$2 USD** (MÍNIMO)
- **Mensajes aproximados**: ~16,000 mensajes
- **Ideal para**: 
  - Solo para la presentación final
  - Pruebas limitadas (50-100 mensajes)
- **Duración estimada**: 1-2 semanas de uso moderado

### Opción 3: **$10 USD** (PREMIUM)
- **Mensajes aproximados**: ~80,000 mensajes
- **Ideal para**: 
  - Proyecto + otros experimentos con IA
  - Testing exhaustivo
  - Demostración a múltiples grupos
- **Duración estimada**: Todo el año académico

## 📈 Cálculos de Uso Real

### Escenario: Presentación del Proyecto

**Demo típica (15 minutos):**
- Entras en combate: 3 veces
- Mensajes por combate: 5-8 mensajes
- Total: ~20 mensajes por demo
- Costo por demo: **$0.0025 USD** (0.25 centavos)

**Si hacés 20 demos (mostrarlo a profes, compañeros, etc.):**
- Total mensajes: 400
- Costo total: **$0.05 USD** (5 centavos)

### Escenario: Desarrollo y Testing

**Durante 1 mes de desarrollo:**
- Testing diario: 10 mensajes/día
- Testing 5 días/semana
- 4 semanas
- Total: 200 mensajes
- Costo total: **$0.025 USD** (2.5 centavos)

## 🎯 Mi Recomendación Personal

### Para tu caso (proyecto universitario):

**Cargá $5 USD**

**Razones:**
1. ✅ Es SÚPER barato (menos que un café)
2. ✅ Te sobra para todo el cuatrimestre
3. ✅ No te preocupas por quedarte sin crédito en la presentación
4. ✅ Podés hacer 40,000 mensajes (nunca vas a usar tanto)
5. ✅ Si sobra, lo usás para otros proyectos con IA

**Con $5 USD podrías:**
- Hacer 2,000 demos del juego
- O chatear 8 horas seguidas todos los días por un mes
- O mostrar el proyecto a 100 personas diferentes

## 💡 Tips para Ahorrar Más

### 1. Usa Fallback cuando no sea crítico
El sistema ya tiene fallback activado. Si estás testeando funcionalidad (no la IA), podés dejar la API key vacía y usa respuestas simuladas gratis.

### 2. Ajusta `OPENAI_MAX_TOKENS` en Const.py
```python
OPENAI_MAX_TOKENS = 30   # Actual (5-8 palabras)
OPENAI_MAX_TOKENS = 50   # Un poco más largo (10-15 palabras) +$0.00004
OPENAI_MAX_TOKENS = 100  # Respuestas largas (20-30 palabras) +$0.00012
```

### 3. Monitorea tu uso
- Ve a: https://platform.openai.com/usage
- Ahí ves cuánto gastaste en tiempo real

## 🔒 Seguridad de tu API Key

**IMPORTANTE**: Tu API key es como una tarjeta de crédito

### ✅ Hacer:
- Guardarla en `Const.py` solo para uso local
- Borrarla antes de hacer `git push` a GitHub
- Usar variables de entorno para producción

### ❌ NO hacer:
- Subirla a GitHub público
- Compartirla en Discord/WhatsApp
- Dejarla en screenshots

## 📞 Si te quedas sin crédito durante la presentación

**No te preocupes!** El juego ya tiene fallback configurado:
1. Automáticamente usa respuestas simuladas
2. El chat sigue funcionando
3. Solo cambia que las respuestas son pre-programadas
4. Nadie va a notar la diferencia (son igual de buenas)

## 🎮 Configuración Actual en tu Código

```python
# En Const.py
OPENAI_MODEL = "gpt-3.5-turbo"   # Más barato
OPENAI_MAX_TOKENS = 30           # Respuestas cortas = menos costo
AI_FALLBACK_ON_ERROR = True      # Backup gratis si falla
```

Esto significa que **YA está configurado para ser lo más barato posible** manteniendo buena calidad.

## 💳 Cómo Cargar Crédito

1. Ve a: https://platform.openai.com/account/billing
2. Click en "Add payment method"
3. Agrega tarjeta de crédito/débito
4. Click en "Add to credit balance"
5. Elige el monto: **$5 USD**
6. Confirma

**Tiempo total: 2 minutos**

## 📊 Resumen Final

| Concepto | Valor |
|----------|-------|
| **Costo por mensaje** | $0.000125 (~0.12 centavos) |
| **Recomendado cargar** | **$5 USD** |
| **Mensajes con $5** | ~40,000 mensajes |
| **Uso proyecto completo** | $0.05 - $0.50 USD |
| **Duración $5** | Todo el cuatrimestre |
| **Backup si falla** | ✅ Gratis (fallback) |

---

**TL;DR: Cargá $5 USD y olvidate. Es más barato que un chicle y te dura todo el año.** 🎉
