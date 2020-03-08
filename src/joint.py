from matplotlib.patches import ConnectionPatch

def capm_and_betas(marko, capm, betas, ax1, ax2):
    marko.plot(ax1, individual=True)
    capm.plot(ax1)
    betas.plot(ax2)
    ax1.legend(prop={"size": 7}, loc=1)
    ax2.legend(prop={"size": 7}, loc=1)

    n = marko.n

    for i, mean, variance, beta in zip(range(n), marko.MM, marko.CM, betas.betas.values()):
        y1 = y2 = mean
        x1 = variance[i]
        x2 = beta

        con = ConnectionPatch(xyA=(x1, y1), xyB=(x2, y2), coordsA="data", coordsB="data",
                            axesA=ax1, axesB=ax2, color="red", linestyle='--')
        ax2.add_artist(con)
