# !/usr/bin/python2.7
# -*- coding: utf-8 -*-
# vim: set sts=4 et:
from pyMail import pyMail
import ConfigParser


class mail_dispatcher:
    def __init__(self, conf_local='./pbb.conf'):
        self.conf = conf_local
        cf = ConfigParser.ConfigParser()
        cf.read(self.conf)

        self.m_add = cf.get("bot_mail", "address")
        self.m_psw = cf.get("bot_mail", "psw")
        self.m_imap = cf.get("bot_mail", "imap_service")

    def doit(self):
        rml = pyMail.ReceiveMailDealer(self.m_add, self.m_psw, self.m_imap)
        print rml.getUnread()

        cf = ConfigParser.ConfigParser()
        cf.read(self.conf)
        c_add = cf.get("rule", "address")
        c_nname = cf.get("rule", "nickname")
        c_sub = cf.get("rule", "subject")
        for num in rml.getUnread()[1][0].split(' '):
            if num != '':
                mailInfo = rml.getMailInfo(num)
                nickname = mailInfo['from'][0]
                m_address = mailInfo['from'][1]
                m_subject = mailInfo['subject']
                if nickname == c_nname and m_address == c_add and \
                        m_subject == c_sub:
                    attachment = mailInfo['attachments'][0]
                    fileob = open(attachment['name'], 'wb')
                    fileob.write(attachment['data'])
                    fileob.close()
                    return attachment['name']
        return None
