import utils
from node import Node
from area import Area
class GuillotineAlgorithm():
    
    def structure(self):
        res,res_dir = self.main_area.polish_structure(self.main_area)
        return ' '.join(res.split()), res_dir

    def spaceDirection(self):
        return self.main_area.value.orientation
    
    def cut(self, area,bin_list):
        '''
        area:[x0,y0,x1,y1]
        x0,y0:bottom left coordinates
        x1,y1:top right coordinates
        bin_list = [([x0,y0,x1,y1],id)....([x0,y0,x1,y1],id)]
        '''
        self.main_area = Node(Area(area))
        self.nodes:list[Node] = [self.main_area]
        while len(self.nodes)>0:
            current_node = self.nodes[0]
            bin_list = [bin for bin in bin_list if not current_node.value.add_bin(bin[0],bin[1])]
            del self.nodes[0]
            if len(bin_list)==0:
                break
            a1,a2 = current_node.value.split_area()
            if a1!=None:
                node1 = current_node.add_child(Area(a1[1]), position=a1[0])
                self.nodes.append(node1)
            if a2!=None:
                node2 = current_node.add_child(Area(a2[1]), position=a2[0])
                self.nodes.append(node2)
