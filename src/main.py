import requests
import sys
import time
import re
from tqdm import tqdm

def decode(filename, cache):
    num_lines = sum(1 for _ in open("../raw_data/" + filename))
    fr = open("../raw_data/" + filename, "r")
    fw = open("../decoded_data/decoded_" + filename, "w")
    fw.write('hex_signature,text_signature\n')

    # Read past header line. Init empty cache.
    fr.readline()
    counts = {}

    for i in tqdm(range(num_lines - 1)):
        # Get hexcode to decode.
        line = fr.readline()
        if not line:
            break

        # Regex for line splitting after data, slower.
        hexcode = re.split(r'(?<=data)(.*)0x', line)[2][:8]
        text_signature = None
        # Raw line splitting.
        # hexcode = line.split('""data"":""')[1][:10]

        if hexcode in cache.keys():
            text_signature = cache[hexcode]
            counts[cache[hexcode]] = 0 if text_signature not in counts else counts[text_signature] + 1
        else:
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

                # Save hex -> text mapping and initialize count.
                cache[hexcode] = text_signature
                counts[text_signature] = 1
                
                response.raise_for_status()
            # Handle errors.
            except requests.exceptions.HTTPError as err:
                if response.status_code == 404:
                    print("404 Hex signature not found")
                else:
                    print(str(err))
            except requests.exceptions.ConnectionError as err:
                print("Connection error.")
            except Exception as err:
                print(f"Unknown error occured {err=}, {type(err)=}")

        # Write hexcode -> function signature to csv.
        fw.write(hexcode + ',' + text_signature + '\n')

    return counts

def write_counts(counts, filename):
    fw = open("../decoded_data/counts_" + filename, "w")
    fw.write('calls,function\n')

    for fn in counts:
        count = counts[fn]
        fw.write(str(count) + ',' + fn + '\n')

def main():
    # Handle no filename given.
    if len(sys.argv) == 1:
        print("Please provide filename(s) as command line arguments.")
        return
    print('Decoding: ' + str(sys.argv[1:])) 

    cache = {}
    for i in range(1,len(sys.argv)):
        filename = sys.argv[i]

        # Decode, write counts and decodings to two different files.
        counts = decode(filename, cache)
        write_counts(counts, filename)

    return 

if __name__ == "__main__":
    main()