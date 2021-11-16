from os import listdir
from os.path import isfile, join

import librosa
import numpy as np
import tensorflow as tf
from keras import Model
from tensorflow.keras import layers

# my_path = "./data/stfts"
# only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
#
# X = []
#
# for f in only_files:
#     D = np.load("./data/stfts/" + f, allow_pickle=True)
#     X.append(D)
#
# X = np.array(X)

latent_dim = 128
shape = [257, 200]


class Autoencoder(Model):
    def get_config(self):
        return {"latent_dim": self.latent_dim,
                "encoder": self.encoder,
                "decoder": self.decoder}

    def __init__(self):
        super(Autoencoder, self).__init__()
        self.latent_dim = latent_dim
        self.encoder = tf.keras.Sequential([
            layers.Flatten(),
            layers.Dense(latent_dim, activation='relu'),
        ])
        self.decoder = tf.keras.Sequential([
            layers.Dense(shape[0] * shape[1], activation='sigmoid'),
            layers.Reshape((shape[0], shape[1]))
        ])

    def call(self, x, **kwargs):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded


def main():
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

    print(maxi)

    X = np.array(X)

    print("training...")

    autoencoder = Autoencoder()

    autoencoder.compile(optimizer='adam',
                        loss=[tf.losses.MeanSquaredError()])
    autoencoder.fit(X, X, epochs=3500, shuffle=True)

    autoencoder.save("./results/sound_autoencoder")


if __name__ == "__main__":
    main()
