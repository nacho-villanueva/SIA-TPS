from os import listdir
from os.path import isfile, join

import keras.models
import librosa
import numpy as np
import soundfile

my_path = "./data/stfts"
only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]

X = []

print("loading files...")
for f in only_files:
    D = np.load("./data/stfts/" + f, allow_pickle=True)
    X.append(D)

X = np.array(X)

autoencoder = keras.models.load_model("./results/sound_autoencoder")


def auto_encode(x, name):
    encoded_i = autoencoder.encoder(x).numpy()
    decoded_o = autoencoder.decoder(encoded_i).numpy()

    for i, o in enumerate(decoded_o):
        y_hat = librosa.istft(o) * 10
        soundfile.write(f"./results/sounds/{name}{i}.wav", y_hat, 22050)


# encoded_i = autoencoder.encoder(X).numpy()
# decoded_o = autoencoder.decoder(encoded_i).numpy()
# for i, o in enumerate(decoded_o):
#     y_hat = librosa.istft(o) * 10
#     soundfile.write(f"./results/sounds/test{i}.wav", y_hat, 22050)

shape = [257, 200]


def generate_stfts():
    my_path = "D:\\Users\\ignac\\Downloads\\speech_commands_v0.01\\Combination3"
    only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]

    maxi = 0

    X = []

    print("loading sounds...")
    i = 0
    for f in only_files:
        y, sr = librosa.load(my_path + "\\" + f)

        D = librosa.stft(y, 512)
        D = librosa.util.normalize(D)

        maxi = max(maxi, D.shape[1])

        D0 = np.zeros((D.shape[0], shape[1]))
        D0[:, :D.shape[1]] = D

        X.append(D0)

        D0.dump(f"./data/stfts/{f}.txt")
        i += 1
        if i == 100:
            break

    return np.array(X)


# encoded_i = autoencoder.encoder(generate_stfts()).numpy()
# decoded_o = autoencoder.decoder(encoded_i).numpy()
# for i, o in enumerate(decoded_o):
#     y_hat = librosa.istft(o) * 10
#     soundfile.write(f"./results/sounds/test{i}.wav", y_hat, 22050)

encoded_i1 = autoencoder.encoder(generate_stfts()).numpy()

combinations = []

for i in range(50):
    for j in range(i+1, 51):
        X3 = (encoded_i1[i] + encoded_i1[j]) / 2
        # X4 = (encoded_i1[i] * 2 + encoded_i1[j]) / 3
        # X5 = (encoded_i1[i] + encoded_i1[j] * 2) / 3
        combinations += [X3]

decoded_o1 = autoencoder.decoder(np.array(combinations)).numpy()
for i, o in enumerate(decoded_o1):
    y_hat = librosa.istft(o) * 10
    soundfile.write(f"./results/sounds/new{i}.wav", y_hat, 22050)
