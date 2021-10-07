#!/usr/bin/env python3

if __name__ == "__main__":
    codes = list(range(10))+list(range(30,48))+list(range(90,97))
    for i in codes:
        print(f"\\033[{i:02}m - \033[{i}mhello\033[0m")
