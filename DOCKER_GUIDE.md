# 🐳 Guía Docker (Opcional)

> **⚠️ IMPORTANTE:** Docker NO es recomendado para este proyecto. Lee [DOCKER_VS_STREAMLIT_ANALYSIS.md](DOCKER_VS_STREAMLIT_ANALYSIS.md) primero.
>
> **Usa Streamlit Cloud** (ver [DEPLOY_NOW.md](DEPLOY_NOW.md)) a menos que tengas una razón específica para usar Docker.

Esta guía es solo para referencia o experimentación local.

---

## ¿Por Qué NO Usar Docker Para Este Proyecto?

| | Streamlit Cloud | Docker |
|---|---|---|
| **Costo** | $0/año | $144-288/año |
| **Setup** | 10 min | 3 horas |
| **Mantenimiento** | 0 hrs/mes | 2-5 hrs/mes |
| **Complejidad** | Muy bajo | Alto |

**Veredicto:** Streamlit Cloud ahorra $200+/año y 50+ horas de trabajo.

---

## Uso de Docker Localmente (Para Desarrollo)

### 1. Build de la Imagen

```bash
# Build de la imagen Docker
docker build -t detector-plagio:latest .

# Esto tarda 5-10 minutos la primera vez
```

### 2. Ejecutar el Container

```bash
# Ejecutar la aplicación
docker run -p 8501:8501 detector-plagio:latest

# La app estará disponible en: http://localhost:8501
```

### 3. Usar docker-compose (Más Fácil)

```bash
# Iniciar la aplicación
docker-compose up

# Con rebuild (después de cambios en código)
docker-compose up --build

# En segundo plano (detached)
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

---

## Comandos Útiles

### Gestión de Containers

```bash
# Ver containers corriendo
docker ps

# Ver todos los containers
docker ps -a

# Detener container
docker stop detector-plagio-app

# Eliminar container
docker rm detector-plagio-app

# Ver logs
docker logs detector-plagio-app -f
```

### Gestión de Imágenes

```bash
# Listar imágenes
docker images

# Eliminar imagen
docker rmi detector-plagio:latest

# Limpiar imágenes no usadas
docker image prune -a
```

### Debugging

```bash
# Entrar al container (shell interactivo)
docker exec -it detector-plagio-app /bin/bash

# Verificar uso de recursos
docker stats detector-plagio-app

# Inspeccionar container
docker inspect detector-plagio-app
```

---

## Deployment en Producción con Docker

### Opción 1: DigitalOcean Droplet

**Costo:** $12-24/mes

```bash
# 1. Crear droplet Ubuntu 22.04
# 2. SSH al servidor
ssh root@tu-ip

# 3. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# 4. Instalar docker-compose
apt install docker-compose

# 5. Clonar repositorio
git clone https://github.com/tu-usuario/ProyectoAnalisisSimilitud.git
cd ProyectoAnalisisSimilitud

# 6. Ejecutar con docker-compose
docker-compose up -d

# 7. Configurar nginx reverse proxy (opcional)
# Ver sección "Nginx Configuration" abajo
```

### Opción 2: AWS ECS / Google Cloud Run

**Costo:** Variable ($10-50/mes)

Requiere configuración específica de cada plataforma.

### Opción 3: Render.com (Con Docker)

Render puede usar tu Dockerfile automáticamente:

1. Ve a render.com
2. "New" → "Web Service"
3. Conecta tu repo
4. Render detecta Dockerfile automáticamente
5. Deploy

**Costo:** $7-25/mes

---

## Configuración Nginx (Para Producción)

Si despliegas en VPS, configura nginx como reverse proxy:

```nginx
# /etc/nginx/sites-available/detector-plagio

