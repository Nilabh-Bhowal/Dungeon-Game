import PyInstaller.__main__
import shutil
import os
import subprocess

v = input("Enter the version: ")
subprocess.call("pyinstaller main.py -F -w --clean -p ./assets/scripts")
if os.path.isdir(f"./builds/{v}"):
    shutil.rmtree(f"./builds/{v}", ignore_errors=True)
os.mkdir(f"./builds/{v}")
shutil.copytree("./assets", f"./builds/{v}/assets")
shutil.move("./dist/main.exe", f"./builds/{v}")
shutil.rmtree("./build", ignore_errors=True)
shutil.rmtree("./dist", ignore_errors=True)
shutil.rmtree(f"./builds/{v}/assets/scripts", ignore_errors=True)
