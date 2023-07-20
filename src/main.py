import requests
import sys
import time
from tqdm import tqdm

def decode(filename):
    num_lines = sum(1 for _ in open("../raw_data/" + filename))
    fr = open("../raw_data/" + filename, "r")
    fw = open("../decoded_data/decoded_" + filename, "w")
    fw.write('hex_signature,text_signature\n')

    # Read past header line.
    fr.readline()

    for i in tqdm(range(num_lines - 1)):
        # Get hexcode to decode.
        line = fr.readline()
        if not line:
            break
        hexcode = line.split('""data"":""')[1][:10]

        # Get function signature with API
        url =  'https://www.4byte.directory/api/v1/signatures/?hex_signature=' + hexcode
        try:
            response = requests.get(url)
            # Sleep to avoid raising 429s
            if response.status_code == 429:
                time.sleep(int(response.headers['Retry-After']))
                response = requests.get(url)

            # Handle and write response
            json = response.json()
            text_signature = json['results'][0]['text_signature']
            fw.write(hexcode + ',' + text_signature + '\n')
            response.raise_for_status()

        except requests.exceptions.HTTPError as err:
            if response.status_code == 404:
                print("404 Hex signature not found")
            else:
                print(str(err))
        except requests.exceptions.ConnectionError as err:
            print("Connection error.")
        except Exception as err:
            print(f"Unknown error occured {err=}, {type(err)=}")

    return

def main():
    # Handle no filename given.
    if len(sys.argv) == 1:
        print("Please provide filename(s) as command line arguments.")
        return
    print(str(sys.argv)) 
    for i in range(1,len(sys.argv)):
        decode(sys.argv[1])
    return 

if __name__ == "__main__":
    main()