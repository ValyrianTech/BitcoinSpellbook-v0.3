#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import time

from helpers.loghelpers import LOG
from trigger.balancetrigger import BalanceTrigger
from trigger.blockheighttrigger import BlockHeightTrigger
from trigger.deadmansswitchtrigger import DeadMansSwitchTrigger
from helpers.jsonhelpers import load_from_json_file
from trigger.manualtrigger import ManualTrigger
from trigger.receivedtrigger import ReceivedTrigger
from trigger.recurringtrigger import RecurringTrigger
from trigger.senttrigger import SentTrigger
from sign_message import verify_message
from trigger.signedmessagetrigger import SignedMessageTrigger
from trigger.timestamptrigger import TimestampTrigger
from trigger.triggerstatustrigger import TriggerStatusTrigger
from trigger.httpgetrequesttrigger import HTTPGetRequestTrigger
from trigger.httppostrequesttrigger import HTTPPostRequestTrigger
from trigger.httpdeleterequesttrigger import HTTPDeleteRequestTrigger
from trigger.triggertype import TriggerType
from helpers.actionhelpers import delete_action

TRIGGERS_DIR = 'json/public/triggers'


def get_triggers():
    """
    Get the list of triggers_ids

    :return: A list of trigger_ids
    """
    triggers = glob.glob(os.path.join(TRIGGERS_DIR, '*.json'))

    return [os.path.splitext(os.path.basename(trigger))[0] for trigger in triggers]


def get_trigger_config(trigger_id):
    """
    Get the configuration of a trigger

    :param trigger_id: id of the trigger
    :return: a dict containing the configuration of the trigger
    """
    try:
        trigger_config = load_from_json_file(os.path.join(TRIGGERS_DIR, '%s.json' % trigger_id))
    except IOError:
        # Trigger does not exist yet, return empty dict
        trigger_config = {}

    return trigger_config


def get_trigger(trigger_id, trigger_type=None):
    """
    Get the specified trigger, which is a subclass of Trigger
    The different trigger types are:
    - ManualTrigger (default)
    - BalanceTrigger
    - ReceivedTrigger
    - SentTrigger
    - BlockHeightTrigger
    - TimestampTrigger
    - RecurringTrigger
    - TriggerStatusTrigger

    If no config is known for the given trigger id then a ManualTrigger is returned

    :param trigger_id: The id of the trigger
    :param trigger_type: The type of the trigger (optional)
    :return: A child class of Trigger
    """
    trigger_config = get_trigger_config(trigger_id)

    if trigger_type is not None:
        trigger_config['trigger_type'] = trigger_type

    if trigger_config['trigger_type'] == TriggerType.BALANCE:
        trigger = BalanceTrigger(trigger_id)
    elif trigger_config['trigger_type'] == TriggerType.RECEIVED:
        trigger = ReceivedTrigger(trigger_id)
    elif trigger_config['trigger_type'] == TriggerType.SENT:
        trigger = SentTrigger(trigger_id)
    elif trigger_config['trigger_type'] == TriggerType.BLOCK_HEIGHT:
        trigger = BlockHeightTrigger(trigger_id)
    elif trigger_config['trigger_type'] == TriggerType.TIMESTAMP:
        trigger = TimestampTrigger(trigger_id)
    elif trigger_config['trigger_type'] == TriggerType.RECURRING:
        trigger = RecurringTrigger(trigger_id)
    elif trigger_config['trigger_type'] == TriggerType.TRIGGERSTATUS:
        trigger = TriggerStatusTrigger(trigger_id)
    elif trigger_config['trigger_type'] == TriggerType.DEADMANSSWITCH:
        trigger = DeadMansSwitchTrigger(trigger_id)
    elif trigger_config['trigger_type'] == TriggerType.SIGNEDMESSAGE:
        trigger = SignedMessageTrigger(trigger_id)
    elif trigger_config['trigger_type'] == TriggerType.MANUAL:
        trigger = ManualTrigger(trigger_id)
    elif trigger_config['trigger_type'] == TriggerType.HTTPGETREQUEST:
        trigger = HTTPGetRequestTrigger(trigger_id)
    elif trigger_config['trigger_type'] == TriggerType.HTTPPOSTREQUEST:
        trigger = HTTPPostRequestTrigger(trigger_id)
    elif trigger_config['trigger_type'] == TriggerType.HTTPDELETEREQUEST:
        trigger = HTTPDeleteRequestTrigger(trigger_id)
    else:
        raise NotImplementedError('Unknown trigger type: %s' % trigger_config['trigger_type'])

    trigger.configure(**trigger_config)

    return trigger


def save_trigger(trigger_id, **trigger_config):
    """
    Save or update a trigger config in the triggers.json file

    :param trigger_id: The id of the trigger
    :param trigger_config: A dict containing the configuration for the trigger
    """
    if 'trigger_type' in trigger_config:
        trigger = get_trigger(trigger_id, trigger_type=trigger_config['trigger_type'])
    else:
        trigger = get_trigger(trigger_id)

    trigger.configure(**trigger_config)
    trigger.save()


