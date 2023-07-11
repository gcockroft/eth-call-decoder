import requests
import time

def main():
    # Open file. 
    f = open("../raw_data/Test API Logs_2023-07-06_23_15_00_2023-07-07_00_15_00_filters-2_by_request.csv", "r")

    # Read past header line.
    print(f.readline())
    i = 0
    while True:
        # Get data
        line = f.readline()
        if not line:
            break
        hexcode = line.split('""data"":""')[1][:10]
        i += 1 
        # Get function signature with API
        url =  'https://www.4byte.directory/api/v1/signatures/?hex_signature=' + hexcode
        try:
            response = requests.get(url)
            # Sleep to avoid raising 429s
            if response.status_code == 429:
                time.sleep(int(response.headers['Retry-After']))
                response = requests.get(url)

            json = response.json()
            print(json['results'][0]['text_signature'])
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            if response.status_code == 404:
                print("404 Hex signature not found")
            else:
                print(str(errh))
        except requests.exceptions.C:
            print("Unknown error")

if __name__ == "__main__":
    main()