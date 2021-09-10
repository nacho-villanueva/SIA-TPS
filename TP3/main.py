import json
import sys
from TP3.config import Config


def main():
    config_file = "./config.json"
    if len(sys.argv) >= 2:
        config_file = sys.argv[1]
    else:
        print("Using default config file (./config.json)")

    file = open(config_file)
    config_dict = json.load(file)
    file.close()

    config = Config()
    config.setup_config(config_dict)

    

if __name__ == "__main__":
    main()