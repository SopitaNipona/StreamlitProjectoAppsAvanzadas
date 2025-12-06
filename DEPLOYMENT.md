# Guía de Deployment - Detector de Plagio

Esta guía te ayudará a desplegar la aplicación Streamlit en **Streamlit Community Cloud** y **Render.com**.

---

## Opción 1: Streamlit Community Cloud (RECOMENDADO - Gratis y Fácil)

Streamlit Community Cloud es la forma más fácil y rápida de desplegar aplicaciones Streamlit.

### Requisitos Previos

1. Cuenta de GitHub (ya tienes el repositorio)
2. Cuenta en [share.streamlit.io](https://share.streamlit.io)

### Paso 1: Preparar el Repositorio

Asegúrate de que tu repositorio tenga estos archivos (ya creados):

```
ProyectoAnalisisSimilitud/
├── app.py                    # Aplicación principal ✓
├── requirements.txt          # Dependencias ✓
├── packages.txt              # Dependencias del sistema ✓
├── setup.sh                  # Script de configuración ✓
├── .streamlit/
│   └── config.toml          # Configuración de Streamlit ✓
└── src/                      # Módulos del detector ✓
```

### Paso 2: Hacer Commit y Push a GitHub

```bash
# En tu terminal, dentro del directorio del proyecto

# 1. Dar permisos de ejecución al script setup.sh
chmod +x setup.sh

# 2. Agregar todos los archivos
git add .

# 3. Hacer commit
git commit -m "Add deployment configuration for Streamlit Cloud"

# 4. Push a GitHub
git push origin main
```

### Paso 3: Desplegar en Streamlit Community Cloud

1. **Ve a [share.streamlit.io](https://share.streamlit.io)**

2. **Inicia sesión con tu cuenta de GitHub**

3. **Haz clic en "New app"**

4. **Configura tu aplicación:**
   - **Repository:** `TuUsuario/ProyectoAnalisisSimilitud`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** Elige un nombre único (ej: `detector-plagio-ia`)

5. **Configuración Avanzada (Advanced settings):**

   Haz clic en "Advanced settings" y configura:

   - **Python version:** `3.9` o `3.10`
   - **Secrets:** No es necesario para esta app

6. **Haz clic en "Deploy!"**

### Paso 4: Esperar el Deployment

- El proceso tarda **5-10 minutos** la primera vez
- Verás los logs en tiempo real
- La app descargará automáticamente:
  - Todas las dependencias de `requirements.txt`
  - Los paquetes del sistema de `packages.txt`
  - Los modelos de spaCy vía `setup.sh`

### Paso 5: ¡Listo!

Tu app estará disponible en:
```
https://tu-app-nombre.streamlit.app
```

Ejemplo: `https://detector-plagio-ia.streamlit.app`

### Actualizar la Aplicación

Cada vez que hagas `git push` a la rama `main`, la app se actualizará automáticamente.

```bash
# Hacer cambios en el código
# ...

git add .
git commit -m "Actualizar funcionalidad X"
git push origin main

# La app se redesplegará automáticamente en 2-3 minutos
```

### Solución de Problemas - Streamlit Cloud

**Problema: La app no carga los modelos de spaCy**

Solución: Verifica que `setup.sh` tenga permisos de ejecución y esté en la raíz del proyecto.

**Problema: Error de memoria**

Streamlit Community Cloud tiene límite de 1GB RAM. Si la app usa demasiada memoria:

1. En `app.py`, modifica el modelo a uno más ligero:
```python
# Cambiar línea 248
detector = PlagiarismDetector(
    language=language,
    model_name='paraphrase-MiniLM-L6-v2'  # Modelo más ligero
)
```

**Problema: La app se "duerme" después de inactividad**

Esto es normal en el plan gratuito. La app se reactiva automáticamente cuando alguien la visita (tarda ~30 segundos).

---

## Opción 2: Render.com (Alternativa con más recursos)

Render.com ofrece más recursos que Streamlit Cloud, pero es un poco más complejo.

### Requisitos Previos

1. Cuenta de GitHub
2. Cuenta en [render.com](https://render.com)

### Paso 1: Crear archivo de configuración para Render

Crea un archivo `render.yaml` en la raíz del proyecto:

```yaml
services:
  - type: web
    name: detector-plagio
    env: python
    region: oregon
    plan: free
    buildCommand: |
      pip install -r requirements.txt
      python -m spacy download es_core_news_md
    startCommand: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
    envVars:
      - key: PYTHON_VERSION
        value: 3.9.0
```

### Paso 2: Hacer Commit y Push

```bash
git add render.yaml
git commit -m "Add Render.com configuration"
git push origin main
```

### Paso 3: Desplegar en Render.com

1. **Ve a [dashboard.render.com](https://dashboard.render.com)**

2. **Haz clic en "New +" → "Web Service"**

3. **Conecta tu repositorio de GitHub:**
   - Autoriza a Render para acceder a tus repos
   - Selecciona `ProyectoAnalisisSimilitud`

4. **Configura el servicio:**
   - **Name:** `detector-plagio`
   - **Environment:** `Python 3`
   - **Region:** Elige la más cercana
   - **Branch:** `main`
   - **Build Command:**
     ```bash
     pip install -r requirements.txt && python -m spacy download es_core_news_md
     ```
   - **Start Command:**
     ```bash
     streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
     ```

5. **Plan:** Selecciona **Free**

6. **Haz clic en "Create Web Service"**

### Paso 4: Esperar el Deployment

- El proceso tarda **10-15 minutos** la primera vez
- Verás los logs en tiempo real
- Render compilará todo desde cero

### Paso 5: ¡Listo!

Tu app estará disponible en:
```
https://detector-plagio.onrender.com
```

### Actualizar la Aplicación en Render

Render redespliega automáticamente cuando haces push a `main`.

### Solución de Problemas - Render

**Problema: La app tarda mucho en cargar**

El plan gratuito de Render "apaga" la app después de 15 minutos de inactividad. El primer acceso después de esto tarda ~1 minuto en "despertar".

Solución: Considera el plan de pago ($7/mes) para mantenerla siempre activa.

**Problema: Build timeout**

Si el build tarda más de 15 minutos (límite del plan gratuito):

1. Reduce las dependencias
2. Usa un modelo más ligero de Sentence-BERT

**Problema: Error de memoria en runtime**

El plan gratuito tiene 512MB RAM. Si la app crashea:

1. Modifica `app.py` para usar modelo más ligero
2. Añade `@st.cache_resource` para cachear el modelo:

```python
@st.cache_resource
def load_detector(language):
    return PlagiarismDetector(
        language=language,
        model_name='paraphrase-MiniLM-L6-v2'
    )

# Usar en el código
detector = load_detector(language)
```

---

## Comparación: Streamlit Cloud vs Render.com

| Característica | Streamlit Cloud | Render.com |
|---------------|----------------|------------|
| **Facilidad de uso** | ⭐⭐⭐⭐⭐ Muy fácil | ⭐⭐⭐⭐ Fácil |
| **Velocidad de deployment** | ⭐⭐⭐⭐⭐ 5-7 min | ⭐⭐⭐ 10-15 min |
| **Memoria RAM (free)** | 1 GB | 512 MB |
| **CPU (free)** | Compartido | Compartido |
| **Sleep después de inactividad** | Sí (~30 min) | Sí (~15 min) |
| **Wake-up time** | ~10-30 seg | ~30-60 seg |
| **Dominio personalizado** | ❌ No | ✅ Sí (plan pago) |
| **Auto-redeploy en push** | ✅ Sí | ✅ Sí |
| **Logs en tiempo real** | ✅ Sí | ✅ Sí |
| **Mejor para** | Apps Streamlit | Apps genéricas Python |

### Recomendación

**Para este proyecto: Usa Streamlit Community Cloud**

Razones:
- ✅ Más fácil y rápido de configurar
- ✅ Mejor integrado con Streamlit
- ✅ Más memoria RAM (1GB vs 512MB)
- ✅ Wake-up más rápido
- ✅ Diseñado específicamente para apps Streamlit

Usa Render.com solo si:
- Necesitas dominio personalizado
- Quieres más control sobre la infraestructura
- Vas a pagar por el plan Pro

---

## Optimizaciones para Deployment

### 1. Reducir Tiempo de Carga

Añade caché al modelo en `app.py`:

```python
import streamlit as st

# Añadir al inicio del archivo, después de los imports
@st.cache_resource
def load_plagiarism_detector(language, model_name='paraphrase-multilingual-MiniLM-L12-v2'):
    """Cachea el detector para evitar recargarlo en cada interacción"""
    return PlagiarismDetector(language=language, model_name=model_name)

# Modificar en main() donde se carga el detector
def main():
    # ... código existente ...

    # En lugar de:
    # detector = PlagiarismDetector(language=language)

    # Usar:
    detector = load_plagiarism_detector(language=language)
```

### 2. Reducir Uso de Memoria

Si tienes problemas de memoria, usa un modelo más ligero:

```python
# En app.py, modificar la carga del detector
detector = load_plagiarism_detector(
    language=language,
    model_name='paraphrase-MiniLM-L6-v2'  # 80MB en lugar de 500MB
)
```

### 3. Mejorar Experiencia de Usuario

Añade mensaje de "primera carga" en `app.py`:

```python
def main():
    st.set_page_config(
        page_title="Detector de Plagio",
        page_icon="📝",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Añadir mensaje informativo
    if 'first_load' not in st.session_state:
        st.info("⏳ Primera carga: descargando modelos de IA... Esto puede tomar 1-2 minutos.")
        st.session_state.first_load = True
```

---

## Variables de Entorno (Opcional)

Si en el futuro necesitas variables de entorno (API keys, etc.):

### En Streamlit Cloud:

1. Ve a tu app en el dashboard
2. Click en "⋮" → "Settings" → "Secrets"
3. Añade en formato TOML:

```toml
API_KEY = "tu-api-key-aqui"
SECRET_TOKEN = "token-secreto"
```

4. Accede en el código:

```python
import streamlit as st

api_key = st.secrets["API_KEY"]
```

### En Render.com:

1. Ve a tu servicio en el dashboard
2. "Environment" → "Add Environment Variable"
3. Añade KEY=VALUE

4. Accede en el código:

```python
import os

api_key = os.environ.get("API_KEY")
```

---

## Monitoreo y Logs

### Streamlit Cloud:

- Los logs están disponibles en el dashboard
- Click en tu app → "Manage app" → Ver logs en tiempo real

### Render.com:

- Click en tu servicio → "Logs"
- Logs en tiempo real con filtros

---

## Costos

### Streamlit Community Cloud:

- ✅ **Completamente GRATIS**
- Límites:
  - 3 apps públicas
  - 1 app privada
  - 1 GB RAM por app
  - Recursos compartidos

### Render.com:

- ✅ **Plan Free:** $0/mes
  - 512 MB RAM
  - Apps se duermen después de 15 min
  - 750 horas/mes de tiempo activo

- **Plan Starter:** $7/mes
  - Siempre activo (no sleep)
  - 512 MB RAM
  - Mejor performance

---

## Checklist Final Antes de Desplegar

- [ ] Todos los archivos están en el repositorio
- [ ] `requirements.txt` está actualizado
- [ ] `setup.sh` tiene permisos de ejecución (`chmod +x setup.sh`)
- [ ] `app.py` no tiene rutas absolutas (usa rutas relativas)
- [ ] El código funciona localmente con `streamlit run app.py`
- [ ] Has hecho commit y push de todos los cambios
- [ ] Has probado que los imports funcionan correctamente

```bash
# Verificación rápida
python -c "from src.plagiarism_detector import PlagiarismDetector; print('OK')"
```

---

## Soporte

Si tienes problemas:

1. **Streamlit Cloud:**
   - [Documentación oficial](https://docs.streamlit.io/streamlit-community-cloud)
   - [Foro de la comunidad](https://discuss.streamlit.io/)

2. **Render.com:**
   - [Documentación oficial](https://render.com/docs)
   - [Community forum](https://community.render.com/)

3. **Revisar logs:**
   - Ambas plataformas muestran logs detallados
   - Busca errores específicos de imports o dependencias

---

## Próximos Pasos Después del Deployment

1. **Comparte tu app:**
   - Copia la URL pública
   - Comparte con profesores, compañeros, etc.

2. **Monitorea el uso:**
   - Revisa estadísticas en el dashboard
   - Identifica errores comunes

3. **Actualiza continuamente:**
   - Mejora basándote en feedback
   - Push para auto-redeploy

4. **Considera un dominio personalizado:**
   - Si usas Render.com (plan pago)
   - O usa un servicio como Cloudflare

---

¡Buena suerte con el deployment! 🚀
