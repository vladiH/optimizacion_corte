import utils
from random import choices
class GeneticAlgorithm:
    @classmethod
    def poblacion_inicial(cls, bin_list, p, n):
        '''
        bin_list:[([0, 0, 1, 3], 'id')....]
        p:probabilidad de rotacion
        n:numero de repeticiones
        '''
        return [[(utils.changeOrientation(bin[0]),bin[1]) if choices([0,1],[p, 1-p])[0]==0 else bin for bin in bin_list] for _ in range(n)]

