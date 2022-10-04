def isContained(area1,area2):
    ''''
    area1, area2 = [xbottom_left, ybottom_left, xtop_right, ytop_right]
    '''
    xa0,ya0,xa1,ya1 = area1
    area1 = area2[0], area2[1], area2[0]+abs(xa0-xa1), area2[1]+abs(ya0-ya1)

    return area1[0]>=area2[0] and area1[1]>=area2[1] and area1[2]<=area2[2] and area1[3]<=area2[3]

def isIntersect(area1,area2):
    ''''
    area1, area2 = [xbottom_left, ybottom_left, xtop_right, ytop_right]
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

# print(is_contained([0,0,3,3],[0,0,2,2]))
# print(is_intersect([0,0,2,2],[0,0,2,2]))