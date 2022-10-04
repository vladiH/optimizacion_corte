import utils
class Area:
    def __init__(self, coordinates, id):
        '''
        data:([x0,y0,x1,y1],id)
        x0,y0:bottom left coordinates
        x1,y1:top right coordinates
        '''
        self.x0, self.y0, self.x1, self.y1 = coordinates
        self.id = id
        self._sub_area:list[Area] = []
        self._polish_notation = None

    def get_sub_area(self):
        return self._sub_area;

    def add_sub_area(self, coordinates, id):
        '''
        data:([x0,y0,x1,y1],id)
        x0,y0:bottom left coordinates
        x1,y1:top right coordinates
        '''
        id = str(id)
        x0, y0, x1, y1 = coordinates
        if len(self._sub_area)==0:
            if utils.isContained([x0, y0, x1, y1],self.get_coordinate()):
                self._sub_area.append(Area([self.x0, self.y0, self.x0+max((x1-x0),0), self.y0 + max((y1-y0),0)], id))
                self._polish_notation = id
                return True
        else:
            horientation,(ax0,ay0,ax1,ay1) = self.get_available_area()
            if utils.isContained([x0, y0, x1, y1],[ax0,ay0,ax1,ay1]):
                self._sub_area.append(Area([ax0, ay0, ax0+max((x1-x0),0), ay0 + max((y1-y0),0)], id))
                self._polish_notation += " "+id+" " +horientation
                return True
        return False

    def get_first_sub_area(self):
        return None if len(self._sub_area) == 0 else self._sub_area[0]
    
    def get_last_sub_area(self):
        return None if len(self._sub_area) == 0 else self._sub_area[-1]
    
    def get_available_area(self):
        '''
        return horientation,[self.x0,self.y0,self.x1,self.y1]
        x0,y0:bottom left coordinates
        x1,y1:top right coordinates
        '''
        if len(self._sub_area) == 0:
            return self.get_orientation(), self.get_coordinate()

        first = self.get_first_sub_area()
        forientation = first.get_orientation()
        fx0,fy0,fx1,fy1 = first.get_coordinate()

        last = self.get_last_sub_area()
        lx0,ly0,lx1,ly1 = last.get_coordinate()
        if forientation=='H':
            return 'H',[lx1,fy0,self.get_coordinate()[2],ly1]
        else:
            return 'V',[fx0,ly1,fx1,self.get_coordinate()[3]]
    
    def split_area(self):
        horientation, area = self.get_available_area()
        available_area = abs(area[0]-area[2])*abs(area[1]-area[3])
        if self.get_area()==available_area:
            return None, None
        area1, area2 = None,None
        if horientation=='H':
            area1 = ('H',(area[0],area[1], self.x1, self.y1))
            area2 = ('V',(self.x0, area[3], area[0],self.y1))
        else:
            area1 = ('V',(self.x0, area[1], self.x1,self.y1))
            area2 = ('H',(area[2],self.y0, self.x1, area[1]))
        if available_area==0:
            area1 = None

        return area1,area2

    def get_polish_notation(self):
        return self._polish_notation

    def get_id(self):
        return self.id
    
    def get_area(self):
        return abs(self.x1-self.x0)*abs(self.y1-self.y0)
    
    def get_coordinate(self):
        return [self.x0,self.y0,self.x1,self.y1]
    
    def get_width(self):
        return abs(self.x1-self.x0)
    
    def get_height(self):
        return abs(self.y1-self.y0)
    
    def get_orientation(self):
        return 'H' if self.get_width()>=self.get_height() else 'V'
    
    def change_orientation(self):
        self.x0 = self.x0 
        self.y0 = self.y0
        aux = self.x1
        self.x1 = self.x0 + abs(self.y1-self.y0)
        self.y1 = self.y0 + abs(aux - self.x0)

    # def rotate(self, angle):
    #     angle = angle * np.pi/180
    #     x0,y0,x1,y1 = self.get_coordinate()
    #     return np.dot(np.array([[np.cos(angle), -np.sin(angle)],[np.sin(angle), np.cos(angle)]]),np.array([[x0,x1],[y0,y1]]))


class Stack():
    # Constructor to initialize the class variables
    def __init__(self):
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
    def evaluatePostfix(self, exp):
         
        # Iterate over the expression for conversion
        for i in exp:
             
            # If the scanned character is an operand
            # (number here) push it to the stack
            if i.isdigit():
                self.push(i)
 
            # If the scanned character is an operator,
            # pop two elements from stack and apply it.
            else:
                val1 = self.pop()
                val2 = self.pop()
                self.push(str(eval(val2 + i + val1)))
 
        return int(self.pop())



# x = Area(([0,0,10,10],'P'))

# bins = [([0,0,4,2],'1'),([0,0,5,2],'1'),([0,0,1,3],'1'),([0,0,2,1],'1')]

# for b in bins:
#     x.add_sub_area(b)

# for b in x._sub_area:
#     print(b.get_coordinate())

# print(x.get_available_area())
# print(x._operator)
# print(x.get_first_sub_area().get_coordinate(), x.get_last_sub_area().get_coordinate())