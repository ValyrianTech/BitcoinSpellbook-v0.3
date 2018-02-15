#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from BIP44.BIP44 import set_testnet
from data.data import balance
from helpers.configurationhelpers import get_use_testnet
from helpers.hot_wallet_helpers import get_address_from_wallet
from integration_test_helpers import spellbook_call

# Change working dir up one level
os.chdir("..")

print 'Starting Spellbook integration test: Balance trigger conditions'
print '----------------------------------------------\n'

#########################################################################################################
# Blockheight trigger
#########################################################################################################

print 'Getting the list of configured triggers'
configured_triggers = spellbook_call('get_triggers')

trigger_name = 'test_trigger_conditions_BalanceTrigger'

# Clean up old test action if necessary
if trigger_name in configured_triggers:
    response = spellbook_call('delete_trigger', trigger_name)
    assert response is None

# --------------------------------------------------------------------------------------------------------
trigger_type = 'Balance'

# ----------------------------------------------------------------------------------------------------------------------

set_testnet(get_use_testnet())

account = 0
index = 3

address = get_address_from_wallet(account=account, index=index)
balance_data = balance(address=address)
print balance_data
amount = balance_data['balance']['final'] + 1


print 'Creating Balance trigger'

print 'Setting trigger amount higher than current balance'
response = spellbook_call('save_trigger', '-t=%s' % trigger_type, trigger_name, '--reset', '-a=%s' % address, '-am=%s' % amount)
assert response is None

print 'Checking if trigger has not been triggered yet'
response = spellbook_call('get_trigger_config', trigger_name)
assert response['triggered'] is False
assert response['address'] == address
assert response['amount'] == amount

print 'Check the conditions of the trigger'
response = spellbook_call('check_triggers', trigger_name)
assert response is None
response = spellbook_call('get_trigger_config', trigger_name)
assert response['triggered'] is False

amount -= 1
print 'Setting trigger amount equal to current balance'
response = spellbook_call('save_trigger', trigger_name, '--reset', '-am=%s' % amount)
assert response is None

print 'Checking if trigger has not been triggered yet'
response = spellbook_call('get_trigger_config', trigger_name)
assert response['triggered'] is False
assert response['address'] == address
assert response['amount'] == amount

print 'Check the conditions of the trigger'
response = spellbook_call('check_triggers', trigger_name)
assert response is None
response = spellbook_call('get_trigger_config', trigger_name)
assert response['triggered'] is True

