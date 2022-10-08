from guillotine_algorithm import GuillotineAlgorithm
from area import Stack
import utils
import numpy as np
from random import choices, shuffle
class GeneticAlgorithm:
    def __init__(self,pieces, vector):
        '''
        vector = [x0,y0]
        '''
        self.main_coordinates = utils.vectorToCoordinates(vector)
        self.main_area = self.area(*self.main_coordinates)
        self.stack = Stack()
        self.guillotine = GuillotineAlgorithm()

    def pieces(self, pieces):
        '''
        return {id:[0,0,x1,x2]}
        '''
        data = {}
        for p in pieces:
            if p[1] not in data:
                data[p[1]] = p[0]
        return data

    @classmethod
    def poblacion_inicial(cls, bin_list, p, n):
        '''
        Genera n poblaciones tomando en cuenta la entrada bin list
            bin_list:[([0, 0, 1, 3], 'id')....]
            p:probabilidad de rotar cada item de bin_list
            n: cantidad de individuos en una poblacion
            return [[([0,0,1,3],'id'),[]],....,[]]
        '''
        data =  [ ]
        for _ in range(n):
            shuffle(bin_list)
            data.append([(utils.changeOrientation(bin[0]),bin[1]) if choices([0,1],[p, 1-p])[0]==0 else bin for bin in bin_list])
        return data


    def run(self, bin_list,bin_quantities, nbest, npoblacion, protacion):
        '''
        bin_list: lista de materiales a cortar en formato [([x0,y0],'id'),....]
        bin_quantities: cantidad de piezas por material a cortar [3,....]
        nbest: numero de individuos a seleccionar como mejores
        npoblacion: numero de individuos de una poblacion
        protacion: probabilidad de rotacion en la poblacion inicial
        '''
        bin_list = self.preprocess_input(bin_list,bin_quantities)
        # print(bin_list)
        self.data = self.pieces(bin_list)
        bin_list = self.poblacion_inicial(bin_list, protacion, npoblacion)
        # print(bin_list)
        # bin_list=[[([0, 0, 2, 6], '8'), ([0, 0, 2, 2], '4'), ([0, 0, 4, 2], '7'), ([0, 0, 4, 3], '3'), ([0, 0, 6, 1], '6'), ([0, 0, 4, 1], '1'), ([0, 0, 3, 2], '2'), ([0, 0, 2, 1], '5')]]
        # print(self.main_coordinates)
        poblacion = []
        horientation = []
        for entrada in bin_list:
            p,o  = self.guillotine.cut(self.main_coordinates,entrada)
            poblacion.append(p)
            horientation.append(o)
        poblacion = np.array(poblacion)
        print(poblacion)
        
        fitness = []
        while True:
            f, index_mejor_individuo = self.seleccion(poblacion, nbest)
            fitness.append((f[0],poblacion[index_mejor_individuo[0]]))
            mejores_individuos = poblacion[index_mejor_individuo]
            new = self.cruce(poblacion, len(poblacion)-len(mejores_individuos))
            new.extend(mejores_individuos)
            poblacion = np.array(new)
            self.mutacion()
            self.sustitucion()
            print(f)
            print(poblacion[index_mejor_individuo])

    def preprocess_input(self,bin_list, bin_quantities):
        '''
        Repite cada elemento de bin_list segun bin_quantities
            bin_list:[([x0,y0],'id'),....]
            bin_quantities:[n,...]
            return:[([0,0,x0,y0],'id'),....]
        '''
        bin_dims = [(utils.vectorToCoordinates(bin[0]),bin[1]) for bin in bin_list]
        zip_bins = list(zip(bin_quantities,bin_dims))
        bin_dims = []
        for x in zip_bins:
            bin_dims.extend(x[0]*[x[1]])
        
        return bin_dims

    def condicion_parada(self,cromosoma:str):
        return False

    def seleccion(self, poblacion, n):
        '''
        n: numero de individuos a seleccionar
        return: 
        '''
        s = np.array([self.fitness(cromosoma) for cromosoma in poblacion])
        index = np.argsort(s)[:n]
        return s[index], index


    def mutacion(self):
        pass

    def cruce(self, poblacion, n):
        new = []
        while len(new)<n:
            parents1 = np.random.choice(poblacion, size=int(np.ceil(n/2)), replace=False)
            parents2 = np.random.choice(poblacion, size=int(np.ceil(n/2)), replace=False)
            for parents in list(zip(parents1, parents2)):
                p1 = np.array(parents[0].split(' '))
                p2 = np.array(parents[1].split(' '))
                #(index, value)
                p1d = self.digit_index(p1)
                #(index, value)
                p2d = self.digit_index(p2)
                min_size = min(len(p1d), len(p2d))
                rand1 = np.random.randint(0,min_size)
                rand2 = np.random.randint(rand1,min_size)
                p1d,p2d = self.cross_gene(p1d, p2d, rand1,rand2)
                # p1i,p1j = p1d[rand1][0], p1d[rand2][0]    
                # p2i,p2j = p2d[rand1][0], p2d[rand2][0]
                # print(p1d, p2d)
                p1[list(p1d[0])]=list(p1d[1])
                p2[list(p2d[0])]=list(p2d[1])
                new.append(' '.join(p1))
                new.append(' '.join(p2))
        return new

    def digit_index(self, array):
        '''
        return: [(index, value),...]
        '''
        digits = []
        for i,val in enumerate(array):
            if val.isdigit():
                digits.append((i,val))
        return digits
    
    def operator_index(self, array):
        '''
        return: [(index, value),...]
        '''
        operators = []
        for i,val in enumerate(array):
            if not val.isdigit():
                operators.append((i,val))
        return operators
    
    def cross_gene(self, array1,array2, min_index, max_index):
        '''
        array1: [(index, value),....]
        array2: [(index, value),....]
        '''
        array1 = list(zip(*array1))
        array2 = list(zip(*array2))
        for i in range(min_index,max_index):
            a = array1[1][i]
            b = array2[1][i]
            array2[1]= self.interchage(list(array2[1]),i,a)
            array1[1]= self.interchage(list(array1[1]),i,b)
        return (array1[0],array1[1]), (array2[0],array2[1])
            

    def interchage(self,array,i, value):
        r = self.find_index(array,value)
        if r!=-1:
            aux = array[i]
            array[i]=array[r]
            array[r] = aux
        else:
            array[i] = value
        return tuple(array)
        
    def find_index(self, array, value):
        try:
            return array.index(value)
        except:
            return -1


    def sustitucion(self):
        pass

    def fitness(self, cromosoma:str):
        # area = 0
        # for gen in cromosoma.split(' '):
        #     if gen.isdigit():
        #         if gen in self.data:
        #             area += self.area(*self.data[gen])
        # return min(100000, self.main_area - area)
        self.stack.reset()
        # area, width, height =self.stack.evaluatePostfix(self.data,cromosoma)
        # if self.main_coordinates[2]-self.main_coordinates[0]<width or self.main_coordinates[3]-self.main_coordinates[1]<height:
        #     return 10000
        # else:
        #     #print(area)

        min_square, bins_area =self.stack.evaluatePostfix(self.data,cromosoma)
        p = self.stack.binsPositions(self.data,cromosoma)
        print(p)
        return (1-bins_area/min_square)


    def area(self, x0,y0,x1,y1):
        return abs(x1-x0)*abs(y1-y0)
            



        

#quantity for each bin defined in bin_dims
bin_quantities = [1,1,1,1,1,1,1,1]
#[width, height]
bin_dims = [([4,1],'1'),([3,2],'2'),([4,3],'3'),([2,2],'4'),([2,1],'5'),([6,1],'6'),([4,2],'7'),([2,6],'8')]
#material size
area = [10,10]

a = GeneticAlgorithm(bin_dims,area)
a.run(bin_dims,bin_quantities,2,1,0.)