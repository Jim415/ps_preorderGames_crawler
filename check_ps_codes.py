import requests

country_codes = [
    "ar-ae", "ar-bh", "ar-kw", "ar-lb", "ar-om", "ar-qa", "ar-sa", "bg-bg", "cs-cz", "da-dk", "de-at", "de-ch", "de-de",
    "el-gr", "en-ae", "en-au", "en-bh", "en-bg", "en-ca", "en-cy", "en-cz", "en-dk", "en-fi", "en-gb", "en-gr", "en-hk",
    "en-hr", "en-hu", "en-id", "en-ie", "en-il", "en-in", "en-is", "en-kw", "en-lb", "en-mt", "en-my", "en-nz", "en-no",
    "en-om", "en-ph", "en-pl", "en-qa", "en-ro", "en-sa", "en-se", "en-sg", "en-si", "en-sk", "en-th", "en-tr", "en-tw",
    "en-us", "en-vn", "en-za", "es-ar", "es-bo", "es-cl", "es-co", "es-cr", "es-ec", "es-es", "es-gt", "es-hn", "es-mx",
    "es-ni", "es-pa", "es-pe", "es-py", "es-sv", "es-uy", "fi-fi", "fr-be", "fr-ca", "fr-ch", "fr-fr", "fr-lu", "he-il",
    "hr-hr", "hu-hu", "it-ch", "it-it", "ja-jp", "ko-kr", "nb-no", "nl-be", "nl-nl", "pl-pl", "pt-br", "pt-pt", "ro-ro",
    "ru-ru", "sk-sk", "sl-si", "sr-rs", "sv-se", "th-th", "tr-tr", "uk-ua", "zh-hans-cn", "zh-hans-hk", "zh-hant-hk", "zh-hant-tw"
]

# country_codes = [
#     "zh-hans-hk", "zh-hant-hk", "en-us", "en-hk"
# ]

base_url = "https://store.playstation.com/en-hk/category/3bf499d7-7acf-4931-97dd-2667494ee2c9/1/"

valid_codes = []

for code in country_codes:
    url = base_url.replace("en-hk", code)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"VALID: {code} -> {url}")
            valid_codes.append(code)
        else:
            print(f"INVALID: {code} -> {url} (Status: {response.status_code})")
    except Exception as e:
        print(f"ERROR: {code} -> {url} ({e})")

print("\nValid codes:")
print(valid_codes)
print(len(valid_codes))

