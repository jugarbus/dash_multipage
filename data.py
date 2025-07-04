import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
# Cargar datos
df_raw = pd.read_csv("./data/Arritmias.csv")

# Seleccionar columnas numéricas
cols = df_raw.columns[1:-4]
df = df_raw.copy(deep=True)

# Convertir datos numéricos
for i in range(len(cols)):
    df[cols[i]] = df[cols[i]].astype(str).str.replace(",", ".").astype(float)

# Copia del DataFrame
df_copy = df.copy(deep=True)

# Reemplazo de valores en SEXO y AV
df_copy["SEXO"] = df_copy["SEXO"].replace({1: "Hombre", 2: "Mujer"})
df_copy["AV"] = df_copy["AV"].replace({0: "No arritmia", 1: "Arritmia"})

# Selección de variables numéricas
df_num = df_copy.drop(columns=['PACIENTES', 'BZ + CORE (%)', 'BZ (%)', 'CORE (%)', 'AV', 'SEXO', "BZ + CORE (g)"], errors='ignore')
df_num_2 = df_copy.drop(columns=['PACIENTES', 'AV', 'SEXO'], errors='ignore')


# Separar los datos en dos grupos según el valor de AV
grupo_sin_arritmia = df_num_2[df['AV'] == 0]
grupo_con_arritmia = df_num_2[df['AV'] == 1]


# Función para aplicar reducción de dimensionalidad
def apply_dimensionality_reduction(method):
    if method == "t-SNE":
        reducer = TSNE(n_components=2, perplexity=10, verbose=0, random_state=42)
    elif method == "PCA":
        reducer = PCA(n_components=2)
    else:
        return None
    return reducer.fit_transform(df_num)