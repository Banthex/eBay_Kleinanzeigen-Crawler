# eBay_Kleinanzeigen-Crawler

```
pip3 install -r requirements.txt
py .\src\Main.py
```


## Args
 ```
 usage: Main.py [-h] --url URL [--output_json OUTPUT_JSON] [--json_pref JSON_PREF] [--output_folder OUTPUT_FOLDER]
               [--proxy PROXY] [--sleep SLEEP]

Website monitor

options:
  -h, --help            show this help message and exit
  --url URL             Website which will be monitored (default: None)
  --output_json OUTPUT_JSON
                        Results to json (default: 0)
  --json_pref JSON_PREF
                        File prefix (default: )
  --output_folder OUTPUT_FOLDER
                        File folder (default: data/)
  --proxy PROXY         Use proxy (default: 0)
  --sleep SLEEP         Time (secs) between requests (default: 15)
  ```