server {
    listen 80;
    server_name tu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts para requests largos
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

```bash
# Habilitar sitio
ln -s /etc/nginx/sites-available/detector-plagio /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx

# Configurar SSL con Let's Encrypt
apt install certbot python3-certbot-nginx
certbot --nginx -d tu-dominio.com
```

---

## Optimizaciones Docker

### 1. Multi-stage Build (Reducir Tamaño)

```dockerfile
# Dockerfile optimizado
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app
COPY . .
RUN python -m spacy download es_core_news_md

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### 2. Usar .dockerignore

Ya incluido en el proyecto. Reduce tamaño de build context.

### 3. Cachear Layers

Orden óptimo en Dockerfile:
1. Sistema dependencies (cambian raramente)
2. requirements.txt (cambian ocasionalmente)
3. Código fuente (cambia frecuentemente)

---

## Monitoreo y Logs

### Logs con docker-compose

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Solo de la app
docker-compose logs -f detector-plagio

# Últimas 100 líneas
docker-compose logs --tail=100
```

### Logs en Producción

Configurar log rotation:

```yaml
# docker-compose.yml
services:
  detector-plagio:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

---

## Troubleshooting

### Problema: "Port 8501 already in use"

```bash
# Ver qué está usando el puerto
lsof -i :8501

# Matar el proceso
kill -9 <PID>

# O usar otro puerto
docker run -p 8502:8501 detector-plagio
```

### Problema: Container crashea inmediatamente

```bash
# Ver logs del container fallido
docker logs <container-id>

# Ejecutar con terminal interactivo para debugging
docker run -it detector-plagio /bin/bash
```

### Problema: Out of memory

```bash
# Aumentar límite de memoria
docker run --memory=2g -p 8501:8501 detector-plagio

# O en docker-compose.yml
services:
  detector-plagio:
    mem_limit: 2g
```

### Problema: Build muy lento

```bash
# Limpiar cache de Docker
docker builder prune

# Build sin cache
docker build --no-cache -t detector-plagio .
```

---

## Comparación de Tamaños

```
Imagen sin optimizar: ~2.5 GB
Imagen con multi-stage: ~1.8 GB
Imagen python:alpine (no recomendada): ~1.2 GB pero problemas de compatibilidad
```

---

## CI/CD con Docker

### GitHub Actions

```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Build Docker image
        run: docker build -t detector-plagio .

      - name: Test Docker image
        run: docker run -d -p 8501:8501 detector-plagio

      # Push a Docker Hub (opcional)
      - name: Login to Docker Hub
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Push to Docker Hub
        run: |
          docker tag detector-plagio tu-usuario/detector-plagio:latest
          docker push tu-usuario/detector-plagio:latest
```

---

## Costo Total Estimado (Año 1)

### Opción Docker en VPS

```
DigitalOcean Droplet (2GB): $12/mes × 12 = $144
Dominio: $12/año
SSL: Gratis (Let's Encrypt)
---
Total: $156/año

Tiempo de setup: 4-6 horas
Tiempo de mantenimiento: 3 horas/mes = 36 horas/año
Valor del tiempo (@$20/hr): $800/año

Costo total real: $156 + $800 = $956/año
```

### Opción Streamlit Cloud

```
Hosting: $0/año
Dominio: Incluido (.streamlit.app)
SSL: Incluido
---
Total: $0/año

Tiempo de setup: 10 minutos
Tiempo de mantenimiento: 0 horas/año

Costo total real: $0/año
```

**Ahorro usando Streamlit Cloud: $956/año** 💰

---

## Conclusión

Docker es excelente para:
- ✅ Múltiples microservicios
- ✅ Infraestructura compleja
- ✅ Requisitos específicos del sistema
- ✅ On-premise deployments

Pero para tu app Streamlit:
- ❌ Complejidad innecesaria
- ❌ Costo adicional
- ❌ Más mantenimiento
- ❌ Sin beneficios reales

**Recomendación final: Usa Streamlit Cloud** 🎯

Ver [DEPLOY_NOW.md](DEPLOY_NOW.md) para empezar en 10 minutos.

---

## Referencias

- [Docker Documentation](https://docs.docker.com/)
- [Streamlit Docker Deployment](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
