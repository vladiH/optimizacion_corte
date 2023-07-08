import numpy as np
import utils
import time
from guillotine_algorithm import GuillotineAlgorithm
from area import Stack
from random import choices, shuffle

class EnfriamientoSimulado:
    def __init__(self,vector, 
                prorientation=0.3, 
                pcoperator=0.3, 
                pcnoperator=0.1,
                pexchanging=0.3):
        '''
        vector = [x0,y0]
        prorientation: probability to rotate orientation
        pcoperator: probability of changing an operator
        pcnoperator: probability of changing a nested operator
        pexchanging : probability of exchanging two numbers
        '''
        self.main_coordinates = utils.vectorToCoordinates(vector)
        self.prorientation = prorientation
        self.pcoperator = pcoperator
        self.pcnoperator = pcnoperator
        self.pexchanging = pexchanging

        self.stack = Stack()
        self.guillotine = GuillotineAlgorithm()

    def run(self, bin_list, p, n, stop, k=0.01, t=20000):
        '''
        t: temperatura inicial
        p: probabilidad de rotar en la exploracion inicial
        n: numero de indivudos en la exploracion inicial
        stop: stop number, iteration to do for getting result
        '''
        start_time = time.time()
        best_aptitude = []
        #s_actual:[polish expression, orientation]
        s_actual, aptitud_actual = self.initialChromosome(bin_list, p, n)
        s_mejor, aptitud_mejor = s_actual, aptitud_actual
        t = t
        i = 0
        try:
            while i<stop:
                best_aptitude.append((s_actual, aptitud_actual*100, time.time()-start_time))
                s_nuevo, aptitud_nuevo = self.newNeighbors(s_actual)
                diff = aptitud_nuevo - aptitud_actual
                if diff < 0:
                    s_actual = s_nuevo
                    aptitud_actual = aptitud_nuevo
                    if aptitud_nuevo < aptitud_mejor:
                        s_mejor = s_nuevo
                        aptitud_mejor = aptitud_nuevo
                else:
                    if np.random.rand()<self.probabilidad(-(diff), t):
                        s_actual = s_nuevo
                        aptitud_actual = aptitud_nuevo
                i +=1
                t = self.actualizarTemperatura(t, k)
                if i%100==0:
                    print(20*'=', end='\n')
                    print(s_actual,' ', aptitud_actual)
            return best_aptitude, s_mejor, aptitud_mejor*100
        except KeyboardInterrupt:
            return best_aptitude, s_mejor, aptitud_mejor*100

    def scouting(self, bin_list, p, n):
        '''
        Genera n individuos a partir de bin list
            bin_list:[([0, 0, 1, 3], 'id')....]
            p:probabilidad de rotar cada item de bin_list
            n: total de muestras a generar
            return [[([0,0,1,3],'id'),[]],....,[]]
        '''
        data =  [ ]
        for _ in range(n):
            shuffle(bin_list)
            data.append([(utils.changeOrientation(bin[0]),bin[1]) if choices([0,1],[p, 1-p])[0]==0 else bin for bin in bin_list])
        return data
    

    def preprocessInput(self,bin_list):
        '''
            bin_list:[([x0,y0],'id'),....]
            return:[([0,0,x0,y0],'id'),....]
        '''
        bin_dims = [[utils.vectorToCoordinates(bin[0]),bin[1]] for bin in bin_list]
        return bin_dims
    
    def inputDictionary(self, pieces):
        '''
        return {id:[0,0,x1,x2]}
        '''
        self.input_dictionary = {}
        for p in pieces:
            if p[1] not in self.input_dictionary:
                self.input_dictionary[p[1]] = p[0]

    def initialChromosome(self, bin_list, p, n):
        bin_list = self.preprocessInput(bin_list)
        self.inputDictionary(bin_list)
        bin_list = self.scouting(bin_list, p, n)
        chromosomes = self.cutting(bin_list)
        return self.bestChromosome(chromosomes)

    def bestChromosome(self, chromosomes):
        '''
        chromosomes:[['polish expression','orientation'],...[]]
        n: numero de individuos a seleccionar como optimos
        return: best chromosome, aptitude
        '''
        aptitudes = np.array([self.aptitude(chromosome) for chromosome in chromosomes])
        index = np.argsort(aptitudes)
        return chromosomes[index[0]], aptitudes[index[0]]

    def aptitude(self, cromosoma:str):
        self.stack.reset()
        min_space, bins_area =self.stack.evaluatePostfix(self.input_dictionary, cromosoma)
        return 1 - bins_area/min_space.area()

    def cutting(self, bin_list):
        polish_expression = []
        orientation = []
        for entrada in bin_list:
            p,o  = self.guillotine.cut(self.main_coordinates,entrada)
            polish_expression.append(p)
            orientation.append(o)
        #[['polish expresion','orientation'],...[]]
        return np.array(list(zip(polish_expression,orientation)))

    def newNeighbors(self, chromosome):
        current_chrom, current_orien = chromosome
        array = np.array(current_chrom.split(' '))
        digit_index = self.digitIndex(array)
        operator_index = self.operatorIndex(array)
        neighbors = []
        while len(neighbors)==0:
            for i in range(len(digit_index)):
                chro = array
                new_oidx = self.exchanging(digit_index, i)
                if new_oidx == None:
                    continue
                idx, value = list(zip(*new_oidx))
                chro[[idx]] = value
                chro = list(chro)
                neighbors.append(np.array([' '.join(chro), current_orien]))

            for i in range(len(operator_index)):
                chro = array
                new_oidx = self.operatorMutation(operator_index, i)
                if new_oidx == None:
                    continue
                idx, value = list(zip(*new_oidx))
                chro[[idx]] = value
                chro = list(chro)
                neighbors.append(np.array([' '.join(chro), current_orien]))
            
            for i in range(len(current_orien)):
                orientation = self.orientationMutation(current_orien, i)
                if orientation == None:
                    continue
                neighbors.append(np.array([current_chrom, orientation]))
            
            neighbors = self.filterNeighbors(neighbors)
        return neighbors
    
    def filterNeighbors(self, chromosomes):
        width = self.main_coordinates[2]-self.main_coordinates[0]
        height = self.main_coordinates[3] - self.main_coordinates[1]
        valid_chromosomes = []
        fitness = []
        for i, chromosome in enumerate(chromosomes):
            self.stack.reset()
            min_space, bins_area =self.stack.evaluatePostfix(self.input_dictionary, chromosome)
            if min_space.width()>width or min_space.height()>height:
                continue
            valid_chromosomes.append(chromosome)
            fitness.append(bins_area/min_space.area())
        if len(fitness) == 0:
            return []
        fitness = np.array(fitness)
        index = np.argsort(fitness)[::-1]
        return valid_chromosomes[index[0]], 1- fitness[index[0]]
    
    def exchanging(self, digit_index, index):
        if index == len(digit_index)-1:
            return None
        exchange = np.random.choice(2, 1, replace=False, p=[1-self.pexchanging, self.pexchanging])
        if exchange == 0:
            return None
            
        idx1 = np.random.choice(np.arange(index,len(digit_index)), 1, replace=False)[0]
        aux = digit_index[index][1]
        digit_index[index][1] = digit_index[idx1][1]
        digit_index[idx1][1] = aux
        return digit_index


    def operatorMutation(self, operator_index, index):
        length = len(operator_index)
        prev = -1
        pos = int(operator_index[index][0])
        next = -1
        if index - 1>=0:
            prev = int(operator_index[index-1][0])
        if index + 1<length:
            next = int(operator_index[index+1][0])
        
        if (pos-1 == prev and pos + 1 == next) or (pos-1 != prev and pos + 1 != next):
            rotate = np.random.choice(2, 1, replace=False, p=[1-self.pcnoperator, self.pcnoperator])
            if rotate == 0:
               return None
        else:
            rotate = np.random.choice(2, 1, replace=False, p=[1-self.pcoperator, self.pcoperator])
            if rotate == 0:
               return None
        if operator_index[index][1] == 'H':
            operator_index[index][1] = 'V'
        else:
            operator_index[index][1] = 'H'
        return operator_index
    
    def orientationMutation(self, orientation, index):
        orientation = [*orientation]
        rotate = np.random.choice(2, 1, replace=False, p=[1-self.prorientation, self.prorientation])
        if rotate == 0:
            return None
        if orientation[index] == 'H':
            orientation[index] = 'V'
        else:
            orientation[index] = 'H'
        return ''.join(orientation)
    
    def interchange(self,a,b):
        aux = a
        a = b
        b = aux
        return a, b

    def digitIndex(self, array):
        '''
        return: [(index, value),...]
        '''
        chars = []
        for i,val in enumerate(array):
            if val.isdigit():
                chars.append([i,val])
        return chars
    
    def operatorIndex(self, array):
        '''
        return: [(index, value),...]
        '''
        operators = []
        for i,val in enumerate(array):
            if not val.isdigit():
                operators.append([i,val])
        return operators

    def probabilidad(self, diff, t):
        return np.exp(diff/t)

    
    def actualizarTemperatura(self, t,k):
        return t/(1 + k*t)



# bin_dims = [([4,1],'1'),([3,2],'2'),([4,3],'3'),([2,2],'4'),([2,1],'5'),([6,1],'6'),([4,2],'7'),([2,6],'8')]
# #material size
# print(bin_dims)
# area = [10,10]

# prorientation = 0.3
# pcoperator = 0.3
# pcnoperator = 0.1
# pexchanging = 0.3
# a = EnfriamientoSimulado(area,
#                         prorientation,
#                         pcoperator,
#                         pcnoperator,
#                         pexchanging)
# r = a.run(bin_dims,0.7, 20)
# print(r[0])
# print(r[len(r)-1])