# ☕ Cofai – Análisis de Ventas E-commerce

> Trabajo Práctico: Gestión Colaborativa, Control de Versiones y Organización Empresarial
> Cátedra Organización Empresarial · UTN TUP · 2026

---

## Descripción del Proyecto

**Cofai** es una empresa tostadora de café especialidad con canal de venta e-commerce.
Su catálogo incluye tres líneas de productos:

| Categoría | Productos |
|---|---|
| **Granos** | Blend Cofai, Etiopía, Brasil Cerrado, Colombia Huila — en 250g y 1kg |
| **Cafeteras** | DeLonghi Dedica EC685, DeLonghi Magnifica Evo, Philips Serie 3200 LatteGo |
| **Accesorios** | Molinillo Manual Hario, Tamper Acero 58mm, Prensa Francesa 600ml |

Este repositorio contiene el análisis de ventas del primer semestre 2025, desarrollado
como ejercicio de gestión colaborativa con Git, GitHub y Jira.

---

## Integrante

| Nombre | Roles asumidos |
|---|---|
| Franco Peron | P1 – Hugo (Líder) · P2 – Paco (Dev) · P3 – Luis (QA) |

> Trabajo realizado en modalidad individual, habilitada por la cátedra.

---

## Estructura del Repositorio

```
cofai-ventas/
│
├── datos/
│   └── ventas_cofai.csv               # Dataset de ventas Ene–Jun 2025 (30 registros)
│
├── scripts/
│   └── analisis_ventas_cofai.py       # Script principal de análisis en Python
│
├── resultados/                        # Generado automáticamente al ejecutar el script
│   ├── ventas_por_categoria.csv
│   ├── ventas_mensuales_por_categoria.csv
│   └── grafico_evolucion_mensual_categorias_y_total.png
│
├── README.md
└── .gitignore
```

---

## Qué hace el script

El script `analisis_ventas_cofai.py` realiza el siguiente flujo:

1. **Carga y normalización** del CSV con pandas — columnas a lowercase, conversión de fechas
2. **Cálculo de indicadores globales** — facturación total, unidades vendidas, producto más vendido
3. **Análisis por categoría** — facturación, unidades de Granos, Cafeteras y Accesorios
4. **Exportación de resultados** — dos archivos CSV en `/resultados`
5. **Gráfico de líneas** — evolución mensual por categoría más línea de total general, guardado como PNG en `/resultados`

### Librerías utilizadas

| Librería | Uso |
|---|---|
| `os` | Manejo de rutas relativas para reproducibilidad en cualquier entorno |
| `pandas` | Carga, normalización, agrupación y análisis del dataset |
| `matplotlib` | Generación y exportación del gráfico de evolución mensual |

---

## Cómo ejecutar el script

### En Google Colab (método usado en el TP)

```python
# Celda 1 – Configurar identidad
!git config --global user.email "tu@email.com"
!git config --global user.name "Franco Peron"

# Celda 2 – Clonar el repositorio
!git clone https://github.com/FrancoPeron/cofai-ventas.git
%cd cofai-ventas

# Celda 3 – Instalar dependencias (ya disponibles en Colab)
!pip install pandas matplotlib --quiet

# Celda 4 – Ejecutar el análisis
!python scripts/analisis_ventas_cofai.py
```

### En entorno local

```bash
git clone https://github.com/FrancoPeron/cofai-ventas.git
cd cofai-ventas
pip install pandas matplotlib
python scripts/analisis_ventas_cofai.py
```

---

## Trazabilidad Jira

Cada commit respeta el formato `COFAI-N: descripción en tiempo presente`:

| Issue Jira | Commit | Rol |
|---|---|---|
| `COFAI-2` | `COFAI-2: Inicializar repositorio con estructura de carpetas` | P1 – Hugo |
| `COFAI-3` | `COFAI-3: Agregar dataset ventas_cofai.csv con datos del semestre` | P2 – Paco |
| `COFAI-4` | `COFAI-4: Desarrollar script analisis_ventas_cofai.py con indicadores y gráficos` | P2 – Paco |
| `COFAI-5` | `COFAI-5: Revisión de calidad y cierre del Pull Request` | P3 – Luis |

---

## Dependencias

- Python 3.8+
- `pandas >= 1.3`
- `matplotlib >= 3.4`
