# Jan Zmrzly 217807
# VUT FSI Aplikovana informatika a automatizace
# Algoritmy umele intligence
# zdroj: https://gist.github.com/Bart6114/8414730

import numpy as np
from pulp import (LpProblem, LpConstraintVar, LpVariable, apis,
                  lpSum, value,
                  LpMinimize, LpConstraintGE, LpContinuous, LpInteger)

class MasterProblem:
    def __init__(self, product_length:int, items_length:np.array, items_demand:np.array, init_patterns:np.array):
        self.product_length = product_length
        self.items_length = items_length
        self.items_demand = items_demand
        self.init_patterns = init_patterns

        self.constraints = []
        self.patterns = []
        self.problem = LpProblem("1D-CuttingStockProblem", LpMinimize)
        self.objective = LpConstraintVar("objective")
        self.problem.setObjective(self.objective)
        self.get_constraints()
        self.get_patterns()

    def get_constraints(self):
        """
        Create variables & set the constraints, in other words: 
        set the minimum amount of items to be produced
        """
        for i, item in enumerate(self.items_demand):
            # Create constraintvar and set to >= demand for item
            constraint = LpConstraintVar(f"C:{i}", LpConstraintGE, item)
            self.constraints.append(constraint)
            self.problem += constraint

    def get_patterns(self):
        """
        Save initial patterns and set column constraints 
        """
        for i, pattern in enumerate(self.init_patterns):
            template = []
            [template.append(n) for n, m in enumerate(pattern) if m > 0]

            # Create decision variable: will determine how often pattern x should be produced
            decision_variable = LpVariable(f"P:{i}", 0, None, LpContinuous,
                                           lpSum(self.objective+[self.constraints[j] for j in template]))
            self.patterns.append(decision_variable)

    def solve(self):
        """
        Solves the master problem and returns the optimal dual variables and objective value
        """
        self.problem.solve(apis.PULP_CBC_CMD(msg=False))

        return [self.problem.constraints[i].pi for i in self.problem.constraints]
    
    def add_pattern(self, pattern):
        """
        Adds a new pattern to the master problem.
        """
        self.init_patterns = np.vstack([self.init_patterns, pattern])
        temp = []
        [temp.append(n) for n, m in enumerate(pattern) if m > 0]

        decision_variable = LpVariable(f"P:{self.init_patterns.size}", 0, None, LpContinuous,
                                       lpSum(self.objective+[pattern[i]*self.constraints[i] for i in temp]))
        self.patterns.append(decision_variable)

    def get_subproblem(self, duals):
        """
        Create/run new slave and return new pattern (if available)
        """
        sub_problem = SubProblem(duals, self.items_length, self.product_length)
        pattern = sub_problem.return_pattern()
        
        return pattern
    
    def set_relaxed(self, relaxed):
        """
        If no new patterns are available, solve model as IP problem
        """
        if relaxed is False:
            for var in self.problem.variables():
                var.cat = LpInteger

    def get_objective(self):
        return value(self.problem.objective)
    
    def get_used_patterns(self):
        used_patterns = []
        for i, variable in enumerate(self.patterns):
            if value(variable) > 0:
                used_patterns.append((value(variable), self.init_patterns[i]))
        
        return used_patterns

class SubProblem:
    """
    Solves the sub problem for the given dual variables and returns the corresponding pattern and reduced cost.
    """
    def __init__(self, duals, items_length, product_length):
        self.sub_problem = LpProblem("SubProblemSolver", LpMinimize)
        self.variables = [LpVariable(f"S:{i}", 0, None, LpInteger) for i, x in enumerate(duals)]
        # Use duals to set objective coefficients
        self.sub_problem += -lpSum([duals[i]*x for i,x in enumerate(self.variables)])
        self.sub_problem += lpSum([items_length[i]*x for i,x in enumerate(self.variables)]) <= product_length

        self.sub_problem.solve(apis.PULP_CBC_CMD(msg=False))
        self.sub_problem.roundSolution()

    def return_pattern(self):
        pattern = False
        if value(self.sub_problem.objective) < -1.00001:
            pattern = []
            for variable in self.variables:
                pattern.append(value(variable))
        return pattern

def column_eneration(product_length, items_length, items_demand, item_count):
    """
    Solves the cutting stock problem using column generation.
    """
    items_length = np.array(items_length)
    items_demand = np.array(items_demand)

    init_patterns = np.eye(item_count)
    master_problem = MasterProblem(product_length, items_length,items_demand, init_patterns)

    relaxed = True
    # Once no more new columns can be generated set relaxed to False
    while relaxed is True:
        duals = master_problem.solve()
        new_pattern = master_problem.get_subproblem(duals)
        if new_pattern:
            master_problem.add_pattern(new_pattern)
        else:
            master_problem.set_relaxed(False)
            master_problem.solve()
            relaxed = False

    # print(f"Solution: {master_problem.get_objective()} sheets")
    used_patterns = master_problem.get_used_patterns()
    # [print(f"Pattern {i}: Selected {pattern[0]}: Times {pattern[1]}")
    #  for i, pattern in enumerate(used_patterns)]
    
    return master_problem.get_objective(), used_patterns

if __name__ == "__main__":
    product_length = 15
    items_length = np.array([4,3,2])
    items_demand = np.array([80,50,100])
    item_count = items_length.size

    column_eneration(product_length, items_length, items_demand, item_count)