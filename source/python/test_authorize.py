# -*- coding: utf-8 -*-

import sys
import warnings

sys.dont_write_bytecode = True
warnings.filterwarnings('ignore')

from authorize import Authorize


def main():
    test1()
    return

def test1():

    a: Authorize = Authorize("127.0.0.1", 5432, "dbportal", "pusr", "pppp")
    v1 = a.get_magic_number("admin")
    print(v1)

    return

if __name__ == '__main__':
    main()
