# -*- coding: utf-8 -*-
'''
@since: 30.04.2012

@author: moschlar
'''
#
## SAUCE - System for AUtomated Code Evaluation
## Copyright (C) 2013 Moritz Schlarb
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU Affero General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Affero General Public License for more details.
##
## You should have received a copy of the GNU Affero General Public License
## along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import logging

from smtplib import SMTP, SMTP_SSL
from email.mime.text import MIMEText

from tg import config
from paste.deploy.converters import asbool

log = logging.getLogger(__name__)


def sendmail(to_addrs, subject, text):  # pragma: no cover

    server = config.get('smtp_server')
    use_tls = asbool(config.get('smtp_use_tls'))
    username = config.get('smtp_username')
    password = config.get('smtp_password')
    from_addr = config.get('admin_email_from')

    log.debug('Sending mail via %s', server)

    if use_tls:
        s = SMTP_SSL()
    else:
        s = SMTP()
    s.connect(server)
    if username:
        s.login(username, password)
    msg = MIMEText(text, _charset='utf-8')
    msg['From'] = from_addr
    msg['Reply-To'] = from_addr
    if isinstance(to_addrs, basestring):
        msg['To'] = to_addrs
    else:
        msg['To'] = ', '.join(to_addrs)
    msg['Subject'] = subject
    s.sendmail(from_addr, to_addrs, msg.as_string())
    s.quit()


def main():  # pragma: no cover
    subject = u'Huhu'
    text = u'This is SPÄRTA'
    sendmail(to_addrs=['Testor <test@test.de>', ], subject=subject, text=text)

if __name__ == '__main__':  # pragma: no cover
    main()
