import numpy as np
import math
import itertools

type_cut = np.dtype([
    ("len", int),
    ("amount", int)
])

class Node:
    def __init__(self, material_rest:int, parent, cuts:np.array, item:int):
        self.parent = parent
        self.children = []
        self.cuts = cuts
        self.material_rest = material_rest
        self.item = item
        self.extended = False
        self.in_patterns = False
        self.pattern_position = np.array([[0,0]])

    def __str__(self):
        string = (f"Cuts: {self.cuts}\tMaterial rest: {self.material_rest}\tItem: {self.item}\tExtended: {self.extended}")
        return string
    
    def __repr__(self):
        string = (f"Cuts: {self.cuts}\tMaterial rest: {self.material_rest}\tItem: {self.item}\tExtended: {self.extended}")
        return string
    
    def extend(self):
        self.extended = True

    def put_in_pattern(self):
        self.in_patterns = True

    def add_children(self, children):
        self.children = children
    
    def get_possition(self, position):
        self.pattern_position = np.vstack((self.pattern_position, position))

class Tree:
    def __init__(self, product_length:int, items_length:np.array, items_demand:np.array):
        self.product_length = product_length
        self.items_length = items_length
        self.items_demand = items_demand
        self.items_count = np.size(items_length)
        self.nodes = [] 

    def get_node(self, parent:Node, cuts:np.array, maretial_rest:int, item:int) -> Node:
        new_node = Node(maretial_rest, parent, cuts, item)
        return new_node
    
    def get_cuts(self, children:int, item:int) -> np.array:
        cuts = [np.array([(item, i)], dtype=type_cut) for i in range(children)]
        return cuts
    
    def get_children(self, parent:Node, item:int):
        children_count = math.floor(parent.material_rest/item)+1
        cuts = self.get_cuts(children_count, item)
        i = 0
        children = []
        for cut in cuts:
            material_rest = parent.material_rest-i*item
            new_node = self.get_node(parent, cut, material_rest, item)
            self.nodes.append(new_node)
            children.append(new_node)
            i += 1
        parent.extend()
        parent.add_children(children)
    
    def create_tree(self):   
        first_node = self.get_node(None, np.array([]), self.product_length, 0)
        self.nodes.append(first_node)
        self.get_children(first_node, self.items_length[0])
        
        for i, item in enumerate(self.items_length):
            if i == np.size(self.items_length)-1:
                break 
            for node in self.nodes:
                if (node.item == item and
                    node.material_rest >= item and
                    node.extended == False):
                    self.get_children(node, self.items_length[i+1])
               
        
class Patterns:
    def __init__(self, product_length:int, items_length:np.array, items_demand:np.array):
        self.product_length = product_length
        self.items_length = items_length
        self.items_demand = items_demand
        self.patterns:np.array
        self.tree_model:Tree

    def create_tree(self):
        self.tree_model = Tree(self.product_length, self.items_length, self.items_demand)
        self.tree_model.create_tree()

    def create_patterns(self):
        self.create_tree()
        
        # ctreating zeros patterns matrix, dimensions n, m
        sorted_tree = sorted(self.tree_model.nodes, key=lambda node: node.extended)
        count_extended = [(key, len(list(group))) for key, group in 
                          itertools.groupby(sorted_tree, key=lambda node: node.extended) if key == False]
        n = np.size(self.items_length)+1 # plus row with waste
        m = count_extended[0][1]
        self.patterns = np.zeros((n,m))
        
        # placing no-extended nodes to patterns matrix
        added_nodes = []
        grouped_nodes = itertools.groupby(sorted_tree, key=lambda node: node.extended)
        selected_nodes = [node for key, group in grouped_nodes for node in group if key == False]
        for i, node in enumerate(selected_nodes):
            pos = np.where(self.items_length == node.item)[0][0]
            # placing cut length
            self.patterns[pos][i] = node.cuts[0][1]
            # placing resting material
            self.patterns[n-1][i] = node.material_rest
            node.get_possition(np.array([pos, i]))
            node.put_in_pattern()
            added_nodes.append(node)

        # placing extended nodes to patterns matrix
        grouped_nodes = itertools.groupby(sorted_tree, key=lambda node: node.extended)
        selected_nodes = [node for key, group in grouped_nodes for node in group if key == True]
        # [print(child) for node in selected_nodes for child in node.children]
        for node in selected_nodes:
            for child in node.children:
                # i = child.pattern_position[0]
                # j = child.pattern_position[1]-1
                print(child.pattern_position.shape)
                # if i > 0 and j > 0:
                #     self.patterns[i][j] = node.cuts[0][1]
                #     print(i, j)
                
        
        print(self.patterns)  

if __name__ == "__main__":
    prod_len = 15
    items_len = np.array([4, 6, 7])
    items_demand = np.array([80, 50 ,100])
    pt = Patterns(prod_len, items_len, items_demand)
    pt.create_tree()
    pt.create_patterns()
    # [print(node) for node in pt.tree_model.nodes]