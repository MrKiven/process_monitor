# -*- coding: utf-8 -*-


def check_isDigit(filed_str):
    strList=filed_str.split('.')
    if len(strList) == 1:
        if strList[0].isdigit():
            return 1
        else:
            print "%s is not a  numeric." % filed_str
            return 0
    elif len(strList) == 2:
        if strList[0].isdigit() and strList[1].isdigit():
            return 1
        else:
            print "%s is not a  numeric." % filed_str
            return 0
    else:
        print "%s is not a  numeric." % filed_str
        return 0
