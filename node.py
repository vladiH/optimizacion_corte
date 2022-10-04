from area import Area
class Node:
    def __init__(self, value:Area, children = None):
        self.value = value
        self.children = children
        self.position = None

    def add_child(self, child:Area, position):
        node = Node(child)
        if self.children is None:
            self.children = [node]
        else:
            self.children.append(node)
        #H,V
        self.position = position
        return node

    def get_nodes(self):
        print('+++++++')
        print(self.value.get_area())
        print(self.value.id)
        print(self.position)
        print(self.value.get_polish_notation())
        if self.children is None:
            return
        for child in self.children:
            child.get_nodes()
    # def add_child_by_value(self, value):
    #     self.children.add_child(Node(value))

    # def add_children(self, list_of_children):
    #     for child in list_of_children:
    #         self.add_child(child)

    def is_leaf(self):
        return self.children is None