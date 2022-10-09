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

    def generate_single_chromosome(self):
        bin = [(utils.changeOrientation(bin[0]),bin[1]) if choices([0,1],[self.protacion, 1-self.protacion])[0]==0 else bin for bin in self.init_bin_list]
        p, o = self.guillotine.cut(self.main_coordinates, bin)
        return np.array([p,o])


    def run(self, bin_list, nbest, npoblacion, protacion):
        '''
        bin_list: lista de materiales a cortar en formato [([x0,y0],'id'),....]
        nbest: numero de individuos a seleccionar como mejores
        npoblacion: numero de individuos de una poblacion
        protacion: probabilidad de rotacion en la poblacion inicial
        '''
        self.protacion = protacion
        bin_list = self.preprocess_input(bin_list)
        self.init_bin_list = bin_list
        self.data = self.pieces(bin_list)
        bin_list = self.poblacion_inicial(bin_list, protacion, npoblacion)
        poblacion = []
        orientation = []
        for entrada in bin_list:
            p,o  = self.guillotine.cut(self.main_coordinates,entrada)
            poblacion.append(p)
            orientation.append(o)
        
        #[['polish expresion','orientation'],...[]]
        poblacion = np.array(list(zip(poblacion,orientation)))
        best_aptitude = []
        i = 0
        try:
            while True:
                scores, idxs = self.seleccion(poblacion, nbest)
                best_aptitude.append((scores[0],poblacion[idxs[0]]))
                if self.condicion_parada(i):
                    break
                best_chrom = poblacion[idxs]
                new_generation = self.cruce(poblacion, len(poblacion)-len(best_chrom))
                #self.mutacion()
                new_generation = self.sustitucion(new_generation)
                new_generation.extend(best_chrom)
                poblacion = np.array(new_generation)
                if i%100==0:
                    print(10*'=', end='\n')
                    print(best_chrom[0],' ', scores[0])
                    i = 0
                i += 1
            return best_aptitude
        except KeyboardInterrupt:
            return best_aptitude

    def preprocess_input(self,bin_list):
        '''
            bin_list:[([x0,y0],'id'),....]
            return:[([0,0,x0,y0],'id'),....]
        '''
        bin_dims = [[utils.vectorToCoordinates(bin[0]),bin[1]] for bin in bin_list]
        # zip_bins = list(zip(bin_quantities,bin_dims))
        # bin_dims = []
        # for x in zip_bins:
        #     bin_dims.extend(x[0]*[x[1]])
        return bin_dims

    def condicion_parada(self, fitness):
        return fitness==2000

    def seleccion(self, poblacion, n):
        '''
        poblacion:[['polish expresion','orientation'],...[]]
        n: numero de individuos a seleccionar como optimos
        return: [bins_are/min_square,....], [best_fitness_index1,second_best_fitness_index,...]
        '''
        bins_over_min_square = np.array([self.fitness(cromosoma) for cromosoma in poblacion])
        index = np.argsort(bins_over_min_square)[:n]
        return bins_over_min_square[index], index


    def mutacion(self):
        pass

    def cruce(self, poblacion, n):
        '''
        poblacion:[['polish expresion','orientation'],...[]]
        '''
        p,h = list(zip(*poblacion))
        index = np.arange(len(p))
        new = []
        while len(new)<n:
            index1 = np.random.choice(index, size=int(np.ceil(n/2)), replace=False)
            index2 = np.random.choice(index, size=int(np.ceil(n/2)), replace=False)
            for i1,i2 in zip(index1, index2):
                p1 = np.array(p[i1].split(' '))
                p2 = np.array(p[i2].split(' '))
                #(index, value)
                p1d = self.digit_index(p1)
                #(index, value)
                p2d = self.digit_index(p2)
                min_size = min(len(p1d), len(p2d))
                rand1 = np.random.randint(0,min_size)
                rand2 = np.random.randint(rand1,min_size)
                p1d,p2d, ori1, ori2 = self.gene_cross(p1d, p2d, h[i1],h[i2], rand1,rand2)
                # p1i,p1j = p1d[rand1][0], p1d[rand2][0]    
                # p2i,p2j = p2d[rand1][0], p2d[rand2][0]
                # print(p1d, p2d)
                p1[p1d[0]]=p1d[1]
                p2[p2d[0]]=p2d[1]
                new.append(np.array([' '.join(p1), ori1]))
                new.append(np.array([' '.join(p2), ori2]))
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
    
    def gene_cross(self, array1,array2, orientation1, 
                        orientation2, min_index, max_index):
        '''
        array1: [(index, value),....], orientation1
        array2: [(index, value),....], orientation2
        '''
        idx1, val1 = map(list,zip(*array1))
        idx2, val2 = map(list,zip(*array2))
        orientation1 = [*orientation1]
        orientation2 = [*orientation2]
        for i in range(min_index,max_index):
            gen1 = val1[i]
            gen2 = val2[i]
            gen1, gen2 = self.interchage(gen1, gen2)
            ori1 = orientation1[i]
            ori2 = orientation2[i]
            orientation1[i],orientation2[i] = self.interchage(ori1,ori2)
            val1, orientation1 = self.fix_gene_cross(val1,orientation1,i,gen1)
            val2, orientation2 = self.fix_gene_cross(val2,orientation2,i,gen2)

        return (idx1,val1), (idx2,val2), ''.join(orientation1), ''.join(orientation2)
            

    def interchage(self,a,b):
        aux = a
        a = b
        b = aux
        return a, b
    
    def fix_gene_cross(self, array1, array2, pos, gen):
        '''
        array1: digits chromosome,
        array2; orientation of chromosomes
        pos: position to fix
        gen: gen to fix
        '''
        index = self.find_index(array1, gen)
        if index==-1:
            array1[pos] = gen
        else:
            aux = array1[pos]
            array1[pos] = array1[index]
            array1[index] = aux

            aux = array2[pos]
            array2[pos] = array2[index]
            array2[index] = aux
        
        return array1, array2

        
    def find_index(self, array, value):
        try:
            return array.index(value)
        except:
            return -1


    def sustitucion(self, chromosomes):
        width = self.main_coordinates[2]-self.main_coordinates[0]
        height = self.main_coordinates[3] - self.main_coordinates[1]
        for i, chromosome in enumerate(chromosomes):
            min_space, bins_area =self.stack.evaluatePostfix(self.data,chromosome)
            if min_space.width()>width or min_space.height()>height:
                chromosomes[i]= self.generate_single_chromosome()
        return chromosomes
        

    def fitness(self, cromosoma:str):
        self.stack.reset()
        min_space, bins_area =self.stack.evaluatePostfix(self.data,cromosoma)
        return (1-bins_area/min_space.area())


    def area(self, x0,y0,x1,y1):
        return abs(x1-x0)*abs(y1-y0)
            



# bin_dims = utils.generate_input(6,1,10)       

# #[width, height]
# bin_dims = [([4,1],'1'),([3,2],'2'),([4,3],'3'),([2,2],'4'),([2,1],'5'),([6,1],'6'),([4,2],'7'),([2,6],'8')]
# #material size
# print(bin_dims)
# area = [10,10]

# a = GeneticAlgorithm(bin_dims,area)
# a.run(bin_dims,2,6,0.8)

