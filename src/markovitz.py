import numpy as np
import cvxpy as cp


class MarkowitzBullet:
    """
    MM : Mean Matrix
    CM : Covariance Matrix
    EM : Expected Mean
    n : Number of stocks
    
    w : weightage for market point
    risk : min risk for given mean
    ret: given mean

    w_min : min weightage for sigma mean
    var_mean : min variance
    ret_mean : return fot min variance

    line_mean : 
    line_var: 
    """
    def __init__(self, MM, CM, EM, **kwargs):
        # Stocks data
        self.MM = MM
        self.CM = CM
        self.EM = EM
        self.n = len(self.MM)        
        
        # Curve properties
        self.mu_min = kwargs.get('mu_min', 0.00)
        self.mu_max = kwargs.get('mu_max', 0.50)
        self.mu_gap = kwargs.get('mu_gap', 0.005)
        
        # Prepate lines
        self.prepare()

    def prepare(self):
        mu_range = np.arange( self.mu_min, self.mu_max, self.mu_gap)  # mu_range : mu range
        sg = lambda mu: cp.quad_form(self.solveSub(mu), self.CM).value  # sg : sigma generator

        mu = []
        sigma = []
        
        for m in mu_range:
            try:
                s = sg(m)
                sigma.append(s)
                mu.append(m)
            except cp.error.DCPError:
                pass

        if not len(mu):
            raise ValueError('Data are not proper')

        self.mu_min = max(self.mu_min, mu[0])
        self.mu_max = min(self.mu_max, mu[-1])

        # variance and mean line
        self.line_mean = np.array(mu)
        self.line_var = np.array(sigma)

        # minimum variable
        self.w_min = self.solveSub()
        self.risk_min = cp.quad_form(self.w_min, self.CM).value
        self.ret_min = (self.MM @ self.w_min.T)

        # Solve problem
        if not self.mu_min <= self.EM <= self.mu_max:
            raise ValueError('Return is not in range')

        self.w = self.solveSub(self.EM)
        self.risk = cp.quad_form(self.w, self.CM).value
        self.ret = self.EM

    def solveSub(self, EM=None):
        w = cp.Variable(self.n)
        risk = cp.quad_form(w, self.CM)
        conditions = [
            sum(w) == 1,
            self.MM @ w.T == EM
        ]
        if EM is None:
            conditions = [
                sum(w) == 1
            ]
        
        prob = cp.Problem(cp.Minimize(risk), conditions)
        prob.solve()
        return np.array(w.value)

    def plot(self, ax):
        # Bullet line
        ax.plot(self.line_var, self.line_mean, label='μ vs σ : Markowitz bullet')

        # Market  point        
        ax.plot(self.risk, self.ret, label='Min σ for given μ', marker="o")

        # Lowest point
        ax.plot(self.risk_min, self.ret_min, marker="o")

        # Fill frontier
        ax.fill_between(self.line_var, self.ret_min, self.line_mean, where=self.line_mean >= self.ret_min,  color='#8FE388', label='Efficient frontier')

        # Add a title
        ax.set_title('Markowitz bullet')

        # Add X and y Label
        ax.set_xlabel('σ axis')
        ax.set_ylabel('μ axis')

        # Add a grid
        ax.grid(alpha=.4,linestyle=':')

        # Add a Legend
        ax.legend(prop={"size":7})
