# 🚀 Guía Rápida de Deployment

Esta aplicación puede desplegarse gratuitamente en **Streamlit Community Cloud** o **Render.com**.

---

## ⚡ Quick Start - Streamlit Cloud (5 minutos)

### Paso 1: Preparar el Código

```bash
# Dar permisos de ejecución al script de setup
chmod +x setup.sh

# Commit y push
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

### Paso 2: Desplegar

1. Ve a **[share.streamlit.io](https://share.streamlit.io)**
2. Inicia sesión con GitHub
3. Click en **"New app"**
4. Configura:
   - **Repository:** Tu repositorio
   - **Branch:** `main`
   - **Main file:** `app.py`
5. Click en **"Deploy!"**

### Paso 3: ¡Listo!

Tu app estará en: `https://tu-app.streamlit.app`

⏱️ **Tiempo total:** 5-10 minutos

---

## 📋 Archivos Necesarios (Ya Incluidos)

- ✅ `app.py` - Aplicación principal
- ✅ `requirements.txt` - Dependencias Python
- ✅ `packages.txt` - Dependencias del sistema
- ✅ `setup.sh` - Script para descargar modelos spaCy
- ✅ `.streamlit/config.toml` - Configuración de Streamlit

---

## 🔧 Troubleshooting Común

### La app no carga:
- Verifica que `setup.sh` tenga permisos: `chmod +x setup.sh`
- Revisa los logs en el dashboard de Streamlit Cloud

### Error de memoria:
- El plan gratuito tiene 1GB RAM
- Si es necesario, cambia a modelo más ligero en `app.py` línea 30:
  ```python
  model_name='paraphrase-MiniLM-L6-v2'  # Más ligero
  ```

### La app se "duerme":
- Normal en plan gratuito después de inactividad
- Se reactiva automáticamente al visitarla (~30 segundos)

---

## 📚 Documentación Completa

Para instrucciones detalladas, incluyendo deployment en Render.com, optimizaciones y troubleshooting avanzado:

👉 **[Ver DEPLOYMENT.md](DEPLOYMENT.md)**

---

## 🔄 Actualizar la App

Cada vez que hagas push a `main`, la app se actualiza automáticamente:

```bash
# Hacer cambios en el código
git add .
git commit -m "Mejora en la funcionalidad X"
git push origin main

# La app se redespliega automáticamente en 2-3 minutos
```

---

## 📊 Comparación de Plataformas

| | Streamlit Cloud | Render.com |
|---|---|---|
| **Facilidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **RAM (free)** | 1 GB | 512 MB |
| **Setup** | 5 min | 10 min |
| **Mejor para** | Apps Streamlit | Apps genéricas |

**Recomendación:** Usa Streamlit Cloud para este proyecto.

---

## ✅ Checklist Pre-Deployment

- [ ] `setup.sh` tiene permisos de ejecución
- [ ] Todo el código está en GitHub
- [ ] La app funciona localmente: `streamlit run app.py`
- [ ] Has hecho commit de todos los cambios

---

## 🆘 Soporte

- [Documentación Streamlit Cloud](https://docs.streamlit.io/streamlit-community-cloud)
- [Foro de Streamlit](https://discuss.streamlit.io/)
- [Documentación de Render](https://render.com/docs)

---

¡Buena suerte! 🎉
