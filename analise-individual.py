# Análise de Sobreposição individual das Glebas Federais do estado do Acre.

# %%
import geopandas as gpd
import pandas as pd
import locale
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from IPython.display import display, Markdown
pd.options.display.float_format = '{:.4f}'.format
pd.set_option('display.precision', 4)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
import warnings
warnings.filterwarnings('ignore')
glebas = gpd.read_file('../glebas-federais.gpkg', layer='glebas-mais-amazonia')
area_estudo = gpd.read_file('../glebas-federais.gpkg', layer='area-estudo')
uf = gpd.read_file('../glebas-federais.gpkg', layer='uf-brasil')
sr_ponto = gpd.read_file('../glebas-federais.gpkg', layer='sr_incra')
mun = gpd.read_file('../glebas-federais.gpkg', layer='municipios-area-estudo')

uf_analise = 'Acre'

# Definição de cores
cor_gleba = '#e9cf68'
cor_SIGEF = '#e0bd1f'
cor_PA = '#998115'
cor_TI = '#f2d4d3'
cor_TQ = '#d7c0dd'
cor_UC = '#99eb65'
cor_Floresta = '#a7f5e0'
cor_massa_agua = '#0751ff'
cor_rodovias = '#e10c00'
cor_gleba_flo = '#D9E3A9'
cor_gleba_uc = '#C1DC66'
cor_gleba_ti = '#EFD9A5'
cor_gleba_pa = '#C1A83E'
cor_gleba_tq = '#CDAFD4'
cor_gleba_sigef = '#E4C643'



# %%
glebas = glebas[glebas['uf_nome']==uf_analise]
# listagem das glebas do estado analisado por ordem alfabética.
lista = glebas[['gid', 'nome_gleba']].sort_values('nome_gleba')['gid'].to_list()

