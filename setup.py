import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(name="Image Checker",
      version="0.0.1",
      author="Patrick Liem",
      author_email="hszer0@gmail.com",
      executables=[Executable("ImageChecker.py", base=base, shortcutName="Image Checker", shortcutDir="DesktopFolder")]
      )
