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

1. Put raw data files in `/raw_data`.
2. Provide the filename(s) to decode as command line arguments, 1 or more files.
3. Decoded CSV files will appear in `/decoded_data` as `decoded_<RAW_FILENAME>` in the format "hex_signature,function_signature".

**Notes:**
- Data is parsed out as the first 10 characters succeeding the raw string `""data"":""`.
- The decoder sleeps repeatedly to avoid 429 errors, increasing runtime.