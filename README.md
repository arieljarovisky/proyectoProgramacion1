# 📦 Caja Plus

**Gestión integral para pequeños comercios y emprendedores**

---

## 🧩 Proyecto académico - Algoritmos y Estructuras de Datos I

**Integrantes:**
- Andrés Cecconi 🔗 [GitHub](https://github.com/andres-Cecconi)
- Ariel Jarovisky 🔗 [GitHub](https://github.com/arieljarovisky)
- Ignacio Ganci 🔗 [GitHub](https://github.com/IGanci)

**Docente:** María Julia Monasterio  
**Año:** 2025

---

## 📝 Descripción General

**Caja Plus** es una aplicación web diseñada para simplificar y optimizar la gestión diaria de pequeños comercios y emprendimientos. Ofrece un sistema centralizado que integra:

- Control de ingresos y egresos
- Gestión de stock de productos
- Registro de ventas
- Generación de reportes analíticos
- Alertas automáticas de stock bajo
- Métricas predictivas basadas en patrones de consumo

Todo en una plataforma accesible, intuitiva y pensada para usuarios sin conocimientos técnicos avanzados.

---

## 🎯 Objetivos

- Digitalizar y automatizar procesos comerciales cotidianos
- Mejorar el control financiero y de inventario
- Brindar información precisa para la toma de decisiones inteligentes
- Ofrecer una solución adaptable a múltiples rubros comerciales

---

## 📦 Módulos del Sistema

### 🛒 Módulo de Stock
- Registro, edición y baja de productos
- Alertas por stock mínimo configurable
- Visualización de inventario actualizado

### 💵 Módulo de Ventas y Caja
- Registro de ventas y egresos
- Impacto automático en inventario y saldo
- Eliminación segura de movimientos
- Consulta de historial de movimientos

### 📊 Módulo de Reportes
- Generación de métricas: productos más vendidos, estacionalidad de ventas
- Filtros por fecha, tipo de movimiento y categoría
- Balance de caja por período

### 🔐 Funcionalidades Cross-Módulo
- Sistema de login de usuario
- Modo claro/oscuro para mejorar la experiencia de uso
- Conexión frontend-backend mediante `fetch()`
- Manejo de excepciones y validaciones de datos

---

## 🌟 Beneficios Principales

- **Ahorro de tiempo**: Automatización de tareas administrativas
- **Mayor control**: Finanzas y stock bajo supervisión
- **Visibilidad**: Información clara para la toma de decisiones
- **Escalabilidad**: Adaptable a distintos tipos de negocios

---

## 🛠️ Tecnologías Utilizadas

- **Frontend:** HTML, CSS (TailwindCSS), JavaScript
- **Backend:** Python (Flask)
- **Base de Datos:** Archivos locales en formato JSON

---

## 🚤 Cómo levantar el proyecto (setup)

### 1. Cloná ambos repositorios:
- Frontend: `https://github.com/...`
- Backend: `https://github.com/...`

### 2. Instalá dependencias del backend:
Desde la terminal, ingresá en la carpeta del backend y ejecutá el siguiente comando para instalar las dependencias necesarias:

```bash
cd backend
pip install -r requirements.txt
```

### 3. Ejecutá el servidor del backend:
En la misma terminal, iniciá el servidor Flask ejecutando:

```bash
python app.py
```

Se mostrará una URL local (por ejemplo: `http://127.0.0.1:5000` o similar).

### 4. Configurá la conexión del frontend:

- Ingresá en la carpeta del frontend.
- Dentro del directorio `js/`, abrí el archivo `config.js`.
- Reemplazá la URL de la constante `API_BASE_URL` por la URL local que te indicó el servidor backend.

Ejemplo:
```js
const API_BASE_URL = "http://127.0.0.1:5000";
```

Esta configuración permite que el frontend se comunique correctamente con el backend.

### 5. Abrí el frontend
Podés abrir el archivo `index.html` en tu navegador preferido. El sistema debería estar funcionando y conectado al backend correctamente.


## 🛤️ Plan de Entregas

### 🚀 Entrega 40%
- Estructura base del frontend y backend
- Configuración de entorno en GitHub
- Sistema de login de usuarios
- Formulario inicial para ingresos/egresos
- Almacenamiento de datos en JSON

### 🚀 Entrega 80%
- Registro completo de ventas y egresos
- Actualización de stock en tiempo real
- Implementación de tabla de movimientos
- Validaciones de formularios y errores
- Aplicación de estilos (TailwindCSS)

### 🚀 Entrega 100%
- Filtros avanzados en reportes
- Métricas de ventas y consumo
- Alertas automáticas por bajo stock
- Modo claro/oscuro
- Optimización de API y documentación final

---

## 🏁 Estado del Proyecto

✅ Entrega 40% completada  ✅
✅ Entrega 80% en proceso...
✅ Entrega 100% en proceso... 

¡Gracias por visitar nuestro proyecto!
