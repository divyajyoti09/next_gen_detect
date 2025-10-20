import time
from tqdm import tqdm

for i in tqdm(range(10)):
    for j in tqdm(range(10), leave=False):
        time.sleep(0.1)
