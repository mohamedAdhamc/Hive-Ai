-- all possible moves and placements (nassar)
-- constrains (queen not surrounded, hive connected)
-- evaluation function (ali, zain)
-- normal min max (fady)
-- alpha beta min max (adel)
-- iterative deepening (ayman)

-- notation:
-- movement -> ( (2,1), (3,0) )
-- deploy -> ( "ant", (2,1) )

-- output: an array of tuples with all possible moves
function array<Tuple> allPossibleMoves (Board board_state)

-- output: the evaluation of the current board state
function int evaluateBoard (Board board_state)

-- output: a tuple with the movement of the chosen child
function Tuple getBestMove (StateTree root)
    normalMinMax(root) || alphabetaPruning(root) || iterativeDeepening(root)
    for (root.children)
        -- find root child with max score    
    return max_score_child.move

-- output: a score of the evaluation of the current node
function int normalMinMax (StateTree node, bool max_or_min)
    -- inputs:
    -- node: a StateTreeNode object with the current node of the tree
    -- max_or_min: a boolean that determines if the current level is maximizer or minimizer
    return score

-- output: a score of the evaluation of the current node
function int alphabetaPruning (StateTree node, bool max_or_min)
    -- inputs:
    -- node: a StateTreeNode object with the current node of the tree
    -- max_or_min: a boolean that determines if the current level is maximizer or minimizer
    return score

-- output: a score of the evaluation of the current node
function int iterativeDeepening (int max_time)
    -- inputs:
    -- max_time: the maximum number of operations that can be performed by the ai
    return score
