import matplotlib.pyplot as plt

winrates3 = [66.666, 39.333, 48.6666, 52.0, 64.0, 75.333, 44.0, 50.666, 31.3333, 60.0]

ax.set_title(r'Winrate des versions avec le filtre 4x4 contre le filtre 5x5')
ax.set_ylabel('Winrate')
ax.set_xlabel('Numéro de version')


ax.bar(np.arange(0, 10), height=winrates3)
plt.show()
