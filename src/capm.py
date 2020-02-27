import numpy as np
import cvxpy as cp


class CAPM:
    """
    MM : Mean Matrix
    CM : Covariance Matrix
    EM : Expected Mean
    RR : Risk free return
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
    def __init__(self, MM, CM, EM, RR, **kwargs):
        # Stocks data
        self.MM = MM
        self.RR = RR
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
        identity = [1]*self.n
        O = np.array(identity)
        CI = np.linalg.inv(self.CM)

        self.w_risky = ((self.MM - self.RR * O) @ CI ) / ((self.MM - self.RR * O) @ CI @ O.T)
        
        self.ret_der = ( self.MM @ self.w_risky.T )
        self.risk_der = cp.quad_form(self.w_risky, self.CM).value

        # capm line
        slope = ( self.ret_der - self.RR ) / ( self.risk_der )
        line_eqn = lambda x: (slope * x + self.RR)
        self.capm_risk = np.arange( 0, self.risk_der*2, 0.000001)
        self.capm_ret = np.array([line_eqn(x) for x in self.capm_risk])
        # print(self.capm_risk)
        # print(self.capm_ret)

    def plot(self, ax):
        # x axis
        ax.axhline(color='#000000')

        # y axis
        ax.axvline(color='#000000')

        # Risk free point
        ax.plot(0, self.RR, label='Risk free point', marker='o')

        # Market point
        ax.plot(self.risk_der, self.ret_der, label='Market point', marker='o')

        # CAPM line
        ax.plot(self.capm_risk, self.capm_ret, label='CAPM line')

        # Add a title
        ax.set_title('Capital assets pricing model')

        # Add X and y Label
        ax.set_xlabel('σ axis')
        ax.set_ylabel('μ axis')

        # Add a grid
        ax.grid(alpha=.4,linestyle=':')

        # Add a Legend
        ax.legend(prop={"size":7})
