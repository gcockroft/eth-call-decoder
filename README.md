# eth_call_decoder
A tool for bulk decoding the function signature of `eth_call` requests through hexcode signature lookups in the [Ethereum Signature Database](https://www.4byte.directory/). 

## Usage
The tool parses out the `data` field from a raw CSV file containing the JSON of *all* `eth_call` request data. Example input line:
```javascript
{
    ""method"":""eth_call"",
    ""params"": [
        {
            ""to"":""0x00000000000000000..."",
            ""data"":""0x70a08231000000000...""
        },
        ""latest""
    ],
    ""id"":43,
    ""jsonrpc"":
    ""2.0""
}
```

1. Activate `venv` with `source venv/bin/activate`
2. Put raw data files in `/raw_data`.
3. `cd` into `src`.
4. Provide the filename(s) to decode as command line arguments, 1 or more files e.g. `python3 main.py <RAW_FILENAME.csv>`.

### Result
Two files will appear in `/decoded_data`.
1. `decoded_<FILENAME>`, a csv file in the format \(hexcode,function signature\).
2. `counts_<FILENAME>`, a csv file in the format \(# of occurences,function signature\).

**Notes:**
- 
- Data is parsed out as the first 8 characters succeeding the raw string the regular expression `(?<=data)(.*)0x`.
- Some lines are malformed so `line.json()["data"]` did not work.