# %%
for item in lista:
    gleba = glebas[glebas['gid']==item]
    display(Markdown(f'## Gleba Analisada: {gleba.nome_gleba}'))
    gleba = gleba.rename(columns={'nome_gleba':'Nome da Gleba',
    'area_ha':'Área (ha)'})
    #display(gleba[['Nome da Gleba','Área (ha)']].to_html(index=False))

    #display(Markdown('### Abrangência Municipal'))
    #fig, ax = plt.subplots(figsize=(13,6))

    municipio_gleba = mun.sjoin(gleba, how='inner')
    # municipio_gleba.plot(ax=ax, column='nm_mun', categorical=True,
    #                     legend=True,
    #                     alpha=0.65, cmap='Pastel2',
    #                     legend_kwds={'loc': 'upper center',
    #                     'bbox_to_anchor':(0.5,-0.15),'ncols':3})
    # gleba.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=2)
    # plt.xlabel('Longitude (°)')
    # plt.ylabel('Latitude (°)')
    # plt.grid()
    # plt.show()
    municipio_gleba = municipio_gleba.rename(columns={'cd_uf':'Código da UF',
    'nm_uf':'Estado', 'sigla':'UF', 'cd_mun':'Código do Município',
    'nm_mun':'Nome do Município'})
    # display(municipio_gleba[['Código da UF', 'Estado', 'UF', 
    # 'Código do Município', 'Nome do Município']].to_html(index=False))

    # display(Markdown('### Unidades de Conservação'))
    uc=gpd.read_file('../glebas-federais.gpkg', layer='uc', mask=gleba)
    uc_gleba = uc.overlay(gleba, how='intersection')
    if uc_gleba.shape[0]>0:
        # fig_uc, ax_uc = plt.subplots(figsize=(13,6))
        # uc_gleba.plot(ax=ax_uc, column='nome_uc1', categorical=True,
        #                 legend=True,
        #                 alpha=0.65, cmap='Pastel2',
        #                 legend_kwds={'loc': 'upper center',
        #                 'bbox_to_anchor':(0.5,-0.15),'ncols':3})
        # gleba.plot(ax=ax_uc, facecolor='none', edgecolor='black', linewidth=2)
        # plt.xlabel('Longitude (°)')
        # plt.ylabel('Latitude (°)')
        # plt.grid()
        # plt.show()
        uc_gleba['Área Sobreposta (ha)'] = (uc_gleba.to_crs(5880).area)/10000
        uc_gleba = uc_gleba.rename(columns={'nome_uc1':'Nome',
        'categori3':'Categoria','esfera5':'Responsabilidade'})
        display(uc_gleba[['Nome','Categoria','Responsabilidade',
        'Área Sobreposta (ha)']].to_html(index=False))
    else:
        display(Markdown('Não há sobreposição'))

    display(Markdown('### Terra Indígenas'))
    ti=gpd.read_file('../glebas-federais.gpkg', layer='ti-portarias',
                    mask=gleba)
    ti = ti.set_crs(4674, allow_override=True)
    ti_gleba = ti.overlay(gleba, how='intersection')
    if ti_gleba.shape[0]>0:
        fig_ti, ax_ti = plt.subplots(figsize=(13,6))
        ti_gleba.plot(ax=ax_ti, column='terrai_nom', categorical=True,
                        legend=True,
                        alpha=0.65, cmap='Pastel2',
                        legend_kwds={'loc': 'upper center',
                        'bbox_to_anchor':(0.5,-0.15),'ncols':3})
        gleba.plot(ax=ax_ti, facecolor='none', edgecolor='black', linewidth=2)
        plt.xlabel('Longitude (°)')
        plt.ylabel('Latitude (°)')
        plt.grid()
        plt.show()
        ti_gleba['Área Sobreposta (ha)'] = (ti_gleba.to_crs(5880).area)/10000
        ti_gleba = ti_gleba.rename(columns={'terrai_nom':'Nome',
                                        'fase_ti':'Fase de Regularização'})
        display(ti_gleba[['Nome', 'Fase de Regularização',
                        'Área Sobreposta (ha)']].to_html(index=False))
    else:
        display(Markdown('Não há sobreposição'))

    display(Markdown('### Projetos de Assentamento'))
    pa = gpd.read_file('../glebas-federais.gpkg', layer='pa_brasil',
                        mask=gleba)
    pa_gleba = pa.overlay(gleba, how='intersection')
    if pa_gleba.shape[0] > 0:
        fig_pa, ax_pa = plt.subplots(figsize=(13,6))
        pa_gleba.plot(ax=ax_pa, column='nome_proje', categorical=True,
                        legend=True,
                        alpha=0.65, cmap='Pastel2',
                        legend_kwds={'loc': 'upper center',
                        'bbox_to_anchor':(0.5,-0.15),'ncols':3})
        gleba.plot(ax=ax_pa, facecolor='none', edgecolor='black', linewidth=2)
        plt.xlabel('Longitude (°)')
        plt.ylabel('Latitude (°)')
        plt.grid()
        plt.show()
        pa_gleba['Área Sobreposta (ha)'] = (pa_gleba.to_crs(5880).area)/10000
        pa_gleba = pa_gleba.rename(columns={'cd_sipra':'SIPRA',
                                'nome_proje':'Nome','municipio':'Município'})
        display(pa_gleba[['SIPRA','Nome','Município',
                'Área Sobreposta (ha)']].to_html(index=False))
    else:
        display(Markdown('Não há sobreposição'))

    display(Markdown('### Território Quilombola'))
    tq = gpd.read_file('../glebas-federais.gpkg',
                        layer='tq_brasil', mask=gleba)
    tq_gleba = tq.overlay(gleba, how='intersection')
    if tq_gleba.shape[0] >0:
        fig_tq, ax_tq = plt.subplots(figsize=(13,6))
        tq_gleba.plot(ax=ax_tq, column='nm_comunid', categorical=True,
                        legend=True, alpha=0.65, cmap='Pastel2',
                        legend_kwds={'loc': 'upper center',
                        'bbox_to_anchor':(0.5,-0.15),'ncols':3})
        gleba.plot(ax=ax_tq, facecolor='none', edgecolor='black', linewidth=2)
        plt.xlabel('Longitude (°)')
        plt.ylabel('Latitude (°)')
        plt.grid()
        plt.show()
        tq_gleba['Área Sobreposta (ha)'] = (tq_gleba.to_crs(5880).area)/10000
        tq_gleba = tq_gleba.rename(columns={'nm_comunid':'Nome',
                'esfera':'Responsabilidade', 'fase':'Fase da Regularização'})
        display(tq_gleba[['Nome', 'Responsabilidade', 'Fase da Regularização',
                    'Área Sobreposta (ha)']].to_html(index=False))
    else:
        display(Markdown('Não há sobreposição'))

    display(Markdown('### SIGEF'))
    sigef = gpd.read_file('../glebas-federais.gpkg', layer='sigef-particular',
                        mask=gleba)
    sigef_gleba = sigef.overlay(gleba, how='intersection')
    if sigef_gleba.shape[0] > 0:
        fig_sigef, ax_sigef = plt.subplots(figsize=(13,6))
        sigef_gleba.plot(ax=ax_sigef, facecolor=cor_SIGEF)
        gleba.plot(ax=ax_sigef, facecolor='none', edgecolor='black',
                    linewidth=1)
        # LEGENDAS
        patch_list = []
        patch_list.append(patches.Patch(facecolor='none', edgecolor='black',
                        label='Gleba Federal', linewidth=1))
        patch_list.append(patches.Patch(facecolor=cor_SIGEF, alpha=0.6, 
                            edgecolor='none', label='SIGEF', linewidth=1))
        # Creates a legend with the list of patches above.
        ax_sigef.legend(handles=patch_list, fontsize=10, loc='upper center',
                bbox_to_anchor = (0.5 , -0.15), ncols=3,title='Legenda', title_fontsize=12)
        plt.xlabel('Longitude (°)')
        plt.ylabel('Latitude (°)')
        plt.grid()
        plt.show()
        sigef_gleba['Área Sobreposta (ha)'] = (sigef_gleba.to_crs(5880).area)/10000
        sigef_gleba = sigef_gleba.rename(columns={'parcela_co':'Código SIGEF','natureza':'Natureza do Polígono'})
        display(sigef_gleba[['Código SIGEF','Natureza do Polígono', 'Área Sobreposta (ha)']].to_html(index=False))
    else:
        display(Markdown('Não há sobreposição'))
    
    display(Markdown('### SNCI'))
    snci = gpd.read_file('../glebas-federais.gpkg', layer='snci-particular',
                        mask=gleba)
    snci_gleba = snci.overlay(gleba, how='intersection')
    if snci_gleba.shape[0] > 0:
        fig_snci, ax_snci = plt.subplots(figsize=(13,6))
        snci_gleba.plot(ax=ax_snci, facecolor=cor_SIGEF)
        gleba.plot(ax=ax_snci, facecolor='none', edgecolor='black',
                    linewidth=1)
        # LEGENDAS
        patch_list = []
        patch_list.append(patches.Patch(facecolor='none', edgecolor='black',
                        label='Gleba Federal', linewidth=1))
        patch_list.append(patches.Patch(facecolor=cor_SIGEF, alpha=0.6, 
                            edgecolor='none', label='SNCI', linewidth=1))
        # Creates a legend with the list of patches above.
        ax_sigef.legend(handles=patch_list, fontsize=10, loc='upper center',
                bbox_to_anchor = (0.5 , -0.15), ncols=3,title='Legenda', title_fontsize=12)
        plt.xlabel('Longitude (°)')
        plt.ylabel('Latitude (°)')
        plt.grid()
        plt.show()
        snci_gleba['Área Sobreposta (ha)'] = (snci_gleba.to_crs(5880).area)/10000
        snci_gleba = snci_gleba.rename(columns={'num_certif_1':'Código SNCI'})
        display(snci_gleba[['Código SNCI', 'Área Sobreposta (ha)']].to_html(index=False))
    else:
        display(Markdown('Não há sobreposição'))
    break

