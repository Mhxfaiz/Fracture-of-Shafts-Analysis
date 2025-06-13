# goodman_plot.py

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_goodman_plot(Sf, Su, Se, Smean, Sa):
    sns.set(style="whitegrid")
    fig, ax = plt.subplots()

    # Goodman Line
    ax.plot([0, Su], [Se, 0], label="Goodman Line", color='blue')

    # Soderberg Line
    ax.plot([0, Sf], [Su, 0], label="Soderberg Line", color='green', linestyle='--')

    # Gerber Curve
    sigma_m_vals = np.linspace(0, Su, 100)
    gerber_curve = Se * (1 - (sigma_m_vals / UTS)**2)
    ax.plot(sigma_m_vals, gerber_curve, label="Gerber Curve", color='orange', linestyle='-.')

    # User Point
    ax.plot(sigma_m, sigma_a, 'ro', label='User Input Point')

    ax.set_xlabel("Mean Stress σm (MPa)")
    ax.set_ylabel("Alternating Stress σa (MPa)")
    ax.set_title("Fatigue Failure Criteria")
    ax.legend()
    ax.grid(True)
    ax.set_xlim(0, max(UTS, sigma_m) * 1.1)
    ax.set_ylim(0, max(Se, sigma_a) * 1.1)

    return fig
