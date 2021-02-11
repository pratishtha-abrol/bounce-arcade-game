import global_var 
import global_func
import os

if (os.name == "posix"):
    os.system("clear")
else:
    os.system("cls")
global_func.print_board()