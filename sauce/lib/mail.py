# -*- coding: utf-8 -*-
'''
@since: 22.10.2014
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

from email.mime.text import MIMEText

from repoze.sendmail.delivery import DirectMailDelivery
from repoze.sendmail.mailer import SMTPMailer, SendmailMailer

from tg import config
from paste.deploy.converters import asbool

import logging
log = logging.getLogger(__name__)


__all__ = ['sendmail']


class DummyDelivery(object):
    '''Dummy mail delivery object for the test suite'''
    mailbox = []

    def send(self, fromaddr=None, toaddrs=None, message=None):
        log.debug(message)
        self.mailbox.append(message)

    def flush_mailbox(self):
        try:
            while True:
                self.mailbox.pop()
        except IndexError:
            return

    def assert_contains(self, subject=None, body=None):
        '''Assert that there was at least one mail sent that matches subject and/or body'''
        if not self.mailbox:
            raise AssertionError('No Mail sent at all')
        else:
            for mail in reversed(self.mailbox):
                if subject and subject in mail.get('Subject', ''):
                    return
                if body and body in mail.get_payload(decode=True):
                    return
            raise AssertionError('No Mail in mailbox contained subject or body')


def _make_message(from_addr, to_addrs, subject, body, charset='utf-8'):
    msg = MIMEText(body, _charset=charset)
    msg['From'] = msg['Reply-To'] = from_addr
    msg['To'] = ', '.join(to_addrs)
    msg['Subject'] = subject
    return msg


class Sendmail(object):

    def __init__(self):
        '''
        :ivar to_addr: The default recipient email address
            Will be set to the configuration variable "email_to",
            if configuration is available
        :ivar from_addr: The default sender email address
            Will be set to the configuration variable "admin_email_from",
            if configuration is available
        '''

        self.to_addr = config.get('email_to')
        self.from_addr = config.get('admin_email_from')

        smtp_server = config.get('smtp_server')
        smtp_use_tls = asbool(config.get('smtp_use_tls'))
        smtp_username = config.get('smtp_username')
        smtp_password = config.get('smtp_password')

        test = asbool(config.get('test'))

        if test:
            log.debug('Using DummyDelivery()')
            self.delivery = DummyDelivery()
        else:  # pragma: no cover
            if smtp_server:
                mailer = SMTPMailer(hostname=smtp_server,
                    username=smtp_username, password=smtp_password,
                    force_tls=smtp_use_tls)
                log.debug('Using SMTPMailer(hostname=%s, ...)', smtp_server)
            else:
                mailer = SendmailMailer()
                log.debug('Using SendmailMailer()')
            self.delivery = DirectMailDelivery(mailer)

    def __call__(self, subject, body, to_addrs=None, from_addr=None):
        '''
        :param subject:
        :param body:
        :param to_addrs: List of recipient email addresses
            If to_addrs is None, the default to_addr will be used.
            Additionally, if to_addrs is a list and contains None as an item,
            that item will also be replaced by the default to_addr.
            (see :py:attr:`Sendmail.to_addr`)
        :param from_addr: Sender email address
            If from_addr is None, the default from_addr will be used.
            (see :py:attr:`Sendmail.from_addr`)
        '''

        if to_addrs is None:
            to_addrs = [self.to_addr]
        elif isinstance(to_addrs, basestring):
            to_addrs = [to_addrs]
        else:
            to_addrs = set(to_addrs)  #: :type to_addrs: set
            try:
                to_addrs.remove(None)
            except KeyError:
                pass
            else:
                to_addrs.add(self.to_addr)

        if from_addr is None:
            from_addr = self.from_addr

        # Make human-readable message for logging
        _msg = _make_message(from_addr, to_addrs, subject, body, charset=None)
        log.debug(_msg.as_string())

        msg = _make_message(from_addr, to_addrs, subject, body)
        msgid = self.delivery.send(from_addr, to_addrs, msg)

        return msgid


sendmail = Sendmail()


if __name__ == '__main__':  # pragma: no cover
    import transaction
    with transaction.manager:
        print sendmail(u'Subject', u'Body', 'moschlar@metalabs.de', 'moschlar@metalabs.de')
