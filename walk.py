import os
from os.path import join, getsize

for root, dirs, files in os.walk('./test_folder_0'):
    print(root, "consumes", end=" ")
    print(sum(getsize(join(root, name)) for name in files), end=" ")
    print("bytes in", len(files), "non-directory files", end=" ")
    for name in files:
        print(join(root, name), end=" ")
    print("")
