# EXTRACTING GENE EXPRESSION DATA

import GEOparse

# Downloading a GEO dataset by GEO accession ID
gse = GEOparse.get_GEO(geo="GSE53986", destdir="./")

# Extracting the gene expression matrix from the GEO dataset
gse_matrix = gse.pivot_samples('VALUE')
gse_matrix.to_csv('gene_expression_data.csv')

print(gse_matrix.head())

# NORMALIZING GENE EXPRESSION DATA

import pandas as pd
from sklearn.preprocessing import StandardScaler

# Loading gene expression data
df_gene_expr = pd.read_csv('gene_expression_data.csv')

# Separating the gene identifiers (non-numeric) from the gene expression data (numeric)
gene_ids = df_gene_expr.iloc[:, 0]  
gene_expr_data = df_gene_expr.iloc[:, 1:]  

# Checking if all remaining columns are numeric
if not pd.api.types.is_numeric_dtype(gene_expr_data):
    gene_expr_data = gene_expr_data.apply(pd.to_numeric, errors='coerce')

# Normalizing the gene expression data using z-score (only numeric data)
scaler = StandardScaler()
gene_expr_data_norm = pd.DataFrame(scaler.fit_transform(gene_expr_data), columns=gene_expr_data.columns)

# Reattaching the gene identifiers to the normalized data
df_gene_expr_norm = pd.concat([gene_ids, gene_expr_data_norm], axis=1)

# Saving the normalized data
df_gene_expr_norm.to_csv('normalized_gene_expression.csv', index=False)

# Printing the first few rows of the normalized data
print(df_gene_expr_norm.head())

# STORING DATA IN MYSQL

import pandas as pd
from sqlalchemy import create_engine

# Loading your normalized gene expression data
df_gene_expr_norm = pd.read_csv('normalized_gene_expression.csv')

# Creating a connection to the MySQL database
engine = create_engine('mysql+mysqlconnector://[user]:[password]@localhost/hospital_db')

# Loading the normalized gene expression data into the database
df_gene_expr_norm.to_sql('gene_expression_data', engine, if_exists='replace', index=False)

# Printing confirmation
print("Data loaded successfully into MySQL database.")


