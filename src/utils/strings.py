from typing import List


def joinNatural(*args: str):
    # if not len(args):
    #     return ""
    # elif len(args) == 1:
    #     return 
    # print(args)
    match len(args):
        case 0: return ""
        case 1: return args[0]
        case 2: return args[0] + " and " + args[1]
        case _:
            s = args[0]
            for i in args[1 :-1]:
                s += ", " + i
            return s + ", and " + args[-1]
