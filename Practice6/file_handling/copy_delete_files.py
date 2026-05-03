import shutil
import os

shutil.copy("test.txt", "copy.txt")

if os.path.exists("copy.txt"):
    os.remove("copy.txt")
