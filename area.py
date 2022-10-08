import numpy as np
from numpy.core.fromnumeric import shape
from bin import Bin
class Area:
    def __init__(self, coordinates):
        '''
        coordinates:[x0,y0,x1,y1]
        x0,y0:bottom left coordinates
        x1,y1:top right coordinates
        '''
        self.x0, self.y0, self.x1, self.y1 = coordinates
        #list[]
        self.bin_list:list[Bin] = []
        self._polish_notation = None
        self._bin_horientation = None

    def bins(self):
        return [data.coordinate() for data in self.bin_list];

    def add_bin(self, coordinates, id):
        '''
        coordinates:[x0,y0,x1,y1],
        id:bin id
        x0,y0:bottom left coordinates
        x1,y1:top right coordinates
        '''
        id = str(id)
        x0, y0, x1, y1 = coordinates
        horientation,(ax0,ay0,ax1,ay1) = self.available_area()
        if not self.is_contained([x0, y0, x1, y1],[ax0,ay0,ax1,ay1]):
            return False
        
        aux = Bin([ax0, ay0, ax0+max((x1-x0),0), ay0 + max((y1-y0),0)], id)
        self.bin_list.append(aux)
        if self._polish_notation==None:
            self._polish_notation = id
            self._bin_horientation = aux.orientation()
        else:
            self._polish_notation += " "+id+" " +horientation
            self._bin_horientation += aux.orientation()
        
        # print('agregado')
        # print(aux.coordinate(), aux.id())
        # print(self._polish_notation)
        return True

    def first_bin(self):
        return None if len(self.bin_list) == 0 else self.bin_list[0]
    
    def last_bin(self):
        return None if len(self.bin_list) == 0 else self.bin_list[-1]
    
    def available_area(self):
        '''
        return horientation,[self.x0,self.y0,self.x1,self.y1]
        x0,y0:bottom left coordinates
        x1,y1:top right coordinates
        '''
        if len(self.bin_list) == 0:
            return self.orientation(), self.coordinate()

        first = self.first_bin()
        forientation = first.orientation()
        fx0,fy0,fx1,fy1 = first.coordinate()

        last = self.last_bin()
        lx0,ly0,lx1,ly1 = last.coordinate()
        if forientation=='H':
            return 'H',[lx1,fy0,self.coordinate()[2],ly1]
        else:
            return 'V',[fx0,ly1,fx1,self.coordinate()[3]]
    
    def split_area(self):
        horientation, area = self.available_area()
        available_area = abs(area[0]-area[2])*abs(area[1]-area[3])
        if self.area()==available_area:
            return None, None
        area1, area2 = None,None
        if horientation=='H':
            area1 = ('H',(area[0],area[1], self.x1, self.y1))
            area2 = ('V',(self.x0, area[3], area[0],self.y1))
        else:
            area1 = ('V',(self.x0, area[1], self.x1,self.y1))
            area2 = ('H',(area[2],self.y0, self.x1, area[1]))
        
        a1 = abs(area1[1][0]-area1[1][2])*abs(area1[1][1]-area1[1][3])
        a2 = abs(area2[1][0]-area2[1][2])*abs(area2[1][1]-area2[1][3])

        if a1 ==0:
            area1 = None
            
        if a2 ==0:
            area2 = None
        return area1,area2

    def polish_notation(self):
        return self._polish_notation, self._bin_horientation
    
    def bin_positions(self):
        return [bin.coordinate() for bin in self.bin_list]
    
    def area(self):
        return abs(self.x1-self.x0)*abs(self.y1-self.y0)
    
    def coordinate(self):
        return [self.x0,self.y0,self.x1,self.y1]
    
    def width(self):
        return abs(self.x1-self.x0)
    
    def height(self):
        return abs(self.y1-self.y0)
    
    def orientation(self):
        return 'H' if self.width()>=self.height() else 'V'
    
    def change_orientation(self):
        self.x0 = self.x0 
        self.y0 = self.y0
        aux = self.x1
        self.x1 = self.x0 + abs(self.y1-self.y0)
        self.y1 = self.y0 + abs(aux - self.x0)
    
    def is_contained(self, area1,area2):
        ''''
        area1, area2 = [xbottom_left, ybottom_left, xtop_right, ytop_right]
        '''
        xa0,ya0,xa1,ya1 = area1
        area1 = area2[0], area2[1], area2[0]+abs(xa0-xa1), area2[1]+abs(ya0-ya1)

        return area1[0]>=area2[0] and area1[1]>=area2[1] and area1[2]<=area2[2] and area1[3]<=area2[3]

    # def rotate(self, angle):
    #     angle = angle * np.pi/180
    #     x0,y0,x1,y1 = self.coordinate()
    #     return np.dot(np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]]),np.array([[x0,x1],[y0,y1]]))


