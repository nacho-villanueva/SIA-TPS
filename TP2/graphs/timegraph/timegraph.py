import matplotlib.pyplot as plt
import json

data_json_file = open("data.json")
data_json = json.load(data_json_file)
data_json_file.close()

bar_names = data_json["bar_names"]
bar_height = []
for bn in bar_names:
    bar_height.append(sum(data_json[bn])/len(data_json[bn]))

plt.rcParams.update({'font.size': 22})
plt.figure("Time graph",figsize=(15,15))
plt.title("Time graph")
plt.ylabel("seg")
plt.bar(bar_names,bar_height)
plt.show()