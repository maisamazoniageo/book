%% 
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
