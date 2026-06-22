import pandas as pd
import matplotlib.pyplot as plt

# -----------------------
# CARGA
# -----------------------
df = pd.read_csv("global_nike_small.csv")
print("Filas iniciales:", len(df))

# -----------------------
# LIMPIEZA
# -----------------------
df = df.drop(columns=["size_count", "available_size_count", "employee_price", "gtin"], errors="ignore")
df = df.drop_duplicates()
df = df.dropna(subset=["product_name", "price_local"])

limite = df["price_local"].quantile(0.99)
df = df[df["price_local"] > 0]
df = df[df["price_local"] <= limite]

categoricas = ["gender_segment", "subcategory", "brand_name", "color_name",
               "availability_level", "localized_size", "size_conversion_id", "sport_tags"]
for col in categoricas:
    if col in df.columns:
        df[col] = df[col].fillna("UNKNOWN")

if "discount_pct" in df.columns:
    df["discount_pct"] = df["discount_pct"].fillna(0)

df["product_name"] = df["product_name"].astype(str).str.strip()
print("Filas después de limpiar:", len(df))

# -----------------------
# CONVERSIÓN A USD
# Tasas aproximadas al snapshot del dataset (2026-03-19)
# -----------------------
TASAS_A_USD = {
    "ARS": 1 / 1050,   "AUD": 0.63, "BRL": 0.18,  "CAD": 0.74,
    "CHF": 1.13,        "CLP": 0.001,"CNY": 0.14,  "COP": 0.00024,
    "CZK": 0.044,       "DKK": 0.145,"EGP": 0.02,  "EUR": 1.08,
    "GBP": 1.27,        "HKD": 0.13, "HRK": 0.143, "HUF": 0.0028,
    "IDR": 0.000063,    "ILS": 0.28, "INR": 0.012, "JPY": 0.0067,
    "KRW": 0.00073,     "MXN": 0.052,"MYR": 0.225, "NOK": 0.095,
    "NZD": 0.59,        "PHP": 0.018,"PLN": 0.25,  "RON": 0.217,
    "SAR": 0.267,       "SEK": 0.096,"SGD": 0.75,  "SKK": 0.044,
    "THB": 0.029,       "TRY": 0.028,"TWD": 0.031, "USD": 1.0,
    "ZAR": 0.055,
}

df["tasa_usd"] = df["currency"].map(TASAS_A_USD)
df["price_usd"] = df["price_local"] * df["tasa_usd"]
sin_tasa = df["tasa_usd"].isna().sum()
if sin_tasa > 0:
    print(f"Monedas sin tasa definida ({sin_tasa} filas):", df[df["tasa_usd"].isna()]["currency"].unique())

df_usd = df.dropna(subset=["price_usd"])

# -----------------------
# ANÁLISIS
# -----------------------
print("\nPrecio promedio por categoría (USD):")
print(df_usd.groupby("category")["price_usd"].mean().sort_values(ascending=False))

print("\nTop 10 productos más caros (USD):")
print(df_usd.sort_values("price_usd", ascending=False)[["product_name", "currency", "price_local", "price_usd"]].head(10))

print("\nProductos con descuento:")
print(df[df["discount_pct"] > 0][["product_name", "currency", "price_local", "discount_pct"]].head(10))

print("\nProductos por país:")
print(df["country_code"].value_counts().head(10))

print("\nDisponibilidad general:")
print(df["in_stock"].value_counts())

# Explotar sport_tags (campo separado por |)
sport_series = df["sport_tags"].dropna()
sport_series = sport_series[sport_series != "UNKNOWN"]
todos_los_deportes = sport_series.str.split("|").explode().str.strip()
print("\nTop deportes:")
print(todos_los_deportes.value_counts().head(10))

# -----------------------
# GRÁFICOS
# -----------------------
COLOR  = "#111111"
BAR_COLOR = "#E5002B"
ACCENT = "#767676"
STOCK_COLORS = ["#E5002B", "#CCCCCC"]

