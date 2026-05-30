# COFAI – ANÁLISIS DE VENTAS POR PRODUCTO Y CATEGORÍA

# =============================================================================

# Estructura del repositorio esperada:
#   cofai-ventas/
#   ├── datos/ventas_cofai.csv
#   ├── scripts/analisis_ventas_cofai.py   ← este archivo
#   └── resultados/                        ← se crea automáticamente

import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
# sys para detectar el entorno de ejecución (Colab o local).
# os para manejo de rutas.
# Se implemento pandas como libreria para la manipulación de datos 
# matplotlib para la visualización 

# =============================================================================
# RUTAS RELATIVAS


# Detecta automáticamente si el script corre en Colab o en local.
# En Colab el módulo 'google.colab' está disponible; en local no existe.
IN_COLAB = 'google.colab' in sys.modules

if IN_COLAB:
    BASE_DIR = "/content/cofai-ventas"
else:
    # En local usa la ubicación real del archivo para construir la ruta raíz
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATOS_DIR = os.path.join(BASE_DIR, "datos") #/datos
RESULTADOS_DIR = os.path.join(BASE_DIR, "resultados") #/resultados
os.makedirs(RESULTADOS_DIR, exist_ok=True) # crea la carpeta resultados si no existe


# =============================================================================
# CARGA Y PREPARACIÓN DEL DATASET

ruta_csv = os.path.join(DATOS_DIR, "ventas_cofai.csv") # ruta al archivo CSV de ventas
datos = pd.read_csv(ruta_csv) 

# Normalización: lowercase y sin espacios para robustez ante variantes de CSV
datos.columns = [col.strip().lower().replace(" ", "_") for col in datos.columns]
datos["fecha_venta"] = pd.to_datetime(datos["fecha_venta"]) # convertimos a formato fecha para análisis temporal

# Agregamos una columna de "mes" para análisis mensual (formato Periodo: '2025-01', '2025-02', etc.)
datos["mes"] = datos["fecha_venta"].dt.to_period("M")

# =============================================================================
# INFORMACIÓN GENERAL (consola)

print("=" * 60)
print("  COFAI – REPORTE DE VENTAS ENERO–JUNIO 2025")
print("=" * 60)
print(f"\nRegistros cargados: {len(datos)}")
print(f"Período: {datos['fecha_venta'].min().date()} → {datos['fecha_venta'].max().date()}")
print(f"Categorías: {sorted(datos['categoria'].unique())}")
print()


# =============================================================================
# CÁLCULOS

# • Uso de las siguentes funciones de pandas para el análisis:
# groupby: agrupa los datos por categoría y calcula la facturación total, unidades vendidas y número de transacciones para cada categoría.
# agg: función de pandas que permite aplicar múltiples agregaciones a diferentes columnas de un DataFrame.
# unstack: reorganiza el resultado del groupby para que las categorías se conviertan en columnas, facilitando la visualización y análisis posterior.

# Agrupa los datos por mes y categoría, suma la facturación, reorganiza el resultado en formato de tabla y calcula la facturación total por mes para superponerla en el gráfico.

# Facturación total ---
facturacion_total = datos["monto_venta"].sum()
print(f"📦 Facturación total del período: ${facturacion_total:,.0f}")

# Unidades totales vendidas ---
unidades_totales = datos["cantidad_vendida"].sum()
print(f"🛒 Unidades totales vendidas: {unidades_totales}")

# Producto más vendido (unidades) ---
prod_unidades = datos.groupby("producto")["cantidad_vendida"].sum().sort_values(ascending=False)
print(f"🏆 Producto más vendido (unidades): {prod_unidades.index[0]} ({prod_unidades.iloc[0]} uds.)")

# EVOLUCIÓN MENSUAL POR CATEGORÍA
ventas_mensuales_categoria = datos.groupby(["mes", "categoria"])["monto_venta"].sum().unstack(fill_value=0)
ventas_mensuales_totales = datos.groupby("mes")["monto_venta"].sum()

ventas_men_categoria_total = ventas_mensuales_categoria.copy()
ventas_men_categoria_total["Total General"] = ventas_mensuales_totales 
# creo una variable nueva que adjunte la columna con los totales para luego mostrarla en el gráfico de evolución mensual por categoría y total general

print("\n📅 Facturación Mensual por Categoría y total ($) ---")
print(ventas_men_categoria_total.to_string())

# ANÁLISIS POR CATEGORÍA
cat_stats = datos.groupby("categoria").agg(
    facturacion=("monto_venta", "sum"),
    unidades=("cantidad_vendida", "sum"),
    transacciones=("id", "count")
).sort_values("facturacion", ascending=False)

print("\n🔖 Ventas por Categoría ---")
print(cat_stats.to_string())

# =============================================================================

# Tabla de indicadores por categoría
ruta_cat = os.path.join(RESULTADOS_DIR, "ventas_por_categoria.csv")
cat_stats.to_csv(ruta_cat)
print(f"\n✅ Tabla de categorías guardada: {ruta_cat}")

# Tabla mensual por categoría
ruta_mens = os.path.join(RESULTADOS_DIR, "ventas_mensuales_por_categoria.csv")
ventas_mensuales_categoria.to_csv(ruta_mens)
print(f"✅ Tabla mensual guardada: {ruta_mens}")

# guardo las tablas de resultados en formato CSV dentro de la carpeta resultados para su posterior análisis o presentación.

# =============================================================================
# GRÁFICO – EVOLUCIÓN MENSUAL DE VENTAS POR CATEGORÍA Y TOTAL GENERAL

plt.figure(figsize=(9,5))
# figure: crea una nueva figura para el gráfico con un tamaño específico (9 pulgadas de ancho por 5 pulgadas de alto).

colores = ["#D12B1F", "#2F52B1", "#9B6928", "#0CEE3D"]  # Máximo 3 colores para categorías + total general
for i, cat in enumerate(ventas_men_categoria_total.columns[:4]):
    plt.plot(ventas_men_categoria_total.index.astype(str), ventas_men_categoria_total[cat], marker="o", label=cat, color=colores[i])
# plot: dibuja una línea en el gráfico para cada categoría y otra línea para el total general, con marcadores en cada punto de datos y estilos de línea específicos.
# index.astype(str): convierte el índice de meses a cadenas de texto para que se muestren correctamente en el eje x.
# enumerate: se utiliza para iterar sobre las categorías y asignar un color específico a cada una.

plt.title("Evolución Mensual de Ventas por Categoría y Total")
plt.xlabel("Mes")
plt.ylabel("Facturación ($)")
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.tight_layout()
# title, xlabel, ylabel: establecen el título del gráfico y las etiquetas de los ejes.
# grid: agrega una cuadrícula al fondo del gráfico para mejorar la legibilidad.
# legend: muestra una leyenda que identifica cada línea del gráfico.
# tight_layout: ajusta automáticamente el diseño del gráfico para evitar solapamientos y asegurar que

ruta_grafico = os.path.join(RESULTADOS_DIR, "grafico_evolucion_mensual_categorias_y_total.png")
plt.savefig(ruta_grafico, dpi=150, bbox_inches="tight")
plt.show()
# savefig: guarda el gráfico generado en la ruta especificada con una resolución de 150 dpi y ajustando los bordes para que no se recorten elementos del gráfico.
# show: muestra el gráfico en pantalla.
# Finalmente, se imprime un mensaje confirmando que el gráfico ha sido guardado correctamente en la ubicación especificada.

print(f"✅ Gráfico guardado: {ruta_grafico}")

