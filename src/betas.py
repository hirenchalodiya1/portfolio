class Betas:
    def __init__(self, returns_of_stocks, returns_of_market, market_ret, risk_free_return, mean_matrix):
        self.MM = mean_matrix
        self.RR = risk_free_return
        self.MR = market_ret

        self.betas = dict()

        market_variance = returns_of_market.var()
        
        # calculating betas by analysing daily market data
        for stock, returns in returns_of_stocks.items():
            beta = returns_of_market.cov(returns)/market_variance
            self.betas[stock] = beta

        # SML line
        sml_slope = (self.MR - self.RR) / (1 - 0)
        self._min_beta = min(0, min(self.betas.values()))
        self._max_beta = max(1, max(self.betas.values()))
        self.line_sml = lambda x: self.RR + sml_slope * x

    def plot(self, ax):
        # x axis
        ax.axhline(color='#000000')

        # y axis
        ax.axvline(color='#000000')

        # Add risk free point
        ax.plot(0, self.RR, label='Risk free point', marker='o')

        # Complete market point
        ax.plot(1, self.MR, label='Market point', marker='o')

        # SML Line
        ax.plot([self._min_beta, self._max_beta], [self.line_sml(self._min_beta), self.line_sml(self._max_beta)], label='SML')
        
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