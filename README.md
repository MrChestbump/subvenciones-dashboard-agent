# 📊 Dashboard de Subvenciones

**Agente automático de consulta de subvenciones y actualización del dashboard**

## 🚀 Descripción

Sistema automatizado que:
- **Consulta diariamente** fuentes de subvenciones (BDNS, fondos europeos, etc.)
- **Almacena datos** en formato JSON
- **Actualiza automáticamente** el dashboard con nuevas oportunidades
- **Ejecuta mediante GitHub Actions** sin necesidad de servidores externos

## 📋 Estructura del Proyecto

```
subvenciones-dashboard-agent/
├── .github/
│   └── workflows/
│       └── daily.yml          # Workflow de GitHub Actions
├── scraper.py              # Script de scraping
├── dashboard.html          # Dashboard visualización
├── subvenciones.json       # Datos generados (auto-actualizado)
└── README.md
```

## ⚙️ Configuración

### 1. GitHub Actions

El workflow se ejecuta automáticamente:
- **Diariamente a las 8:00 AM UTC**
- **Manualmente** desde Actions > Daily Subsidy Scraper > Run workflow

### 2. Personalizar Fuentes

Edita `scraper.py` para añadir tus fuentes específicas:

```python
SOURCES = [
    {
        "name": "BDNS",
        "url": "https://www.pap.hacienda.gob.es/bdnstrans/GE/es/index",
        "type": "scraper"
    },
    # Añade más fuentes aquí
]
```

### 3. Ver el Dashboard

**Opción A: Archivo local**
- Descarga `dashboard.html` y ábrelo en tu navegador

**Opción B: GitHub Pages** (recomendado)
1. Ve a Settings > Pages
2. Selecciona branch: `main`, folder: `/ (root)`
3. Save
4. Tu dashboard estará en: `https://mrchestbump.github.io/subvenciones-dashboard-agent/dashboard.html`

## 🛠️ Uso

### Ejecutar Manualmente

1. Ve a la pestaña **Actions**
2. Selecciona **Daily Subsidy Scraper**
3. Click en **Run workflow**
4. Los resultados se guardarán en `subvenciones.json`

### Datos Generados

Formato JSON:
```json
{
  "fecha": "2025-01-15T08:00:00",
  "total": 25,
  "subvenciones": [
    {
      "titulo": "...",
      "organismo": "...",
      "fecha_limite": "...",
      "url": "..."
    }
  ]
}
```

## 📝 Próximos Pasos

- [ ] Personalizar `scraper.py` con fuentes reales
- [ ] Activar GitHub Pages para el dashboard
- [ ] Integrar dashboard de CodePen con 71 clientes
- [ ] Configurar notificaciones por email/Slack
- [ ] Añadir filtros por sector/región

## 🔒 Permisos

GitHub Actions tiene permisos de escritura para actualizar archivos automáticamente.

## 💬 Soporte

Para dudas o mejoras, crea un Issue en este repositorio.
