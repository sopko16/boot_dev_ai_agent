from functions.run_python_file import run_python_file


def main():
    
    print("main.py:")
    print(run_python_file("calculator", "main.py")) # (should print the calculator's usage instructions)
    print()
    print("main.py with args:")
    print(run_python_file("calculator", "main.py", ["3 + 5"])) # (should run the calculator... which gives a kinda nasty rendered result)
    print()
    print("run calculator tests:")
    print(run_python_file("calculator", "tests.py")) # (should run the calculator's tests successfully)
    print("error #1:")
    print(run_python_file("calculator", "../main.py")) # (this should return an error)
    print()
    print("error #2:")
    print(run_python_file("calculator", "nonexistent.py")) # (this should return an error)
    print()
    print("error #3:")
    print(run_python_file("calculator", "lorem.txt")) # (this should return an error)
    print()


if __name__ == "__main__":
    main()