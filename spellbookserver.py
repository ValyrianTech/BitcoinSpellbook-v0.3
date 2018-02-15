#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import sys
import time
import traceback
from datetime import datetime
from functools import wraps
from logging.handlers import RotatingFileHandler

from bottle import Bottle, request, response

from action.actionhelpers import get_actions, get_action_config, save_action, delete_action, run_action, get_reveal
from authentication import initialize_api_keys_file
from data.data import get_explorers, get_explorer_config, save_explorer, delete_explorer
from data.data import latest_block, block_by_height, block_by_hash, prime_input_address
from data.data import transactions, balance, utxos
from decorators import authentication_required, use_explorer, output_json
from helpers.configurationhelpers import get_host, get_port
from helpers.hot_wallet_helpers import get_hot_wallet
from inputs.inputs import get_sil, get_profile, get_sul
from linker.linker import get_lal, get_lbl, get_lrl, get_lsl
from randomaddress.randomaddress import random_address_from_sil, random_address_from_lbl, random_address_from_lrl, \
    random_address_from_lsl
from trigger.triggerhelpers import get_triggers, get_trigger_config, save_trigger, delete_trigger, activate_trigger, \
    check_triggers, verify_signed_message


class SpellbookRESTAPI(Bottle):
    def __init__(self):
        super(SpellbookRESTAPI, self).__init__()

        # Initialize variables
        self.host = get_host()
        self.port = get_port()

        # make the directory for logs if it doesn't exist
        logs_dir = os.path.join('logs')
        if not os.path.isdir(logs_dir):
            os.makedirs(logs_dir)

        # Initialize the log
        self.log = self.initialize_log(logs_dir)

        # Initialize a separate log for the http requests to the REST API
        self.requests_log = self.initialize_requests_log(logs_dir)

        # Log the requests to the REST API in a separate file by installing a custom LoggingPlugin
        self.install(self.log_to_logger)

        # Make sure that an api_keys.json file is present, the first time the server is started
        # a new random api key and secret pair will be generated
        if not os.path.isfile('json/private/api_keys.json'):
            self.log.info('Generating new API keys')
            initialize_api_keys_file()

        self.log.info('Starting Bitcoin Spellbook')

        try:
            get_hot_wallet()
        except Exception as ex:
            self.log.error('Unable to decrypt hot wallet: %s' % ex)
            sys.exit(1)

        # Initialize the routes for the REST API
        # Routes for managing blockexplorers
        self.route('/spellbook/explorers', method='GET', callback=self.get_explorers)
        self.route('/spellbook/explorers/<explorer_id:re:[a-zA-Z0-9_\-.]+>', method='POST', callback=self.save_explorer)
        self.route('/spellbook/explorers/<explorer_id:re:[a-zA-Z0-9_\-.]+>', method='GET', callback=self.get_explorer_config)
        self.route('/spellbook/explorers/<explorer_id:re:[a-zA-Z0-9_\-.]+>', method='DELETE', callback=self.delete_explorer)

        # Routes for retrieving data from the blockchain
        self.route('/spellbook/blocks/latest', method='GET', callback=self.get_latest_block)
        self.route('/spellbook/blocks/<height:int>', method='GET', callback=self.get_block_by_height)
        self.route('/spellbook/blocks/<block_hash:re:[a-f0-9]+>', method='GET', callback=self.get_block_by_hash)

        self.route('/spellbook/transactions/<txid:re:[a-f0-9]+>/prime_input', method='GET', callback=self.get_prime_input_address)
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/transactions', method='GET', callback=self.get_transactions)
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/balance', method='GET', callback=self.get_balance)
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/utxos', method='GET', callback=self.get_utxos)

        # Routes for Simplified Inputs List (SIL)
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/SIL', method='GET', callback=self.get_sil)

        # Routes for Profile
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/profile', method='GET', callback=self.get_profile)

        # Routes for Simplified UTXO List (SUL)
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/SUL', method='GET', callback=self.get_sul)

        # Routes for Linked Lists
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/LAL', method='GET', callback=self.get_lal)
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/LBL', method='GET', callback=self.get_lbl)
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/LRL', method='GET', callback=self.get_lrl)
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/LSL', method='GET', callback=self.get_lsl)

        # Routes for Random Address
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/random/SIL', method='GET', callback=self.get_random_address_from_sil)
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/random/LBL', method='GET', callback=self.get_random_address_from_lbl)
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/random/LRL', method='GET', callback=self.get_random_address_from_lrl)
        self.route('/spellbook/addresses/<address:re:[a-km-zA-HJ-NP-Z1-9]+>/random/LSL', method='GET', callback=self.get_random_address_from_lsl)

        # Routes for Triggers
        self.route('/spellbook/triggers', method='GET', callback=self.get_triggers)
        self.route('/spellbook/triggers/<trigger_id:re:[a-zA-Z0-9_\-.]+>', method='GET', callback=self.get_trigger)
        self.route('/spellbook/triggers/<trigger_id:re:[a-zA-Z0-9_\-.]+>', method='POST', callback=self.save_trigger)
        self.route('/spellbook/triggers/<trigger_id:re:[a-zA-Z0-9_\-.]+>', method='DELETE', callback=self.delete_trigger)
        self.route('/spellbook/triggers/<trigger_id:re:[a-zA-Z0-9_\-.]+>/activate', method='GET', callback=self.activate_trigger)
        self.route('/spellbook/triggers/<trigger_id:re:[a-zA-Z0-9_\-.]+>/message', method='POST', callback=self.verify_signed_message)
        self.route('/spellbook/triggers/<trigger_id:re:[a-zA-Z0-9_\-.]+>/check', method='GET', callback=self.check_trigger)
        self.route('/spellbook/check_triggers', method='GET', callback=self.check_all_triggers)

        # Routes for Actions
        self.route('/spellbook/actions', method='GET', callback=self.get_actions)
        self.route('/spellbook/actions/<action_id:re:[a-zA-Z0-9_\-.]+>', method='GET', callback=self.get_action)
        self.route('/spellbook/actions/<action_id:re:[a-zA-Z0-9_\-.]+>', method='POST', callback=self.save_action)
        self.route('/spellbook/actions/<action_id:re:[a-zA-Z0-9_\-.]+>', method='DELETE', callback=self.delete_action)
        self.route('/spellbook/actions/<action_id:re:[a-zA-Z0-9_\-.]+>/run', method='GET', callback=self.run_action)

        # Routes for RevealSecret actions
        self.route('/spellbook/actions/<action_id:re:[a-zA-Z0-9_\-.]+>/reveal', method='GET', callback=self.get_reveal)

        # start the webserver for the REST API
        self.run(host=self.host, port=self.port)

    @staticmethod
    def initialize_log(logs_dir):
        # Create a log file for the Core daemon
        logger = logging.getLogger('Spellbook')

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
        logger.addHandler(stream_handler)

        file_handler = RotatingFileHandler(os.path.join(logs_dir, 'spellbook.txt'), maxBytes=10000000, backupCount=5)
        file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
        logger.addHandler(file_handler)

        logger.setLevel(logging.DEBUG)

        return logger

    @staticmethod
    def initialize_requests_log(logs_dir):
        # Create a log file for the http requests to the REST API
        logger = logging.getLogger('api_requests')

        file_handler = RotatingFileHandler(os.path.join(logs_dir, 'requests.txt'), maxBytes=10000000, backupCount=5)
        file_handler.setFormatter(logging.Formatter('%(message)s'))
        logger.addHandler(file_handler)

        logger.setLevel(logging.DEBUG)

        return logger

    def log_to_logger(self, fn):
        @wraps(fn)
        def _log_to_logger(*args, **kwargs):
            start_time = int(round(time.time() * 1000))
            request_time = datetime.now()
            actual_response = response
            try:
                actual_response = fn(*args, **kwargs)
            except Exception as ex:
                response_status = '500 ' + str(ex)
                self.log.error('%s caused an exception: %s' % (request.url, ex))
                traceback.print_exc()
            else:
                response_status = response.status

            end_time = int(round(time.time() * 1000))
            self.requests_log.info('%s | %s | %s | %s | %s ms | %s' % (request_time,
                                                                       request.remote_addr,
                                                                       request.method,
                                                                       response_status,
                                                                       end_time - start_time,
                                                                       request.url))
            return actual_response
        return _log_to_logger

    @staticmethod
    @output_json
    def get_explorers():
        explorers = get_explorers()
        if explorers is not None:
            return explorers
        else:
            return {'error': 'Unable to retrieve explorer_ids'}

    @staticmethod
    @authentication_required
    def save_explorer(explorer_id):
        save_explorer(explorer_id, request.json)

    @staticmethod
    @output_json
    @authentication_required
    def get_explorer_config(explorer_id):
        explorer_config = get_explorer_config(explorer_id)
        if explorer_config is not None:
            return explorer_config
        else:
            return {'error': 'No explorer configured with id: %s' % explorer_id}

    @staticmethod
    @authentication_required
    def delete_explorer(explorer_id):
        delete_explorer(explorer_id)

    @staticmethod
    @output_json
    @use_explorer
    def get_latest_block():
        return latest_block()

    @staticmethod
    @output_json
    @use_explorer
    def get_block_by_height(height):
        return block_by_height(height)

    @staticmethod
    @output_json
    @use_explorer
    def get_block_by_hash(block_hash):
        return block_by_hash(block_hash)

    @staticmethod
    @output_json
    @use_explorer
    def get_prime_input_address(txid):
        return prime_input_address(txid)

    @staticmethod
    @output_json
    @use_explorer
    def get_transactions(address):
        return transactions(address)

    @staticmethod
    @output_json
    @use_explorer
    def get_balance(address):
        return balance(address)

    @staticmethod
    @output_json
    @use_explorer
    def get_utxos(address):
        return utxos(address, int(request.query.confirmations))

    @staticmethod
    @output_json
    @use_explorer
    def get_sil(address):
        block_height = int(request.json['block_height'])
        return get_sil(address, block_height)

    @staticmethod
    @output_json
    @use_explorer
    def get_profile(address):
        block_height = int(request.json['block_height'])
        return get_profile(address, block_height)

    @staticmethod
    @output_json
    @use_explorer
    def get_sul(address):
        confirmations = int(request.json['confirmations'])
        return get_sul(address, confirmations)

    @staticmethod
    @output_json
    @use_explorer
    def get_lal(address):
        block_height = int(request.json['block_height'])
        xpub = request.json['xpub']
        return get_lal(address, xpub, block_height)

    @staticmethod
    @output_json
    @use_explorer
    def get_lbl(address):
        block_height = int(request.json['block_height'])
        xpub = request.json['xpub']
        return get_lbl(address, xpub, block_height)

    @staticmethod
    @output_json
    @use_explorer
    def get_lrl(address):
        block_height = int(request.json['block_height'])
        xpub = request.json['xpub']
        return get_lrl(address, xpub, block_height)

    @staticmethod
    @output_json
    @use_explorer
    def get_lsl(address):
        block_height = int(request.json['block_height'])
        xpub = request.json['xpub']
        return get_lsl(address, xpub, block_height)

    @staticmethod
    @output_json
    @use_explorer
    def get_random_address_from_sil(address):
        rng_block_height = int(request.json['rng_block_height'])
        sil_block_height = int(request.json['sil_block_height'])
        return random_address_from_sil(address=address, sil_block_height=sil_block_height, rng_block_height=rng_block_height)

    @staticmethod
    @output_json
    @use_explorer
    def get_random_address_from_lbl(address):
        rng_block_height = int(request.json['rng_block_height'])
        sil_block_height = int(request.json['sil_block_height'])
        xpub = request.json['xpub']
        return random_address_from_lbl(address=address, xpub=xpub, sil_block_height=sil_block_height, rng_block_height=rng_block_height)

    @staticmethod
    @output_json
    @use_explorer
    def get_random_address_from_lrl(address):
        rng_block_height = int(request.json['rng_block_height'])
        sil_block_height = int(request.json['sil_block_height'])
        xpub = request.json['xpub']
        return random_address_from_lrl(address=address, xpub=xpub, sil_block_height=sil_block_height, rng_block_height=rng_block_height)

    @staticmethod
    @output_json
    @use_explorer
    def get_random_address_from_lsl(address):
        rng_block_height = int(request.json['rng_block_height'])
        sil_block_height = int(request.json['sil_block_height'])
        xpub = request.json['xpub']
        return random_address_from_lsl(address=address, xpub=xpub, sil_block_height=sil_block_height, rng_block_height=rng_block_height)

    @staticmethod
    @output_json
    def get_triggers():
        triggers = get_triggers()
        if triggers is not None:
            return triggers
        else:
            return {'error': 'Unable to retrieve explorer_ids'}

    @staticmethod
    @output_json
    @authentication_required
    def get_trigger(trigger_id):
        trigger_config = get_trigger_config(trigger_id)
        if trigger_config is not None:
            return trigger_config
        else:
            return {'error': 'No trigger configured with id: %s' % trigger_id}

    @staticmethod
    @output_json
    @authentication_required
    def save_trigger(trigger_id):
        return save_trigger(trigger_id, **request.json)

    @staticmethod
    @output_json
    @authentication_required
    def delete_trigger(trigger_id):
        return delete_trigger(trigger_id)

    @staticmethod
    @output_json
    @authentication_required
    def activate_trigger(trigger_id):
        return activate_trigger(trigger_id)

    @staticmethod
    @output_json
    def verify_signed_message(trigger_id):
        return verify_signed_message(trigger_id, **request.json)

    @staticmethod
    @output_json
    @use_explorer
    @authentication_required
    def check_trigger(trigger_id):
        return check_triggers(trigger_id)

    @staticmethod
    @output_json
    @use_explorer
    @authentication_required
    def check_all_triggers():
        return check_triggers()

    @staticmethod
    @output_json
    def get_actions():
        actions = get_actions()
        if actions is not None:
            return actions
        else:
            return {'error': 'Unable to retrieve action_ids'}

    @staticmethod
    @output_json
    @authentication_required
    def get_action(action_id):
        action_config = get_action_config(action_id)
        if action_config is not None:
            return action_config
        else:
            return {'error': 'No action with id %s found' % action_id}

    @staticmethod
    @output_json
    @authentication_required
    def save_action(action_id):
        return save_action(action_id, **request.json)

    @staticmethod
    @output_json
    @authentication_required
    def delete_action(action_id):
        return delete_action(action_id)

    @staticmethod
    @output_json
    @authentication_required
    def run_action(action_id):
        return run_action(action_id)

    @staticmethod
    @output_json
    def get_reveal(action_id):
        return get_reveal(action_id)


if __name__ == "__main__":
    SpellbookRESTAPI()
