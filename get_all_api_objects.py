import requests
import uuid
import json
import os
import threading


class BackgroundWrite(threading.Thread):

    def __init__(self, data, filename):
        self.data = data
        self.filename = filename
        threading.Thread.__init__(self)


    def run(self):
        with open(f"{self.filename}", "w") as outfile:
            json.dump(self.data, outfile)

        print("Finished background file write to",
              self.filename)


class RickandMortyGetObjects:
    main_url = "https://rickandmortyapi.com/api"

    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.data = []
        self.lock = threading.Lock()

    def get_data(self):
        print(f"Retrieving data for endpoint: {self.endpoint}")
        data = []
        current_page = 1
        is_next = True
        # self.lock.acquire()

        def get_one_page():
            nonlocal current_page
            nonlocal data
            response = requests.get(f'{self.main_url}/{self.endpoint}/?page={current_page}')
            if response.status_code == 200:
                response_json = response.json()
                data += response_json["results"]
                current_page += 1
                return response_json["info"]["next"]
            else:
                raise Exception("Connection error with api")

        while is_next:
            print(f"here {self.endpoint}")
            is_next = get_one_page()

        self.data = data
        print(f"Done with {self.endpoint}")
        self.lock.release()

    def create_json_files(self):
        self.lock.acquire()
        if not os.path.exists(self.endpoint):
            os.makedirs(self.endpoint)
        for data_entry in self.data:
            json_data = {"Id": str(uuid.uuid4()),
                         "Metadata": data_entry["name"],
                         "RawData": data_entry}
            background = BackgroundWrite(json_data, f"{self.endpoint}/{data_entry['id']}.json")
            background.start()
        self.lock.release()


def get_all_data_for_all_objects():
    character = RickandMortyGetObjects("character")
    t_1 = threading.Thread(target=character.get_data)
    t_1.start()

    location = RickandMortyGetObjects("location")
    t_2 = threading.Thread(target=location.get_data)
    t_2.start()

    episode = RickandMortyGetObjects("episode")
    t_3 = threading.Thread(target=episode.get_data)
    t_3.start()
    print("Done with data retrieval: skipping to writing data to json files.")

    t_1_1 = threading.Thread(target=character.create_json_files)
    t_1_1.start()
    t_2_1 = threading.Thread(target=location.create_json_files)
    t_2_1.start()
    t_3_1 = threading.Thread(target=episode.create_json_files)
    t_3_1.start()

    t_1.join()
    t_2.join()
    t_3.join()
    t_1_1.join()
    t_2_1.join()
    t_3_1.join()


if __name__ == "__main__":
    get_all_data_for_all_objects()

