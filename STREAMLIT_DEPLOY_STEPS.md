# 🚀 Deploy en Streamlit Cloud - Pasos Exactos

## Paso a Paso (15 minutos total)

---

## ✅ PASO 1: Preparar y Subir a GitHub (5 minutos)

Abre tu terminal y ejecuta estos comandos:

```bash
# Navega a tu proyecto
cd /home/diego/github/ProyectoAnalisisSimilitud

# Verifica que todos los archivos de deployment estén listos
ls -la packages.txt setup.sh .streamlit/config.toml

# Añade todos los archivos
git add .

# Haz commit
git commit -m "Ready for Streamlit Cloud deployment"

# Sube a GitHub
git push origin main
```

**Verifica en GitHub:** Ve a tu repositorio y confirma que ves:
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `packages.txt`
- ✅ `setup.sh`
- ✅ Carpeta `src/` con los módulos
- ✅ Carpeta `.streamlit/` con `config.toml`

---

## ✅ PASO 2: Crear Cuenta en Streamlit Cloud (2 minutos)

1. **Ve a:** https://share.streamlit.io

2. **Click en "Sign in"**

3. **Selecciona "Continue with GitHub"**

4. **Autoriza a Streamlit:**
   - Streamlit pedirá acceso a tus repositorios
   - Click "Authorize streamlit"
   - Confirma tu contraseña de GitHub si te la pide

5. **¡Listo!** Ya tienes cuenta en Streamlit Cloud

---

## ✅ PASO 3: Desplegar Tu App (3 minutos)

### 3.1 Crear Nueva App

1. En el dashboard de Streamlit Cloud, click en **"New app"** (botón azul arriba a la derecha)

### 3.2 Configurar el Deployment

Completa el formulario con estos datos exactos:

**Repository:**
```
tu-usuario-github/ProyectoAnalisisSimilitud
```
(Busca y selecciona tu repositorio de la lista)

**Branch:**
```
main
```

**Main file path:**
```
app.py
```

