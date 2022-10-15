import numpy as np
import utils
from guillotine_algorithm import GuillotineAlgorithm
from area import Stack
from random import choices, random, shuffle

class AlgoritmoGenetico:
    def __init__(self,vector, pcross=0.5, prorientation=0.3, pcoperator=0.3, pcnoperator=0.1, pexchanging=0.3):
        '''
        vector = [x0,y0]
        prorientation: probability to rotate orientation
        pcoperator: probability of changing an operator
        pcnoperator: probability of changing a nested operator
        pexchanging : probability of exchanging two numbers
        pcross: probability de que exista cruce
        '''
        self.main_coordinates = utils.vectorToCoordinates(vector)
        self.prorientation = prorientation
        self.pcoperator = pcoperator
        self.pcnoperator = pcnoperator
        self.pexchanging = pexchanging
        self.pcross = pcross

        self.stack = Stack()
        self.guillotine = GuillotineAlgorithm()
    
    def firstGeneration(self, bin_list, p, n):
        bin_list = self.preprocessInput(bin_list)
        self.initial_bins = bin_list
        self.inputDictionary(bin_list)
        bin_list = self.scouting(bin_list, p, n)
        return self.cutting(bin_list)
    
    def cutting(self, bin_list):
        polish_expression = []
        orientation = []
        for entrada in bin_list:
            p,o  = self.guillotine.cut(self.main_coordinates,entrada)
            polish_expression.append(p)
            orientation.append(o)
        #[['polish expresion','orientation'],...[]]
        return np.array(list(zip(polish_expression,orientation)))

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
    
    def selection(self, chromosomes, n):
        '''
        chromosomes:[['polish expression','orientation'],...[]]
        n: numero de individuos a seleccionar como optimos
        return: best_chrom, best_chrom_aptitude, chromosomes sorted asc
        '''
        aptitudes = np.array([self.aptitude(chromosome) for chromosome in chromosomes])
        index = np.argsort(aptitudes)
        return chromosomes[index[:n]], aptitudes[index[:n]], chromosomes[index], aptitudes[index]

    def aptitude(self, cromosoma:str):
        self.stack.reset()
        min_space, bins_area =self.stack.evaluatePostfix(self.input_dictionary, cromosoma)
        return 1 - bins_area/min_space.area()
        
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
    
    def geneCrossFix(self, array1, array2, pos, gen):
        '''
        array1: digits chromosome,
        array2; orientation of chromosomes
        pos: position to fix
        gen: gen to fix
        '''
        index = self.findIndex(array1, gen)
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

        
    def findIndex(self, array, value):
        try:
            return array.index(value)
        except:
            return -1

    def interchage(self,a,b):
        aux = a
        a = b
        b = aux
        return a, b

    def geneCross(self, array1,array2, orientation1, 
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
            val1, orientation1 = self.geneCrossFix(val1,orientation1,i,gen1)
            val2, orientation2 = self.geneCrossFix(val2,orientation2,i,gen2)
        return (idx1,val1), (idx2,val2), ''.join(orientation1), ''.join(orientation2)

    def crossing(self, poblacion, aptitudes, n):
        '''
        poblacion:[['polish expresion','orientation'],...[]]
        aptitudes: aptitudes de cada cromosoma(mejor a peor entre 0 y 1)
        n: indica el numero de cromosomas que se consideran como optimo
        '''
        p,h = list(zip(*poblacion))
        aptitudes = 1- aptitudes
        aptitudes = aptitudes/(np.sum(aptitudes)+0.0000001)
        index = np.arange(len(p))
        new = []
        index1 = np.random.choice(index, size=int(np.ceil(len(p)/2)), replace=True, p=aptitudes)
        index2 = np.random.choice(index, size=int(np.ceil(len(p)/2)), replace=False, p=aptitudes)
        for i1,i2 in zip(index1, index2):
            cross = np.random.choice(2, 1, replace=False, p=[1-self.pcross, self.pcross])
            if cross == 0:
                new.append(np.array([p[i1], h[i1]]))
                new.append(np.array([p[i1], h[i1]]))
            else:
                p1 = np.array(p[i1].split(' '))
                p2 = np.array(p[i2].split(' '))
                p1d = self.digitIndex(p1)
                p2d = self.digitIndex(p2)
                min_size = min(len(p1d), len(p2d))
                rand1,rand2 = np.random.choice(min_size, 2, replace=False)
                init = min(rand1, rand2)
                end = max(rand1, rand2)
                p1d,p2d, ori1, ori2 = self.geneCross(p1d, p2d, h[i1],h[i2], init,end)
                p1[p1d[0]]=p1d[1]
                p2[p2d[0]]=p2d[1]
                new.append(np.array([' '.join(p1), ori1]))
                new.append(np.array([' '.join(p2), ori2]))
        return new[:n]

    def mutation(self, chromosomes):
        '''
        chromosomes:[['polish expresion','orientation'],...[]]
        '''
        for i,chromosome in enumerate(chromosomes):
            current_chrom, current_orien = chromosome
            array = np.array(current_chrom.split(' '))
            digit_index = self.digitIndex(array)
            operator_index = self.operatorIndex(array)
            result,  type = self.mutate(digit_index, operator_index, current_orien)
            if result == None:
                continue
            if type == 'orientation':
                chromosomes[i] = np.array([current_chrom, result])
            elif type == 'digit' or 'operator':
                idx, value = list(zip(*result))
                array[[idx]] = value
                array = list(array)
                chromosomes[i] = np.array([' '.join(array), current_orien])
        return chromosomes

    def mutate(self, digit_index, operator_index, orientation):
        type = choices(['operator', 'orientation', 'digit'], k=1)[0]
        if type == 'orientation':
            i = np.random.choice(len(orientation),1)[0]
            return self.orientationMutation(orientation,i), type
        if type == 'digit':
            i,j = np.random.choice(len(digit_index),2, replace=False)
            return self.exchanging(digit_index, i, j), type
        if type == 'operator':
            i = np.random.choice(len(operator_index),1)[0]
            return self.operatorMutation(operator_index, i), type
    
    def exchanging(self, digit_index, i, j):
        if i==j:
            return digit_index
        exchange = np.random.choice(2, 1, replace=False, p=[1-self.pexchanging, self.pexchanging])
        if exchange == 0:
            return None
        aux = digit_index[i][1]
        digit_index[i][1] = digit_index[j][1]
        digit_index[j][1] = aux
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

    def generateSingleChromosome(self, protacion):
        bin = [(utils.changeOrientation(bin[0]),bin[1]) if choices([0,1],[protacion, 1-protacion])[0]==0 else bin for bin in self.initial_bins]
        p, o = self.guillotine.cut(self.main_coordinates, bin)
        return np.array([p,o])

    def substitution(self, chromosomes, protacion):
        width = self.main_coordinates[2]-self.main_coordinates[0]
        height = self.main_coordinates[3] - self.main_coordinates[1]
        for i, chromosome in enumerate(chromosomes):
            self.stack.reset()
            min_space, bins_area =self.stack.evaluatePostfix(self.input_dictionary,chromosome)
            if min_space.width()>width or min_space.height()>height:
                chromosomes[i]= self.generateSingleChromosome(protacion)
        return chromosomes

    def run(self, bin_list, nbest, npoblacion, protacion, stop):
        '''
        bin_list: lista de materiales a cortar en formato [([x0,y0],'id'),....]
        nbest: numero de individuos a seleccionar como mejores
        npoblacion: numero de individuos por generacion
        protacion: probabilidad de rotacion en la generacion de cromosomas
         stop: indica el numero de iteracion donde detenerse
        '''
        best_aptitude = []
        chromosomes = self.firstGeneration(bin_list, protacion, npoblacion)
        i = 0
        try:
            while i<stop:
                best_chrom, best_chrom_aptitude, chromosomes, aptitudes = self.selection(chromosomes, nbest)
                best_aptitude.append((best_chrom[0],best_chrom_aptitude[0]))
                new_generation = self.crossing(chromosomes, aptitudes, len(chromosomes)-nbest)
                new_generation = self.mutation(new_generation)
                new_generation = self.substitution(new_generation, protacion)
                new_generation.extend(best_chrom)
                chromosomes = np.array(new_generation)
                i += 1
                if i%100==0:
                    print(10*'=', end='\n')
                    print(best_chrom[0],' ', best_chrom_aptitude[0])
            return best_aptitude
        except KeyboardInterrupt:
            return best_aptitude


# bin_dims = [([4,1],'1'),([3,2],'2'),([4,3],'3'),([2,2],'4'),([2,1],'5'),([6,1],'6'),([4,2],'7'),([2,6],'8')]
# #material size
# print(bin_dims)
# area = [10,10]

# a = AlgoritmoGenetico(area)
# a.run(bin_dims,2,20,0.8, 4000)