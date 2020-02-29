class Betas:
    def __init__(self, mean_matrix, market_ret, risk_free_return):
        self.MM = mean_matrix
        self.RR = risk_free_return
        self.MR = market_ret

        self.betas = list()

        for mu in self.MM:
            self.betas.append((mu - self.RR) / (self.MR - self.RR))
