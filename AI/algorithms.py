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
                break

        return root.evaluation

    else:
        root.evaluation = float('inf')
        for child in root.children:
            eval_value = apply_alphabeta(depth - 1, True, child, alpha, beta)

            root.evaluation = min(root.evaluation, eval_value)
            beta = min(beta, root.evaluation)

            if beta <= alpha:
                break

        return root.evaluation

import time
def iterative_depening(max_time, max_min, tree):
    # assuming start with depth 1
    # Ex: a
    #     |->b
    #     |->c
    #     |->d
    start_time = time.time()
    result = None
    depth= 1
    while(True):
        result = apply_alphabeta(depth, max_min, tree._root)
        if (time.time() - start_time) >= max_time:
            break
        depth = depth + 1
        tree.add_level(tree._root, 1)
        tree._depth = depth
    return result
