import numpy as np
import cvxpy as cp
from utils import solvePortfolio


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
        self.mu_gap = kwargs.get('mu_gap', 0.1)

        # Prepare war material
        identity = [1]*self.n
        self.CI = np.linalg.inv(self.CM)  # C inverse
        self.O = np.array(identity)

        self._a = ( ( self.CI @ self.O.T ) * ( self.MM @ self.CI @ self.MM.T ) )
        self._b = ( ( self.CI @ self.O.T ) * ( self.O @ self.CI @ self.MM.T ) )
        self._c = ( self.O @ self.CI @ self.O.T * self.MM @ self.CI @ self.MM.T ) # scalar
        self._d = ( self.MM @ self.CI @ self.O.T * self.O @ self.CI @ self.MM.T ) # scalar
        self._e = ( ( self.CI @ self.MM.T ) * ( self.O @ self.CI @ self.O.T ) )
        self._f = ( ( self.CI @ self.MM.T ) * ( self.MM @ self.CI @ self.O.T ) )
        
        # Prepate lines
        self.prepare()

    def prepare(self):
        mu_range = np.arange( self.mu_min, self.mu_max, self.mu_gap)  # mu_range : mu range
        sg = lambda mu: cp.quad_form(self.solveSubProblem(mu), self.CM).value  # sg : sigma generator
        # sg = lambda mu: cp.quad_form(solvePortfolio(self.CM, self.MM, mu), self.CM).value

        mu = []
        sigma = []
        
        for m in mu_range:
            try:
                s = np.sqrt(sg(m))
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
        self.w_min = solvePortfolio(self.CM, self.MM)
        self.risk_min = np.sqrt(cp.quad_form(self.w_min, self.CM).value)
        self.ret_min = (self.MM @ self.w_min.T)

        # Solve problem
        if not self.mu_min <= self.EM <= self.mu_max:
            raise ValueError('Return is not in range')

        self.w = self.solveSubProblem(self.EM)
        self.risk = np.sqrt(cp.quad_form(self.w, self.CM).value)
        self.ret = self.EM

    def solveSubProblem(self, EM):
        """
        λ1 = ( a - μ * b ) / ( c - d )
        λ2 = ( μ * e - f ) / ( c - d )
        w = λ1 + λ2
        """
        deno = self._c - self._d
        lambda1 = (self._a - EM * self._b) / deno
        lambda2 = (EM * self._e - self._f) / deno
        return lambda1 + lambda2

    def plot(self, ax):
        # x axis
        # ax.axhline(color='#000000')

        # y axis
        # ax.axvline(color='#000000')

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
