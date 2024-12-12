def apply_minmax(depth,max_min,root):
        if len(root.children) ==0 | depth==0:
            return root.evaluation
        
        if max_min:
            root.evaluation= float('-inf')
            for child in root.children:
                root.evaluation = max(root.evaluation,apply_minmax(depth-1,False,child))
            return root.evaluation
        else:
            root.evaluation= float('inf')
            for child in root.children:
                root.evaluation = min(root.evaluation,apply_minmax(depth-1,True,child))
            return root.evaluation
        

def apply_alphabeta(depth, max_min, root, alpha=float('-inf'), beta=float('inf')):

    if len(root.children) == 0 or depth == 0:
        return root.evaluation
    
    if max_min:  
        root.evaluation = float('-inf')
        for child in root.children:
            eval_value = apply_alphabeta(depth - 1, False, child, alpha, beta)
            
            root.evaluation = max(root.evaluation, eval_value)
            alpha = max(alpha, root.evaluation)
            
            if beta <= alpha: # cut-off
                print("beta cutoff")
                break  
        
        return root.evaluation
    
    else:  
        root.evaluation = float('inf')
        for child in root.children:
            eval_value = apply_alphabeta(depth - 1, True, child, alpha, beta)
            
            root.evaluation = min(root.evaluation, eval_value)
            beta = min(beta, root.evaluation)
            
            if beta <= alpha: 
                print("alpha cutoff")
                break 
        
        return root.evaluation