# 1. Precio promedio por categoría (USD)
fig, ax = plt.subplots(figsize=(10, 5))
precios_cat = df_usd.groupby("category")["price_usd"].mean().sort_values()
precios_cat.plot(kind="bar", ax=ax, color=BAR_COLOR, edgecolor="none")
ax.set_title("Precio promedio por categoría (USD)", fontsize=14, fontweight="bold", color=COLOR, pad=12)
ax.set_xlabel("Categoría", fontsize=11, color=ACCENT)
ax.set_ylabel("Precio promedio (USD)", fontsize=11, color=ACCENT)
ax.tick_params(axis="x", rotation=45, labelsize=9)
ax.tick_params(axis="y", labelsize=9)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("grafico_precio_categoria.png", dpi=150)
plt.show()

# 2. Top 10 productos más caros (USD)
fig, ax = plt.subplots(figsize=(12, 5))
top10 = df_usd.sort_values("price_usd", ascending=False).drop_duplicates("product_name").head(10)
nombres = top10["product_name"].str[:35] + "…"
ax.barh(nombres, top10["price_usd"], color=BAR_COLOR, edgecolor="none")
ax.set_title("Top 10 productos más caros (USD)", fontsize=14, fontweight="bold", color=COLOR, pad=12)
ax.set_xlabel("Precio (USD)", fontsize=11, color=ACCENT)
ax.invert_yaxis()
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("grafico_top10_caros.png", dpi=150)
plt.show()

# 3. Distribución de precios en USD (escala logarítmica)
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df_usd["price_usd"], bins=60, color=BAR_COLOR, edgecolor="none", alpha=0.85)
ax.set_xscale("log")
ax.set_title("Distribución de precios (USD, escala logarítmica)", fontsize=14, fontweight="bold", color=COLOR, pad=12)
ax.set_xlabel("Precio en USD (escala log)", fontsize=11, color=ACCENT)
ax.set_ylabel("Cantidad de productos", fontsize=11, color=ACCENT)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("grafico_distribucion_precios.png", dpi=150)
plt.show()

# 4. Países con más productos
fig, ax = plt.subplots(figsize=(10, 5))
df["country_code"].value_counts().head(10).plot(kind="bar", ax=ax, color=BAR_COLOR, edgecolor="none")
ax.set_title("Top 10 países con más productos", fontsize=14, fontweight="bold", color=COLOR, pad=12)
ax.set_xlabel("País", fontsize=11, color=ACCENT)
ax.set_ylabel("Cantidad de productos", fontsize=11, color=ACCENT)
ax.tick_params(axis="x", rotation=45, labelsize=9)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("grafico_paises.png", dpi=150)
plt.show()

# 5. Disponibilidad por categoría (in_stock)
fig, ax = plt.subplots(figsize=(10, 5))
stock_cat = df.groupby("category")["in_stock"].value_counts(normalize=True).unstack(fill_value=0) * 100
if True in stock_cat.columns and False in stock_cat.columns:
    stock_cat = stock_cat[[True, False]]
    stock_cat.columns = ["En stock", "Sin stock"]
stock_cat.plot(kind="bar", ax=ax, color=STOCK_COLORS, edgecolor="none")
ax.set_title("Disponibilidad de stock por categoría (%)", fontsize=14, fontweight="bold", color=COLOR, pad=12)
ax.set_xlabel("Categoría", fontsize=11, color=ACCENT)
ax.set_ylabel("Porcentaje (%)", fontsize=11, color=ACCENT)
ax.tick_params(axis="x", rotation=45, labelsize=9)
ax.legend(fontsize=9)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("grafico_stock_categoria.png", dpi=150)
plt.show()

# 6. Top deportes por cantidad de productos
fig, ax = plt.subplots(figsize=(10, 5))
top_deportes = todos_los_deportes.value_counts().head(12)
top_deportes.sort_values().plot(kind="barh", ax=ax, color=BAR_COLOR, edgecolor="none")
ax.set_title("Top deportes por cantidad de productos", fontsize=14, fontweight="bold", color=COLOR, pad=12)
ax.set_xlabel("Cantidad de productos", fontsize=11, color=ACCENT)
ax.set_ylabel("Deporte / categoría", fontsize=11, color=ACCENT)
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("grafico_deportes.png", dpi=150)
plt.show()