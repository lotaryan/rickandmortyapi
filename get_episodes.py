import json
from datetime import datetime
import os


def get_episodes_between_2017_2021():
    episodes = []
    for i in range(1, len(os.listdir("episode"))):
        with open(f"episode/{i}.json", "r") as outfile:
            episode_data = json.load(outfile)
            episode_air_year = datetime.strptime(episode_data["RawData"]["air_date"], '%B %d, %Y').year
            if episode_air_year == 2017 or episode_air_year == 2021:
                if len(episode_data["RawData"]["characters"]) > 3:
                    episodes.append(episode_data["Metadata"])
            elif episode_air_year < 2017:
                continue
            elif episode_air_year > 2021:
                break
    return episodes


if __name__ == "__main__":
    print(get_episodes_between_2017_2021())
