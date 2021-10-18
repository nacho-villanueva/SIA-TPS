import matplotlib.pyplot as plt

countries = ["Austria", "Belgium", "Bulgaria", "Croatia", "Czech Republic", "Denmark", "Estonia", "Finland", "Germany",
             "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Netherlands", "Norway",
             "Poland", "Portugal", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom"]

YPC1 = [-1.08175, -0.68109, 2.60988, 1.27015, -0.16721, -0.95519, 2.48774, -0.21056, -0.59239, 1.00047, 1.39690,
        -1.58372, -1.80892, -0.85322, 2.30606, 1.53010, -3.47843, -1.84005, -2.10651, 1.47177, 0.52649, 0.78297,
        0.06754, -0.16377, -0.88511, -3.28159, 4.58027, -0.34082]
YPC2 = [-1.27005, -0.41604, 0.26964, 1.90143, -0.13194, -0.40963, -0.08578, -0.03372, -0.47183, 3.40685, -0.03423,
        -1.47726, 0.52181, 0.32780, -0.67535, -0.19500, -1.07629, -0.05723, -0.14396, 0.07299, 1.03477, -0.17226,
        0.79767, 1.15207, -0.40288, -0.10823, -2.82904, 0.50570]

PC1 = [[0, 0.12487],
       [0, -0.50051],
       [0, 0.40652],
       [0, -0.48287],
       [0, 0.18811],
       [0, -0.47570],
       [0, 0.27166]]

PC2 = [[0, -0.17287],
       [0, -0.13014],
       [0, -0.36966],
       [0, 0.26525],
       [0, 0.65827],
       [0, 0.08262],
       [0, 0.55320]]

labels = [
    "Area",
    "GDP",
    "Inflation",
    "Life Expectancy",
    "Military",
    "Population Growth",
    "Unemployment"

]

for i in range(len(PC1)):
    plt.plot(PC1[i], PC2[i], label=labels[i])
    plt.scatter(YPC1, YPC2)
    # plt.text(PC1[i][1], PC2[i][1], labels[i])

for i, txt in enumerate(countries):
    plt.annotate(txt, (YPC1[i]-0.15, YPC2[i]+0.1))

plt.legend()
plt.xlabel("PC1")
plt.ylabel("PC2")

plt.show()


