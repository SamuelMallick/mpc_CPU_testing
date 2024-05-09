import gurobipy as gp
import pyomo.environ as pyo
import numpy as np
from scipy.linalg import block_diag
import time

np.random.seed(0)

# dynamics
mass = 800
c = 0.5
mu = 0.01
g = 9.8
b = 1600
dt = 1
A1 = np.array([[0, 1], [0, 0]])
A2 = np.array([[0], [-c/mass]])
A3 = np.array([[0], [mu*g]])
B = np.array([[0], [b/mass]])

# cost
Q = np.eye(2)
R = np.eye(1)

# horizon
N = 30

MIP = True

class OptProb:
    m : gp.Model
    IC: gp.MConstr
    def save_model(self):
        self.m.write(f'{self.m.ModelName}.mps')
    
    def solve_mpc(self, IC: np.ndarray):
        self.m.setParam("OutputFlag", False)
        self.m.setParam('Presolve', True)
        if hasattr(self, 'IC'):
            self.IC.RHS = IC
        s = time.time()
        self.m.optimize()
        e = time.time()
        print(f'g time {e-s}')
        if self.m.Status == 2:
            t = self.m.Runtime
            J = self.m.ObjVal
            print(f'Solved {self.m.ModelName} succesfully: t = {t:.20f}, J = {J}.')
            return t
        else:
            print(f'Failed solving {self.m.ModelName}.')


class QuadraticallyConstrainedMPC(OptProb):
    def __init__(self) -> None:
        m = gp.Model('multi_shoot')
        x = m.addMVar((2, N+1), name='x', lb=-float('inf'))
        u = m.addMVar((1, N), name='u', lb=-1, ub=1, vtype=gp.GRB.INTEGER if MIP else gp.GRB.CONTINUOUS)

        # IC
        self.IC = m.addConstr(x[:, [0]] == 0)    

        # dynamics
        m.addConstrs((x[:, [k+1]] == x[:, [k]] + dt*(A1@x[:, [k]] + x[1, k]*A2*x[1, k] - A3 + B@u[:, [k]]) for k in range(N)), name='dynamics')
        # m.addConstrs((x[:, [k+1]] == x[:, [k]] + dt*(A1@x[:, [k]] + x[1, k]*A2*x[1, k]) for k in range(N)), name='dynamics')

        # cost
        cost = sum([x[:, k]@Q@x[:, [k]] for k in range(N+1)])
        cost += sum([u[:, k]@R@u[:, [k]] for k in range(N)])

        m.setObjective(cost, gp.GRB.MINIMIZE)
        self.m = m
        self.x = x
        self.u = u

class PyoMPC:
    def __init__(self) -> None:
        m = pyo.ConcreteModel()

        m.u = pyo.Var(pyo.RangeSet(1), pyo.RangeSet(N), within=pyo.Integers, bounds=(-1,1))
        m.x = pyo.Var(pyo.RangeSet(2), pyo.RangeSet(N+1), within=pyo.Reals)
        
        m.dynamics_set = pyo.RangeSet(N)
        dynam1 = lambda m, s: m.x[1, s+1] == m.x[1, s] + dt*(m.x[2, s]) 
        # dynam2 = lambda m, s: m.x[2, s+1] == m.x[2, s] + m.u[1, s]
        dynam2 = lambda m, s: m.x[2, s+1] == m.x[2, s] + dt*(-(c/mass)*m.x[2, s]*m.x[2, s] - mu*g + (b/mass)*m.u[1, s])

        m.IC_1 = pyo.Constraint(expr=(m.x[1, 1] == -100))
        m.IC_2 = pyo.Constraint(expr=(m.x[2, 1] == 1.3))

        m.dynamics1 = pyo.Constraint(m.dynamics_set, rule=dynam1)
        m.dynamics2 = pyo.Constraint(m.dynamics_set, rule=dynam2)

        m.cost_set_x = pyo.RangeSet(N+1)
        m.cost_set_u = pyo.RangeSet(N)
        cost_x = lambda m, s: m.x[1, s]*m.x[1, s] + m.x[2, s]*m.x[2, s]
        cost_u = lambda m, s: m.u[1, s]*m.u[1, s]
        m.obj1 = pyo.Objective(expr=sum(cost_x(m, k) for k in m.cost_set_x) + sum(cost_u(m, k) for k in m.cost_set_u), sense=pyo.minimize)

        # pyo.SolverFactory('mindtpy').solve(m)
        solver = pyo.SolverFactory('mindtpy')
        
        s = time.time()
        res = solver.solve(m, mip_solver='gurobi', nlp_solver='ipopt', mip_solver_mipgap = 0.002, tee=True) 
        e = time.time()
        print(f'pyo time {e-s}')

        if res.solver.termination_condition == pyo.TerminationCondition.optimal:
            print(f'f: {m.obj1()}')
        else:
            print('infeas')
            

PyoMPC()
x0 = np.array([[-100], [1.3]])
constrained = QuadraticallyConstrainedMPC()
constrained.solve_mpc(x0)


# class PolynominalCostMPC(OptProb):
#     def __init__(self) -> None:
#         m = gp.Model('single_shoot')
#         x0 = m.addMVar((2, 1), name='x0')
#         u = m.addMVar((1, N), lb=-1, ub = 1, name='u', vtype=gp.GRB.INTEGER if MIP else gp.GRB.CONTINUOUS) 

#         # cost 
#         cost = 0
#         x = x0
#         for k in range(N+1):
#             M = Q@x
#             cost += sum(x[i] * M[i] for i in range(x.shape[0]))
#             if k < N:
#                 x = x + dt*(A1@x + x[1, 0]*A2*x[1, 0] - A3 + B@u[:, [k]])
#         cost += sum([u[:, k]@R@u[:, [k]] for k in range(N)])

#         m.setObjective(cost, gp.GRB.MINIMIZE)
#         self.m = m
#         self.x0 = x0
#         self.u = u
    
#     def solve_mpc(self, IC: np.ndarray):
#         self.x0.lb = IC
#         self.x0.ub = IC
#         return super().solve_mpc(IC)


