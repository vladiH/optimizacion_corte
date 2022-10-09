import random
def vectorToCoordinates(vector):
    '''
    vector:[x,y]
    return: [0,0,x,y]
    '''
    return [0,0,vector[0],vector[1]]

def changeOrientation(coordinate):
    '''
    coordinates:[x0,y0,x1,y1]
    return:[x0,y0,x0+(y1-y0),y0+(x1-x0)]
    '''
    x0,y0,x1,y1 = coordinate
    aux = x1
    x1 = x0 + abs(y1-y0)
    y1 = y0 + abs(aux - x0)
    return [x0,y0,x1,y1]

def isIntersect(area1,area2):
    ''''
    area1, area2 = [x0,y0,x1,y1]
    '''
    xa0,ya0,xa1,ya1 = area1
    xa_top_left,ya_top_left = xa0, ya1
    xa_bottom_right,ya_bottom_right = xa1, ya0
    xb0,yb0,xb1,yb1 = area2
    xb_top_left,yb_top_left = xb0, yb1
    xb_bottom_right,yb_bottom_right = xb1, yb0
    x0 = max(xa_top_left,xb_top_left)
    y0 = min(ya_top_left,yb_top_left)
    x1 = min(xa_bottom_right,xb_bottom_right)
    y1 = max(ya_bottom_right,yb_bottom_right)
    #print(x0,y0,x1,y1)
    area = max(0,x1-x0)*max(0,y0-y1)
    return area

def generate_input(n, min_size, max_size):
    result = []
    for i in range(1,n+1):
        x0 = random.randint(min_size,max_size)
        y0 = random.randint(min_size,max_size)
        result.append(([x0,y0],str(i)))
    return result



# print(is_contained([0,0,3,3],[0,0,2,2]))
# print(is_intersect([0,0,2,2],[0,0,2,2]))