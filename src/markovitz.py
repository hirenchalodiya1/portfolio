import numpy as np


class MarkowitzBullet:
    """
    MM : Mean Matrix
    CM : Covariance Matrix
    EM : Expected Mean
    n : Number of stocks

    w : weightage for market point
    risk : min risk for given mean
    ret: given mean

    var_mean : min variance
    ret_mean : return fot min variance

    line_mean : mean line
    line_var: variance line
    """

    def __init__(self, mean_matrix, covariance_matrix, expected_mean, **kwargs):
        # Stocks data
        self.MM = mean_matrix
        self.CM = covariance_matrix
        self.EM = expected_mean
        self.n = len(self.MM)

        # Curve properties
        self.mu_min = kwargs.get('mu_min', 0.00)
        self.mu_max = kwargs.get('mu_max', 0.50)
        self.mu_gap = kwargs.get('mu_gap', 0.005)

        # Prepare matrices
        identity = [1] * self.n
        self.CI = np.linalg.inv(self.CM)  # C inverse
        self.Identity = np.array(identity)

        self._a = ((self.CI @ self.Identity.T) * (self.MM @ self.CI @ self.MM.T))
        self._b = ((self.CI @ self.Identity.T) * (self.Identity @ self.CI @ self.MM.T))
        self._c = (self.Identity @ self.CI @ self.Identity.T * self.MM @ self.CI @ self.MM.T)  # scalar
        self._d = (self.MM @ self.CI @ self.Identity.T * self.Identity @ self.CI @ self.MM.T)  # scalar
        self._e = ((self.CI @ self.MM.T) * (self.Identity @ self.CI @ self.Identity.T))
        self._f = ((self.CI @ self.MM.T) * (self.MM @ self.CI @ self.Identity.T))

        # mu and sigma line
        self.line_mu = list()
        self.line_sigma = list()

        # For minimum risk, risk and return
        self.ret_min = None
        self.risk_min = None

        # Portfolio for giver data
        self.w = None
        self.ret = None
        self.risk = None

        # Prepare lines
        self.prepare()

    def prepare(self):
        mu_range = np.arange(self.mu_min, self.mu_max, self.mu_gap)  # mu_range : mu range

        # sg = lambda mu: cp.quad_form(solvePortfolio(self.CM, self.MM, mu), self.CM).value  # sg : sigma generator

        def sigma_generator(em):
            w = self.solve_sub_problem(em)
            return w.T @ self.CM @ w

        mu = []
        sigma = []

        for m in mu_range:
            s = sigma_generator(m)
            sigma.append(np.sqrt(s))
            mu.append(m)

        if not len(mu):
            raise ValueError('Data are not proper')

        self.mu_min = max(self.mu_min, mu[0])
        self.mu_max = min(self.mu_max, mu[-1])

        # variance and mean line
        self.line_mu = np.array(mu)
        self.line_sigma = np.array(sigma)

        # minimum variable
        w_min = (self.Identity @ self.CI) / (self.Identity @ self.CI @ self.Identity.T)
        self.ret_min = (self.MM @ w_min.T)
        self.risk_min = np.sqrt(w_min @ self.CM @ w_min.T)

        # Solve problem
        if not self.mu_min <= self.EM <= self.mu_max:
            raise ValueError('Return is not in range')

        self.w = self.solve_sub_problem(self.EM)
        self.ret = self.EM
        self.risk = np.sqrt(self.w @ self.CM @ self.w.T)

    def solve_sub_problem(self, expected_mean):
        """
        λ1 = ( a - μ * b ) / ( c - d )
        λ2 = ( μ * e - f ) / ( c - d )
        w = λ1 + λ2
        """
        denominator = self._c - self._d
        lambda1 = (self._a - expected_mean * self._b) / denominator
        lambda2 = (expected_mean * self._e - self._f) / denominator
        return lambda1 + lambda2

    def plot(self, ax, line_only=False):
        # Bullet line
        ax.plot(self.line_sigma, self.line_mu, label='μ vs σ : Markowitz bullet')

        # Fill frontier
        ax.fill_between(self.line_sigma, self.ret_min, self.line_mu, where=self.line_mu >= self.ret_min,
                        color='#8FE388', label='Efficient frontier')

        # Lowest point
        ax.plot(self.risk_min, self.ret_min, marker="o")

        if not line_only:
            # Market  point
            ax.plot(self.risk, self.ret, label='Optimal point for given μ', marker="o")

            # Add a title
            ax.set_title('Markowitz bullet')

            # Add X and y Label
            ax.set_xlabel('σ axis')
            ax.set_ylabel('μ axis')

            # Add a grid
            ax.grid(alpha=.4, linestyle=':')

            # Add a Legend
            ax.legend(prop={"size": 7})