**App URL (opcional):**
```
detector-plagio-ia
```
(O el nombre que prefieras - será: https://detector-plagio-ia.streamlit.app)

### 3.3 Configuración Avanzada (Opcional pero Recomendado)

Click en **"Advanced settings"** y configura:

**Python version:**
```
3.9
```

**Secrets:** (Deja vacío por ahora, no necesitas secrets)

### 3.4 Desplegar

Click en el botón **"Deploy!"** (azul, abajo a la derecha)

---

## ✅ PASO 4: Esperar el Build (5-10 minutos)

Verás una pantalla con logs en tiempo real. Esto es lo que sucederá:

### Fase 1: Clonando repositorio
```
Cloning into '/mount/src/proyectoanalisissimilitud'...
```
⏱️ Duración: 10-20 segundos

### Fase 2: Instalando dependencias del sistema
```
Reading package lists...
Building dependency tree...
Installing python3-dev build-essential...
```
⏱️ Duración: 1-2 minutos

### Fase 3: Instalando dependencias Python
```
Collecting numpy
Collecting pandas
Collecting sentence-transformers
...
Successfully installed torch-2.x transformers-4.x
```
⏱️ Duración: 3-5 minutos

### Fase 4: Ejecutando setup.sh
```
Running /mount/src/proyectoanalisissimilitud/setup.sh
Downloading es_core_news_md...
✔ Download and installation successful
```
⏱️ Duración: 1-2 minutos

### Fase 5: Iniciando app
```
You can now view your Streamlit app in your browser.
```
⏱️ Duración: 10-30 segundos

### ✅ Build Exitoso

Cuando veas esto, ¡tu app está lista!:

```
✓ Your app is now deployed!

View app: https://detector-plagio-ia.streamlit.app
```

---

## ✅ PASO 5: Verificar que Funciona (2 minutos)

### 5.1 Abrir la App

Click en el link de tu app o ve a:
```
https://[tu-nombre-elegido].streamlit.app
```

### 5.2 Probar Funcionalidad

**Prueba 1: Entrada de Texto**
1. Scroll hasta "✍️ O escribe/pega texto directamente"
2. Pega este texto en Texto A:
   ```
   La inteligencia artificial está revolucionando el mundo de la tecnología.
   ```
3. Pega este texto en Texto B:
   ```
   La IA está transformando nuestro mundo tecnológico de manera significativa.
   ```
4. Click "🔍 Comparar Documentos"
5. Espera 5-10 segundos
6. ✅ Deberías ver resultados con ~60-75% de similitud

**Prueba 2: Cambiar Idioma**
1. En el sidebar, cambia idioma a "english"
2. Repite la comparación
3. ✅ Debería funcionar igual

---

## 🎉 ¡Felicitaciones! Tu App Está Online

Tu app ahora está disponible públicamente en:
```
https://[tu-nombre].streamlit.app
```

Comparte este link con:
- 👨‍🏫 Profesores
- 👥 Compañeros de clase
- 🌍 Cualquier persona

---

## 🔄 Actualizar la App en el Futuro

Cada vez que hagas cambios:

```bash
# 1. Haz tus cambios en el código
# 2. Commit y push
git add .
git commit -m "Descripción de los cambios"
git push origin main

# 3. ¡Listo! Streamlit redespliega automáticamente en 2-3 minutos
```

No necesitas hacer nada más - el redeploy es automático.

---

## 🐛 Solución de Problemas

### Problema 1: "Error: Could not find spacy model"

**Solución:**
```bash
# Verifica que setup.sh tenga permisos de ejecución
chmod +x setup.sh
git add setup.sh
git commit -m "Fix setup.sh permissions"
git push origin main
```

Luego en Streamlit Cloud:
1. Click en "⋮" (menú)
2. "Reboot app"

### Problema 2: "Build failed: requirements.txt"

**Solución:**
Verifica que `requirements.txt` tenga el formato correcto:
```bash
# Ver el contenido
cat requirements.txt

# Debería tener una línea por dependencia, sin versiones conflictivas
```

Si hay errores, corrígelos y haz push:
```bash
git add requirements.txt
git commit -m "Fix requirements.txt"
git push origin main
```

### Problema 3: La app se queda "Loading..."

**Causas posibles:**
- Primera carga: Espera 60-90 segundos (descarga modelos)
- La app se durmió: Espera 30 segundos (se está reactivando)

**Si persiste >2 minutos:**
1. Refresca la página (F5)
2. Si sigue, ve al dashboard de Streamlit
3. Click "⋮" → "View logs"
4. Busca errores en rojo

### Problema 4: "Error: Memory limit exceeded"

**Solución:** Usa modelo más ligero

Edita `app.py` línea 30:
```python
# Cambiar de:
model_name='paraphrase-multilingual-MiniLM-L12-v2'

# A:
model_name='paraphrase-MiniLM-L6-v2'
```

Luego:
```bash
git add app.py
git commit -m "Use lighter model for deployment"
git push origin main
```

### Problema 5: No puedo encontrar mi repo

**Solución:**
1. Asegúrate de haber hecho push a GitHub
2. Refresca la página de Streamlit Cloud
3. O pega el URL completo: `https://github.com/tu-usuario/ProyectoAnalisisSimilitud`

---

## 📊 Métricas de la App

Una vez desplegada, puedes ver estadísticas:

1. Ve al dashboard de Streamlit Cloud
2. Click en tu app
3. Verás:
   - 👥 Número de visitantes
   - 📈 Uso de recursos
   - 📝 Logs en tiempo real
   - ⚡ Tiempo de respuesta

---

## ⚙️ Configuraciones Avanzadas

### Cambiar el Nombre de la App

1. En el dashboard, click en "⋮" → "Settings"
2. "General" → "App URL"
3. Cambia el nombre
4. Click "Save"

### Hacer la App Privada (Requiere cuenta Teams)

Por defecto, la app es pública. Si quieres hacerla privada:
1. Upgrade a Streamlit Teams (de pago)
2. "Settings" → "Sharing"
3. Selecciona "Private"

### Agregar Secrets (Variables de Entorno)

Si en el futuro necesitas API keys:

1. Dashboard → Tu app → "⋮" → "Settings"
2. "Secrets"
3. Añade en formato TOML:
```toml
API_KEY = "tu-api-key"
```
4. En el código accede con:
```python
import streamlit as st
api_key = st.secrets["API_KEY"]
```

---

## 📱 Compartir Tu App

### Opción 1: Link Directo
```
https://[tu-nombre].streamlit.app
```

### Opción 2: QR Code

Genera un QR code para tu app:
1. Ve a https://www.qr-code-generator.com/
2. Pega tu URL de Streamlit
3. Descarga el QR
4. Comparte en presentaciones

### Opción 3: Embed en Sitio Web

```html
<iframe
  src="https://[tu-nombre].streamlit.app"
  height="800"
  width="100%"
></iframe>
```

---

## 🎓 Tips para Presentar Tu App

### En una Presentación:

1. **Abre la app antes** (si estuvo dormida, tarda 30s en despertar)
2. **Prepara textos de ejemplo** para demostrar
3. **Ten screenshot** por si internet falla
4. **Explica las 4 dimensiones** del análisis (semántico, léxico, estructural, secuencia)

### En un Reporte:

```markdown
# Aplicación Web Desplegada

La aplicación está disponible públicamente en:
https://detector-plagio-ia.streamlit.app

Características:
- Análisis multidimensional de plagio
- Interfaz web interactiva
- Visualizaciones con Plotly
- Soporte para español e inglés
- Procesamiento con IA (Sentence-BERT)

Deployment:
- Plataforma: Streamlit Cloud
- Tecnologías: Python, Streamlit, PyTorch, Transformers
- Tiempo de respuesta: 3-8 segundos por análisis
```

---

## 📞 Soporte

Si tienes problemas:

1. **Revisa los logs:**
   - Dashboard → Tu app → "⋮" → "View logs"

2. **Foro de Streamlit:**
   - https://discuss.streamlit.io/

3. **Documentación oficial:**
   - https://docs.streamlit.io/streamlit-community-cloud

4. **Reboot la app:**
   - Dashboard → Tu app → "⋮" → "Reboot app"

---

## ✅ Checklist Final

Antes de compartir tu app, verifica:

- [ ] La app carga sin errores
- [ ] Puedes comparar dos textos
- [ ] Los gráficos se muestran correctamente
- [ ] El cambio de idioma funciona
- [ ] La carga de archivos funciona
- [ ] Los resultados son coherentes
- [ ] La URL es apropiada para compartir

---

## 🎯 Resumen

**Comando único para empezar:**
```bash
git add . && git commit -m "Deploy to Streamlit" && git push origin main
```

**Luego:**
1. Ve a https://share.streamlit.io
2. Click "New app"
3. Selecciona tu repo
4. Deploy

**Tiempo total:** 15 minutos
**Costo:** $0
**Resultado:** App online y pública ✅

---

¡Éxito con tu deployment! 🚀
