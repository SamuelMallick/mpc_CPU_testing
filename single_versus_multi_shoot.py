import gurobipy as gp
import numpy as np
from scipy.linalg import block_diag

np.random.seed(0)

# dynamics
A = np.array([[1.2, 0.5], [0.8, 1.1]])
# A = np.array([[0.8, 0], [0, 0.7]])
B = np.array([[0.3], [0.4]])

# cost
Q = np.eye(2)
R = np.eye(1)

# horizon
N = 20

MIP = True

class OptProb:
    m : gp.Model
    IC: gp.MConstr
    def save_model(self):
        self.m.write(f'{self.m.ModelName}.mps')
    
    def solve_mpc(self, IC: np.ndarray):
        self.m.setParam("OutputFlag", True)
        self.m.setParam('Presolve', True)
        if hasattr(self, 'IC'):
            self.IC.RHS = IC
        self.m.optimize()
        if self.m.Status == 2:
            t = self.m.Runtime
            J = self.m.ObjVal
            print(f'Solved {self.m.ModelName} succesfully: t = {t:.20f}, J = {J}.')
            return t
        else:
            print(f'Failed solving {self.m.ModelName}.')


class MultiShoot(OptProb):
    def __init__(self) -> None:
        m = gp.Model('multi_shoot')
        x = m.addMVar((2, N+1), name='x', lb=-float('inf'))
        u = m.addMVar((1, N), name='u', lb=-10, ub=10, vtype=gp.GRB.INTEGER if MIP else gp.GRB.CONTINUOUS)

        # IC
        self.IC = m.addConstr(x[:, [0]] == 0)    

        # dynamics
        m.addConstrs((x[:, [k+1]] == A@x[:, [k]] + B@u[:, [k]] for k in range(N)), name='dynamics')

        # cost
        cost = sum([x[:, k]@Q@x[:, [k]] for k in range(N+1)])
        cost += sum([u[:, k]@R@u[:, [k]] for k in range(N)])

        m.setObjective(cost, gp.GRB.MINIMIZE)
        self.m = m
        self.x = x
        self.u = u

class SingleShoot(OptProb):
    def __init__(self) -> None:
        m = gp.Model('single_shoot')
        x0 = m.addMVar((2, 1), name='x0', lb=-10, ub=10)
        u = m.addMVar((1, N), lb=-10, ub = 10, name='u', vtype=gp.GRB.INTEGER if MIP else gp.GRB.CONTINUOUS) 

        # cost 
        cost = 0
        x = x0
        for k in range(N+1):
            M = Q@x
            cost += sum(x[i] * M[i] for i in range(x.shape[0]))
            if k < N:
                x = A@x + B@u[:, [k]]
        cost += sum([u[:, k]@R@u[:, [k]] for k in range(N)])

        m.setObjective(cost, gp.GRB.MINIMIZE)
        self.m = m
        self.x0 = x0
        self.u = u
    
    def solve_mpc(self, IC: np.ndarray):
        self.x0.lb = IC
        self.x0.ub = IC
        return super().solve_mpc(IC)
    
class QuadProg(OptProb):
    def __init__(self) -> None:
        m = gp.Model('quad_prog')
        x0 = m.addMVar((2, 1), name='x0', lb=-10, ub=10)
        u = m.addMVar((1, N), lb=-10, ub = 10, name='u', vtype=gp.GRB.INTEGER if MIP else gp.GRB.CONTINUOUS) 

        A_b = np.vstack([np.linalg.matrix_power(A, i) for i in range(1, N+1)])
        B_b = np.zeros((2*N, N))
        for i in range (N):
            for j in range(i+1):
                if j == i:
                    B_b[2*i:2*i+2, [j]] = B
                else:
                    B_b[2*i:2*i+2, [j]] = np.linalg.matrix_power(A, i-j)@B
        Q_b = block_diag(*[Q]*N)
        R_b = block_diag(*[R]*N)

        H = B_b.T@Q_b@B_b + R_b
        c = 2*x0.T@A_b.T@Q_b@B_b

        # + x0.T@(A_b.T@Q_b@A_b + Q)@x0
        m.setObjective(u@H@u.T + c@u.T + x0.T@(A_b.T@Q_b@A_b + Q)@x0, gp.GRB.MINIMIZE)
        self.m = m
        self.x0 = x0
        self.u = u
    
    def solve_mpc(self, IC: np.ndarray):
        self.x0.lb = IC
        self.x0.ub = IC
        return super().solve_mpc(IC)


num_ICs = 1
x0s = np.random.uniform(-10, 10, (2, num_ICs))
quad_prog = QuadProg()
single = SingleShoot()
multi = MultiShoot()

qp_t = [quad_prog.solve_mpc(x0s[:, [i]]) for i in range(num_ICs)]
sing_t = [single.solve_mpc(x0s[:, [i]]) for i in range(num_ICs)]
mult_t = [multi.solve_mpc(x0s[:, [i]]) for i in range(num_ICs)]
print(f'qp: {sum(qp_t)/len(qp_t)}, sing: {sum(sing_t)/len(sing_t)}, mult: {sum(mult_t)/len(mult_t)}')