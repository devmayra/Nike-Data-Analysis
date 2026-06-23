# Nike Global Products — Análisis Exploratorio de Datos

Análisis exploratorio de un dataset global de productos Nike. El objetivo es entender la distribución de precios entre países y categorías, identificar los productos más caros, y explorar la disponibilidad de stock y los deportes más representados en el catálogo.

## Tecnologías

- Python 3
- pandas
- matplotlib

## Dataset

El dataset original pesa más de 25 MB y no puede subirse a GitHub, por lo que se incluye una versión reducida:

```
global_nike_small.csv
```

Es una muestra de 10.000 filas del dataset completo y permite ejecutar el análisis sin problemas. El dataset original puede encontrarse en [Kaggle](https://www.kaggle.com/datasets/bsthere/nike-global-catalogue-2026).

## Cómo ejecutar

1. Clonar el repositorio:

```bash
git clone https://github.com/devmayra/Nike-Data-Analysis
```

2. Asegurarse de que estos archivos estén en la misma carpeta:

```
nike_analysis.py
global_nike_small.csv
```

3. Ejecutar el script:

```bash
python nike_analysis.py
```

Compatible con cualquier entorno Python estándar.

## Limpieza de datos

Antes del análisis se aplican los siguientes pasos:

- Eliminación de columnas completamente vacías (`size_count`, `employee_price`, `gtin`, etc.)
- Eliminación de duplicados
- Filtrado de precios: se descartan valores en 0 y outliers por encima del percentil 99
- Relleno de valores nulos en columnas categóricas con `"UNKNOWN"`
- Relleno de descuentos nulos con `0`

## Conversión a USD

El dataset incluye precios en moneda local (`price_local`) y una columna `currency` con el código de cada moneda. Como los precios no son comparables directamente entre países, se convierten a USD usando tasas de cambio aproximadas al momento del snapshot (2026-03-19). Esto permite comparar categorías y productos en una unidad común.

## Análisis y gráficos

### 1. Precio promedio por categoría (USD)
Gráfico de barras con el precio promedio en USD para cada categoría de producto (calzado, ropa, accesorios, etc.). Permite comparar el rango de precios entre segmentos sin que las diferencias de moneda distorsionen el resultado.

### 2. Top 10 productos más caros (USD)
Gráfico de barras horizontales con los 10 productos individuales de mayor precio convertido a USD. Útil para detectar ítems premium o de edición limitada independientemente del país de origen.

### 3. Distribución de precios en USD (escala logarítmica)
Histograma que muestra cómo se distribuyen los precios convertidos a USD. Se usa escala logarítmica en el eje X porque la mayoría de los productos se concentran en un rango acotado, pero hay algunos con precios muy altos que distorsionan la escala lineal. Con escala log se puede ver la forma real de la distribución.

### 4. Top 10 países con más productos
Gráfico de barras con los países que tienen más entradas en el dataset. Refleja la cobertura geográfica del catálogo Nike y el tamaño relativo de cada mercado en la muestra.

### 5. Disponibilidad de stock por categoría (%)
Gráfico de barras apiladas que muestra, para cada categoría, qué porcentaje de productos estaban en stock al momento del snapshot. Permite ver si hay categorías con problemas de disponibilidad o si el stock está distribuido de forma pareja.

### 6. Top deportes por cantidad de productos
Gráfico de barras horizontales con los deportes más representados en el catálogo. La columna `sport_tags` puede tener múltiples valores por producto (ej: `"Soccer|Training & Gym"`), por lo que cada etiqueta se cuenta por separado para reflejar mejor la cobertura real por deporte.

## Estructura del repositorio

```
├── nike_analysis.py          # Script principal
├── global_nike_small.csv     # Dataset reducido (muestra de 10.000 filas)
└── README.md
```
