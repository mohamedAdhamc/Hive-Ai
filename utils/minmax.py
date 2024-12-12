def minmax_func(depth,max_min,root):
        if len(root.children) ==0 | depth==0:
            return root.evaluation
        
        if max_min:
            root.evaluation= float('-inf')
            for child in root.children:
                root.evaluation = max(root.evaluation,minmax_func(depth-1,False,child))
            return root.evaluation
        else:
            root.evaluation= float('inf')
            for child in root.children:
                root.evaluation = min(root.evaluation,minmax_func(depth-1,True,child))
            return root.evaluation
        