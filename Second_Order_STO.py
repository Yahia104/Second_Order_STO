import requests
import re
import sys

if len(sys.argv) < 3:
    print("Usage: python3 script.py input.txt output.txt")
    sys.exit(1)

inputfile = sys.argv[1]
outputfile = sys.argv[2]

regex = r"https?://[^\s\"'>]+"

with open(inputfile, "r") as inputurl, open(outputfile, "a") as outputurl:
    for line in inputurl:
        url = line.strip()
        if not url:
            continue
        if not url.startswith(("http://", "https://")):
            url = f"http://{url}"

        print("parsing in : " + url)
        print("#" * 40)

        try:
            res = requests.get(url, timeout=3)
            keys = set(re.findall(regex, res.text))

            if keys:
                for key in keys:
                    try:
                        res2 = requests.get(key, timeout=2)
                        print(f"{key} : {res2.status_code}")
                    except requests.exceptions.RequestException:
                        print("check this manually : " + key)
                        outputurl.write("check this manually : "+ key + "\n")
                        outputurl.write(f"links belong to : {url}\n")
                        outputurl.write("#" * 40 + "\n")
        except :
            print("url is not reached")
