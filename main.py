#!/usr/bin/python2.7
# vim: set sts=4 et:
# coding=utf-8

import sys
import parser
import mail_dispatcher


def main():
    mm = mail_dispatcher.mail_dispatcher("./pbb.conf")
    atta = mm.doit()
    if atta:
        atta = parser.icbc_Ecard(atta)
        mm.sendit(atta)
    sys.exit(0)


if __name__ == "__main__":
    main()
