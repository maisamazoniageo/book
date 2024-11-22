import geopandas as gpd



class Camadas:
    """O aquivo irá conter todas as camadas espaciais a serem carregadas 
    buscando padronizar as variáveis de importação e facilitando a 
    atualização dos endreços de busca.
    """

    def glebas(self):
        return gpd.read_file('../glebas-federais.gpkg', layer='glebas-mais-amazonia')
    
    def uf(self):
        return gpd.read_file('../glebas-federais.gpkg', layer='uf-brasil')