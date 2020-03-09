class Betas:
    def __init__(self, returns_of_stocks, returns_of_market, market_ret, risk_free_return, mean_matrix, **kwargs):
        self.MM = mean_matrix
        self.RR = risk_free_return
        self.MR = market_ret

        self.betas = dict()

        market_variance = returns_of_market.var()

        # calculating betas by analysing daily market data
        for stock, returns in returns_of_stocks.items():
            beta = returns_of_market.cov(returns) / market_variance
            self.betas[stock] = beta

        # SML line
        sml_slope = (self.MR - self.RR) / (1 - 0)
        self._min_beta = min(kwargs.get('beta_min', 0), min(self.betas.values()), 0)
        self._max_beta = max(kwargs.get('beta_max', 1), max(self.betas.values()), 1)
        self.line_sml = lambda x: self.RR + sml_slope * x

    def plot(self, ax):
        # x axis
        ax.axhline(color='#000000')

        # y axis
        ax.axvline(color='#000000')

        # SML Line
        ax.plot([self._min_beta, self._max_beta], [self.line_sml(self._min_beta), self.line_sml(self._max_beta)], label='SML')

        # Add risk free point
        ax.plot(0, self.RR, label='Risk free point', marker='o')

        # Complete market point
        ax.plot(1, self.MR, label='Market point', marker='o')

        for mean, beta in zip(self.MM, self.betas.values()):
            ax.plot(beta, mean, marker='o')

        # Add a title
        ax.set_title('Security Market Line')

        # Add X and y Label
        ax.set_xlabel('β axis')
        ax.set_ylabel('μ axis')

        # Add a grid
        ax.grid(alpha=.4, linestyle=':')

        # Add a Legend
        ax.legend(prop={"size": 7})


class NewBetas:
    def __init__(self, returns_of_stocks, returns_of_market, risk_free_return):
        self.RR = risk_free_return
        self.MR = returns_of_market.mean() * 250
        self.MM = returns_of_stocks.mean() * 250
        self.VM = returns_of_stocks.var() * 250

        self.betas = dict()

        market_variance = returns_of_market.var()
        # calculating betas by analysing daily market data
        for stock, returns in returns_of_stocks.items():
            beta = returns_of_market.cov(returns) / market_variance
            self.betas[stock] = beta

    def plot(self, ax):
        for mean, beta in zip(self.MM, self.betas.items()):
            ax.plot(beta[1], mean, marker='o', label='{}'.format(beta[0]))

        # Add a Legend
        ax.legend(prop={"size": 7})
