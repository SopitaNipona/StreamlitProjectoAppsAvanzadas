# 🎯 DEPLOY AHORA - Pasos Exactos

Sigue estos pasos en orden para tener tu app online en 10 minutos.

---

## ✅ Paso 1: Preparar el Repositorio (2 minutos)

Ejecuta estos comandos en tu terminal:

```bash
# Navega a tu proyecto
cd /home/diego/github/ProyectoAnalisisSimilitud

# Da permisos de ejecución al script
chmod +x setup.sh

# Añade todos los archivos
git add .

# Haz commit
git commit -m "Add deployment configuration for Streamlit Cloud"

# Sube a GitHub
git push origin main
```

---

## ✅ Paso 2: Crear Cuenta en Streamlit Cloud (1 minuto)

1. Ve a: **https://share.streamlit.io**
2. Click en **"Sign in with GitHub"**
3. Autoriza a Streamlit para acceder a tus repositorios

---

## ✅ Paso 3: Desplegar la App (2 minutos)

1. En Streamlit Cloud, click en **"New app"**

2. Completa el formulario:
   ```
   Repository: tu-usuario/ProyectoAnalisisSimilitud
   Branch: main
   Main file path: app.py
   ```

3. (Opcional) Click en **"Advanced settings"** y configura:
   ```
   Python version: 3.9
   ```

4. Click en **"Deploy!"**

---

## ✅ Paso 4: Esperar el Build (5-10 minutos)

Verás una pantalla con logs en tiempo real. Espera a que veas:

```
✅ Your app is now deployed!
```

Tu app estará disponible en:
```
https://[tu-app-nombre].streamlit.app
```

---

## 🎉 ¡Listo!

Tu aplicación ya está online y accesible para cualquier persona con el link.

### Comparte tu app:
```
https://[tu-app-nombre].streamlit.app
```

---

## 🔄 Para Actualizar en el Futuro

Simplemente haz push a GitHub y la app se actualiza sola:

```bash
# Hacer cambios en el código
git add .
git commit -m "Mejora X"
git push origin main

# ¡La app se redespliega automáticamente!
```

---

## ⚠️ Si Algo Sale Mal

### Error: "Command failed with exit code 1"
- Revisa los logs en Streamlit Cloud
- Verifica que `requirements.txt` esté correcto

### Error: "Could not find spacy model"
- Asegúrate que `setup.sh` tiene permisos: `chmod +x setup.sh`
- Verifica que está en la raíz del proyecto

### La app está muy lenta
- Esto es normal en la primera carga
- Las siguientes cargas serán más rápidas gracias al caché

### La app se "duerme"
- Esto es normal en el plan gratuito
- Se reactiva automáticamente cuando alguien la visita

---

## 📱 Próximos Pasos

1. **Prueba tu app** visitando la URL
2. **Comparte el link** con tus profesores/compañeros
3. **Monitorea el uso** en el dashboard de Streamlit Cloud

---

## 📚 Documentación Adicional

- **Guía rápida:** [README_DEPLOYMENT.md](README_DEPLOYMENT.md)
- **Guía completa:** [DEPLOYMENT.md](DEPLOYMENT.md)

---

¡Éxito! 🚀
