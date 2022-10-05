from area import Area
class Node:
    def __init__(self, value:Area):
        self.value = value
        self.left = None
        self.right = None
        self.position = ''

    def add_child(self, child:Area, position):
        node = Node(child)
        node.position = position
        if position=='H':
            self.right = node
        elif position=='V':
            self.left = node
        else:
            raise Exception('Invalid')
        return node

    def polish_structure(self, root):
        res = ''
        res_dire = ''
        if root:
            polish_notation, orientation = root.value.polish_notation()
            if polish_notation:
                res = polish_notation
                res_dire = orientation
                n,o = self.polish_structure(root.left)
                res += ' '+n
                res_dire += o
                n,o = self.polish_structure(root.right)
                res += ' '+n
                res_dire += o
                res += ' '+root.position
        return res, res_dire
    
    # def polish_structure(self, root):
    #     res = []
    #     if root:
    #         polish_notation = root.value.polish_notation()
    #         if polish_notation:
    #             res = root.value.bin_positions()
    #             res += ' '+self.polish_structure(root.left)
    #             res += ' '+self.polish_structure(root.right)
    #             res += ' '+root.position
    #     return res

    # def add_child_by_value(self, value):
    #     self.children.add_child(Node(value))

    # def add_children(self, list_of_children):
    #     for child in list_of_children:
    #         self.add_child(child)

    # def is_leaf(self):
    #     return self.children is None