class Stack():
    # Constructor to initialize the class variables
    def __init__(self):
        self.top = -1
        # This array is used a stack
        self.array = []
    
    def reset(self):
        self.top = -1
        # This array is used a stack
        self.array = []

    # check if the stack is empty
    def isEmpty(self):
        return True if self.top == -1 else False
     
    # Return the value of the top of the stack
    def peek(self):
        if self.isEmpty():
            return None
        return self.array[-1]
     
    # Pop the element from the stack
    def pop(self):
        if not self.isEmpty():
            self.top -= 1
            return self.array.pop()
        else:
            return "$"
     
    # Push the element to the stack
    def push(self, op):
        self.top += 1
        self.array.append(op)

    # The main function that converts given infix expression
    # to postfix expression
    def evaluatePostfix(self, dictionary, exp):
        bins_area = 0
        width = 0
        height = 0
        # Iterate over the expression for conversion
        for i in exp.split(' '):
            # If the scanned character is an operand
            # (number here) push it to the stack
            if i.isdigit():
                val = Bin(dictionary[i],i)
                self.push(val)
                bins_area+=val.area()
            # If the scanned character is an operator,
            # pop two elements from stack and apply it.
            else:
                val1 = self.pop()
                val2 = self.pop()
                if i =='H':
                    width = val1.width() + val2.width()
                    height = max(val1.height(),val2.height())
                elif i == 'V':
                    width = max(val1.width(), val2.width())
                    height = val1.height()+val2.height()
                else:
                    raise Exception('Invalid')
                self.push(Bin([0,0,width,height],val1.id()+val2.id()+str(i)))
        r = self.pop()
        return r.area(), bins_area

    def binsPositions(self, dictionary, exp):
        width = 0
        height = 0
        points = []
        # Iterate over the expression for conversion
        for i in exp.split(' '):
            # If the scanned character is an operand
            # (number here) push it to the stack
            if i.isdigit():
                val = Bin(dictionary[i],i)
                self.push(val)
 
            # If the scanned character is an operator,
            # pop two elements from stack and apply it.
            else:
                val1 = self.pop()
                val2 = self.pop()
                if i =='H':
                    width = val1.width() + val2.width()
                    height = max(val1.height(),val2.height())
                    
                elif i == 'V':
                    width = max(val1.width(), val2.width())
                    height = val1.height()+val2.height()
                else:
                    raise Exception('Invalid')
                id = val1.id()+val2.id()+str(i)
                points.append(val1.coordinate())
                self.push(Bin([0,0,width,height],id))
        r = self.pop()
        return points



# x = Area(([0,0,10,10]))
# bins = [([0,0,4,1],'1'),([0,0,3,2],'2'),([0,0,4,3],'3'),([0,0,2,2],'4'),([0,0,2,1],'5'),([0,0,6,1],'6'),([0,0,4,2],'7'),([0,0,2,6],'8')]

# for b in bins:
#     x.add_bin(b[0],b[1])

# for b in x.bins():
#     print(b)

# print(x.available_area())
# print(x.split_area())
# print(x._polish_notation)