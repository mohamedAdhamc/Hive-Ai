class StateTreeNode:
    
    def __init__(self, parent = None, move = None, evaluation = 0, depth = 0):
        self.evaluation = evaluation
        self.move = move
        self.children = []
        self.parent = parent
        self.depth = depth

    def print_tree(self):
        if self.children == []:
            print("|   " * (self.depth-1) + "|-> ", end="")
            print(self.move, self.evaluation)
            return
        if self.depth > 0:
            print("|   " * (self.depth-1) + "|-> ", end="")
            #print(self.move)
            print(self.move, self.evaluation)
        for child in self.children:
            child.print_tree()