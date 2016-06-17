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

from repoze.sendmail.delivery import DirectMailDelivery, QueuedMailDelivery
from repoze.sendmail.mailer import SMTPMailer, SendmailMailer

from tg import config
from paste.deploy.converters import asbool

from sauce.model import User, Group, Permission

import logging
log = logging.getLogger(__name__)


__all__ = ['sendmail']


def _make_message(from_addr, to_addrs, subject, body, charset='utf-8', cc_addrs=None, bcc_addrs=None):  # pylint:disable=too-many-arguments
    msg = MIMEText(body, _charset=charset)
    msg['From'] = msg['Reply-To'] = from_addr
    msg['To'] = ', '.join(to_addrs)
    if cc_addrs:
        msg['Cc'] = ', '.join(cc_addrs)
    if bcc_addrs:
        msg['Bcc'] = ', '.join(bcc_addrs)
    msg['Subject'] = subject
    return msg


def sendmail(subject, body, to_addrs=None, from_addr=None, cc_managers=False):
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
    :param cc_managers: Whether to Cc the email to all managers
    '''

    default_to_addr = config.get('email_to')
    default_from_addr = config.get('admin_email_from', 'sauce@localhost')

    smtp_server = config.get('smtp_server')
    smtp_use_tls = asbool(config.get('smtp_use_tls'))
    smtp_username = config.get('smtp_username')
    smtp_password = config.get('smtp_password')

    delivery_queue = config.get('mail.delivery_queue', False)
    try:
        delivery_queue = asbool(delivery_queue)
    except ValueError:
        pass

    if not delivery_queue:  # pragma: no cover
        if smtp_server:
            mailer = SMTPMailer(hostname=smtp_server,
                username=smtp_username, password=smtp_password,
                force_tls=smtp_use_tls)
            log.debug('delivery = DirectMailDelivery(SMTPMailer(hostname=%s, ...))', smtp_server)
        else:
            mailer = SendmailMailer()
            log.debug('delivery = DirectMailDelivery(SendmailMailer())')
        delivery = DirectMailDelivery(mailer)
    else:
        log.debug('delivery = QueuedMailDelivery("%s")', delivery_queue)
        delivery = QueuedMailDelivery(delivery_queue)

    to_addrs = to_addrs or default_to_addr or []
    to_addrs = set([to_addrs] if isinstance(to_addrs, basestring) else to_addrs)

    try:
        to_addrs.remove(None)
    except KeyError:
        pass
    else:
        to_addrs.add(default_to_addr)

    from_addr = from_addr or default_from_addr

    cc_addrs = None
    if cc_managers:
        cc_addrs = []
        for manager in User.query.join(User.groups).join(Group.permissions).filter_by(permission_name='manage'):
            cc_addrs.append(manager.email_address)

    # Make human-readable message for logging
    _msg = _make_message(from_addr, to_addrs, subject, body, charset=None, cc_addrs=cc_addrs)
    log.debug(_msg.as_string())

    if to_addrs:
        msg = _make_message(from_addr, to_addrs, subject, body, cc_addrs=cc_addrs)
        msgid = delivery.send(from_addr, to_addrs, msg)
        return msgid


if __name__ == '__main__':  # pragma: no cover
    log.addHandler(logging.StreamHandler())
    log.setLevel(logging.DEBUG)
    import transaction
    with transaction.manager:
        print sendmail(u'Subject', u'Body', 'moschlar@metalabs.de', 'moschlar@metalabs.de')
