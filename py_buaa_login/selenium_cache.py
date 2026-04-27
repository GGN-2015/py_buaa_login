import os
from typing import Optional

CACHE_ROOT = os.path.join(
    os.path.expanduser("~"), ".cache", "selenium")

def listdir(filepath:str) -> list[str]:
    if not os.path.isabs(filepath):
        filepath = os.path.abspath(filepath)

    if os.path.isfile(filepath):
        return [filepath]
    
    if os.path.isdir(filepath):
        arr = []
        for filename in os.listdir(filepath):
            arr += listdir(os.path.join(filepath, filename))
        return arr
    
    return []

def find_cached_chromedrive() -> Optional[str]:
    for filepath in listdir(CACHE_ROOT):
        if filepath.endswith("chromedriver.exe"):
            return filepath
    return None

if __name__ == "__main__":
    print(find_cached_chromedrive())
