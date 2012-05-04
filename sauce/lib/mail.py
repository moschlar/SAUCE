# -*- coding: utf-8 -*-
'''
Created on 30.04.2012

@author: moschlar
'''

import logging

from smtplib import SMTP, SMTP_SSL
from email.mime.text import MIMEText

from tg import config
from paste.deploy.converters import asbool

log = logging.getLogger(__name__)

def sendmail(to_addrs, subject, text):
    
    server = config.get('smtp_server')
    use_tls = asbool(config.get('smtp_use_tls'))
    username = config.get('smtp_username')
    password = config.get('smtp_password')
    from_addr = config.get('admin_email_from')
    
    log.debug('Sending mail via %s' % server)

    if use_tls:
        s = SMTP_SSL()
    else:
        s = SMTP()
    s.connect(server)
    s.login(username, password)
    msg = MIMEText(text, _charset='utf-8')
    msg['From'] = from_addr
    if isinstance(to_addrs, basestring):
        msg['To'] = to_addrs
    else:
        msg['To'] = ', '.join(to_addrs)
    msg['Subject'] = subject
    s.sendmail(from_addr, to_addrs, msg.as_string())
    s.quit()

def main():
    subject = u'Huhu'
    text = u'This is SPÄRTA'
    sendmail(to_addrs=['Moritz Schlarb <moschlar@students.uni-mainz.de>', ], subject=subject, text=text)
    
if __name__ == '__main__':
    main()
