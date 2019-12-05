from cx_Freeze import setup, Executable

base = None    

executables = [Executable("RMA TESING.py", base=base)]

packages = ["idna", "pandas", "datetime","openpyxl", "xlrd"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "RmaTesting",
    options = options,
    version = "0.2",
    description = 'RMA TESING',
    executables = executables
)