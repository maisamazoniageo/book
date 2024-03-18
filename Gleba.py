# %% 
from dataclasses import dataclass
import geopandas as gpd
import pandas as pd
import polars as pl
import numpy as np
import os
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
pd.options.display.float_format = '{:.4f}'.format
pd.set_option('display.precision', 4)
#glebas = gpd.read_file('../drive/Shapes Bases de Glebas e Projetos data 01.03.23/tab_glebas_federais.shp')
#area_estudo = gpd.read_file('../drive/shapes_transformados/amazonia-legal-com-maranhao.shp')
#uf = gpd.read_file('../drive/uf.shp')
#sr_ponto = gpd.read_file("../drive/Shapes Bases de Glebas e Projetos data 01.03.23/sr_incra.shp")

# %%

# Tratar a camada SIGEF Geral

sigef_geral = gpd.read_file('../certificados_04mar2024.gpkg', layer='sigef_geral')
snci_geral = gpd.read_file('../certificados_04mar2024.gpkg', layer='snci_geral')

sigef_geral.to_file('../glebas-federais.gpkg', layer='sigef-particular')
snci_geral.to_file('../glebas-federais.gpkg', layer='snci-particular')
# %%
estados = {
    'RO': 'Rondônia', 'AC': 'Acre', 
    'AM': 'Amazonas', 'RR': 'Roraima', 
    'PA': 'Pará', 'AP': 'Amapá', 'TO': 'Tocantins', 
    'MA': 'Maranhão', 'MT': 'Mato Grosso'}
# %%

for key, value in estados.items():
    sigef_geral[sigef_geral['uf_sigla']==key].to_file('../glebas-federais.gpkg', layer=f'sigef-{value}')

for key, value in estados.items():
    snci_geral[snci_geral['uf_municip']==key].to_file('../glebas-federais.gpkg', layer=f'snci-{value}')
# %%
