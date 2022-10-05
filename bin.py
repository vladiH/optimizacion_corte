class Bin:
    def __init__(self, coordinates, id):
        '''
        coordinates:[x0,y0,x1,y1]
        x0,y0:bottom left coordinates
        x1,y1:top right coordinates
        '''
        self.x0, self.y0, self.x1, self.y1 = coordinates
        self._id = id

    def id(self):
        return self._id
    
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