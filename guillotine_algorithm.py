import utils
from node import Node
from area import Area
class GuillotineAlgorithm():
    def __init__(self,area):
        '''
        area:[x0,y0,x1,y1]
        x0,y0:bottom left coordinates
        x1,y1:top right coordinates
        '''
        self.main_area = Node(Area(area,'Area'))
        self.nodes:list[Node] = [self.main_area]
    
    
    def getNodes(self):
        self.main_area.get_nodes()

    def spaceDirection(self, area):
        '''
        calculate direction of some space and return 0 if direction is horizontal else 1 if direction is vertical
        area:[x0,y0,x1,y1]
        x0,y0:bottom left coordinates
        x1,y1:top right coordinates
        '''
        x0,x1,y0,y1 = area
        return 0 if abs(x0-x1)>abs(y0-y1) else 1
    
    def cut(self, bin_list):
        '''
        bin_list = [([x0,y0,x1,y1],id)....([x0,y0,x1,y1],id)]
        '''
        while len(self.nodes)>0:
            flag_cut = False
            index = 0 
            current_node = self.nodes[0]
            while len(bin_list)>index:
                bin = bin_list[index]
                #skip this if it already have childs
                if current_node.children !=None:
                    continue
                if current_node.value.add_sub_area(bin[0],bin[1]):
                    flag_cut = True
                    del bin_list[index]
                    index -=1
                index +=1
            if len(bin_list)==0:
                break
            if not flag_cut:
                #no_used.append(bin)
                a1,a2 = current_node.value.split_area()
                del self.nodes[0]
                if a1!=None:
                    node1 = current_node.add_child(Area(a1[1],'Area'), position=a1[0])
                    self.nodes.append(node1)
                if a2!=None:
                    node2 = current_node.add_child(Area(a2[1],'Area'), position=a2[0])
                    self.nodes.append(node2)


g = GuillotineAlgorithm([0,0,10,5])
bin_dims = [[1,5],[2,4],[1,4],[3,3],[1,1]]
entrada = []
i =0
for bin in bin_dims:
    entrada.append(([0,0,bin[0],bin[1]],str(i)))
    i +=1
g.cut(entrada)
g.getNodes()