def delete_trigger(trigger_id):
    """
    Delete a trigger

    :param trigger_id: The id of the trigger to delete
    """
    filename = os.path.join(TRIGGERS_DIR, '%s.json' % trigger_id)
    if os.path.isfile(filename):
        os.remove(filename)
    else:
        return {'error': 'Unknown trigger id: %s' % trigger_id}


def activate_trigger(trigger_id):
    """
    Activate a Manual trigger or a DeadMansSwitch trigger

    :param trigger_id: The id of the trigger
    """
    if not os.path.isfile(os.path.join(TRIGGERS_DIR, '%s.json' % trigger_id)):
        return {'error': 'Unknown trigger id: %s' % trigger_id}

    trigger = get_trigger(trigger_id)
    if trigger.trigger_type == TriggerType.MANUAL:
        trigger.activate()
    elif trigger.trigger_type == TriggerType.DEADMANSSWITCH:
        trigger.arm()
    else:
        return {'error': 'Only triggers of type Manual or DeadmansSwitch can be activated manually'}


def check_triggers(trigger_id=None):
    # Get a list of all trigger_ids that are configured
    triggers = get_triggers()

    # If a trigger_id is given, only check that specific trigger
    if trigger_id is not None and trigger_id in triggers:
        triggers = [trigger_id]
    elif trigger_id is not None and trigger_id not in triggers:
        return {'error': 'Unknown trigger id: %s' % trigger_id}

    for trigger_id in triggers:
        trigger = get_trigger(trigger_id=trigger_id)
        if trigger.self_destruct is not None:
            if trigger.self_destruct <= int(time.time()):
                LOG.info('Trigger %s has reached its self-destruct time' % trigger_id)

                # Also destruct any attached actions if needed
                if trigger.destruct_actions is True:
                    for action_id in trigger.actions:
                        LOG.info('Deleting action %s' % action_id)
                        delete_action(action_id=action_id)

                LOG.info('Deleting trigger %s' % trigger_id)
                delete_trigger(trigger_id=trigger_id)
                continue

        if trigger.status == 'Active':
            LOG.info('Checking conditions of trigger %s' % trigger_id)
            if trigger.conditions_fulfilled() is True:
                trigger.activate()


def verify_signed_message(trigger_id, **data):
    if not all(key in data for key in ['address', 'message', 'signature']):
        return {'error': 'Request data does not contain all required keys: address, message and signature'}

    triggers = get_triggers()
    if trigger_id not in triggers:
        return {'error': 'Unknown trigger id: %s' % trigger_id}

    trigger = get_trigger(trigger_id)
    if trigger.trigger_type != TriggerType.SIGNEDMESSAGE:
        return {'error': 'Trigger %s is not a Signedmessage trigger' % trigger.trigger_type}

    if trigger.address is not None and trigger.address != data['address']:
        return {'error': 'Trigger %s only listens to signed messages from address %s' % (trigger.id, trigger.address)}

    if verify_message(address=data['address'], message=data['message'], signature=data['signature']) is True:
        if trigger.status == 'Active':
            LOG.info('Trigger %s received a verified signed message' % trigger_id)
            trigger.process_message(address=data['address'], message=data['message'], signature=data['signature'])
            return trigger.activate()
    else:
        LOG.warning('Trigger %s received a bad signed message' % trigger_id)


def http_get_request(trigger_id, **data):
    triggers = get_triggers()
    if trigger_id not in triggers:
        return {'error': 'Unknown trigger id: %s' % trigger_id}

    trigger = get_trigger(trigger_id)
    if trigger.trigger_type != TriggerType.HTTPGETREQUEST:
        return {'error': 'Trigger %s is not a HTTP GET request trigger but a %s trigger' % (trigger_id, trigger.trigger_type)}

    if trigger.status == 'Active':
        LOG.info('Trigger %s received a HTTP GET request' % trigger_id)
        if len(data) > 0:
            trigger.set_json_data(data=data)
        return trigger.activate()


def http_post_request(trigger_id, **data):
    triggers = get_triggers()
    if trigger_id not in triggers:
        return {'error': 'Unknown trigger id: %s' % trigger_id}

    trigger = get_trigger(trigger_id)
    if trigger.trigger_type != TriggerType.HTTPPOSTREQUEST:
        return {'error': 'Trigger %s is not a HTTP POST request trigger but a %s trigger' % (trigger_id, trigger.trigger_type)}

    if trigger.status == 'Active':
        LOG.info('Trigger %s received a HTTP POST request' % trigger_id)
        if len(data) > 0:
            trigger.set_json_data(data=data)
        return trigger.activate()


def http_delete_request(trigger_id, **data):
    triggers = get_triggers()
    if trigger_id not in triggers:
        return {'error': 'Unknown trigger id: %s' % trigger_id}

    trigger = get_trigger(trigger_id)
    if trigger.trigger_type != TriggerType.HTTPDELETEREQUEST:
        return {'error': 'Trigger %s is not a HTTP DELETE request trigger but a %s trigger' % (trigger_id, trigger.trigger_type)}

    if trigger.status == 'Active':
        LOG.info('Trigger %s received a HTTP DELETE request' % trigger_id)
        if len(data) > 0:
            trigger.set_json_data(data=data)
        return trigger.activate()