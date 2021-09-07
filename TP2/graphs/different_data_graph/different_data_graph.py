import matplotlib.pyplot as plt
import os

def list_dir_and_join(path):
    return [os.path.join(path,d) for d in os.listdir(path)]

def main():
    CURRENT_SCRIPT_FILEPATH = os.path.dirname(os.path.realpath(__file__))
    DATA_DIR = os.path.join(CURRENT_SCRIPT_FILEPATH,"data")

    data_dirs = [d for d in list_dir_and_join(DATA_DIR) if os.path.isdir(d)]
    data = {}

    for d in data_dirs:
        name = os.path.basename(d)
        data[name] = {
            "gen":[],
            "min_fitness":[],
            "max_fitness":[],
            "avg_fitness":[],
            "diversity":[]
        }
        folder_data = []
        for p in list_dir_and_join(d):
            f = open(p)
            headers = f.readline().strip().split(";")
            lines = f.readlines()
            for j in range(len(lines)):
                lines[j] = lines[j].strip().split(";")
                lines[j][0] = int(lines[j][0])
                lines[j][1] = float(lines[j][1])
                lines[j][2] = float(lines[j][2])
                lines[j][3] = float(lines[j][3])
                lines[j][4] = float(lines[j][4])
            folder_data.append(lines)
            f.close()
        for i in range(len(folder_data[0])):
            data[name]["gen"].append(0)
            data[name]["min_fitness"].append(0)
            data[name]["max_fitness"].append(0)
            data[name]["avg_fitness"].append(0)
            data[name]["diversity"].append(0)
            for j in range(len(folder_data)):
                data[name]["gen"][i] = folder_data[j][i][0]
                data[name]["min_fitness"][i] += folder_data[j][i][1]
                data[name]["max_fitness"][i] += folder_data[j][i][2]
                data[name]["avg_fitness"][i] += folder_data[j][i][3]
                data[name]["diversity"][i] += folder_data[j][i][4]
            data[name]["min_fitness"][i] /= len(folder_data)
            data[name]["max_fitness"][i] /= len(folder_data)
            data[name]["avg_fitness"][i] /= len(folder_data)
            data[name]["diversity"][i] /= len(folder_data)

    plt.rcParams.update({'font.size': 22})

    plt.figure("Min fitness",figsize=(15,15))
    plt.title("Min fitness")
    for name in data.keys():
        plt.plot(data[name]["gen"],data[name]["min_fitness"],label=name)
    plt.legend()

    plt.figure("Max fitness",figsize=(15,15))
    plt.title("Max fitness")
    for name in data.keys():
        plt.plot(data[name]["gen"],data[name]["max_fitness"],label=name)
    plt.legend()

    plt.figure("Avg fitness",figsize=(15,15))
    plt.title("Avg fitness")
    for name in data.keys():
        plt.plot(data[name]["gen"],data[name]["avg_fitness"],label=name)
    plt.legend()

    plt.figure("Diversity",figsize=(15,15))
    plt.title("Diversity")
    for name in data.keys():
        plt.plot(data[name]["gen"],data[name]["diversity"],label=name)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()