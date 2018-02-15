#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import logging

from action import Action
from actiontype import ActionType
from validators.validators import valid_url


class WebhookAction(Action):
    def __init__(self, action_id):
        super(WebhookAction, self).__init__(action_id=action_id)
        self.action_type = ActionType.WEBHOOK
        self.webhook = None

    def run(self):
        if self.webhook is None:
            return False

        logging.getLogger('Spellbook').info('executing webhook: %s' % self.webhook)
        try:
            r = requests.get(self.webhook)
        except Exception as ex:
            logging.getLogger('Spellbook').error('Webhook failed: %s' % ex)
            return False
        else:
            if r.status_code == 200:
                logging.getLogger('Spellbook').info('status code webhook: %s' % r.status_code)
                return True
            else:
                logging.getLogger('Spellbook').error('Webhook failed: status code webhook: %s' % r.status_code)
                return False

    def configure(self, **config):
        super(WebhookAction, self).configure(**config)
        if 'webhook' in config and valid_url(config['webhook']):
            self.webhook = config['webhook']

    def json_encodable(self):
        ret = super(WebhookAction, self).json_encodable()
        ret.update({'webhook': self.webhook})
        return ret
