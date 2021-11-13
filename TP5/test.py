# f = open("./data/letters.txt")
# fp = open("./data/parsed_letters.txt", "w")
# lines = f.readlines()
#
# for l in lines:
#     char = l.split(",")
#     for c in char:
#         binary = bin(int(c, 16)).zfill(8)
#         fp.write("{0:05b}".format(int(c, 16)))
#         fp.write("\n")
#     fp.write("\n")
import matplotlib.pyplot as plt

f = open("./results/error.txt")
errors = f.readlines()
errors = [float(x) for x in errors]

plt.plot(errors)
plt.show()