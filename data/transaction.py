#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import logging


class TX(object):
    def __init__(self):
        self.txid = ''
        self.inputs = []
        self.outputs = []
        self.block_height = 0
        self.confirmations = 0

    def print_tx(self):
        print '\nblock ', str(self.block_height), "(" + str(self.confirmations) + " confirmations)", self.txid
        print 'IN:', self.inputs
        print 'OUT:', self.outputs
        print 'primeInput:', self.prime_input_address()

    def prime_input_address(self):
        addresses = []
        for tx_input in self.inputs:
            addresses.append(tx_input['address'])

        return sorted(addresses)[0]

    def received_value(self, address):
        value = 0
        for output in self.outputs:
            if output['address'] == address:
                value += output['value']

        return value

    def is_receiving_tx(self, address):
        received = True
        for tx_input in self.inputs:
            if tx_input['address'] == address:
                received = False

        return received

    def sent_value(self, address):
        value = 0
        for tx_input in self.inputs:
            if tx_input['address'] == address:
                value += tx_input['value']

        change = 0
        for tx_output in self.outputs:
            if tx_output['address'] == address:
                change += tx_output['value']

        return value-change

    def is_sending_tx(self, address):
        sending = False
        for tx_input in self.inputs:
            if tx_input['address'] == address:
                sending = True

        return sending

    def to_dict(self, address):
        tx_dict = {"txid": self.txid,
                   "prime_input_address": self.prime_input_address(),
                   "inputs": self.inputs,
                   "outputs": self.outputs,
                   "block_height": self.block_height,
                   "confirmations": self.confirmations,
                   "receiving": self.is_receiving_tx(address)}
        if tx_dict["receiving"] is True:
            tx_dict["receivedValue"] = self.received_value(address)
        else:
            tx_dict["sentValue"] = self.sent_value(address)

        return tx_dict

    @staticmethod
    def decode_op_return(hex_data):
        unhex_data = None
        if hex_data[:2] == '6a':
            if hex_data[2:4] == '4c':
                data = hex_data[6:]
                check_length = hex_data[4:6]
            elif hex_data[2:4] == '4d':
                data = hex_data[8:]
                check_length = hex_data[4:8]
            elif hex_data[2:4] == '4e':
                data = hex_data[10:]
                check_length = hex_data[4:10]
            else:
                data = hex_data[4:]
                check_length = hex_data[2:4]

            unhex_data = binascii.unhexlify(data)

            if len(unhex_data) != int(check_length, 16):
                logging.error(
                    'OP_RETURN data is not the correct length! {0} -> should be {1}'.format(str(len(unhex_data)),
                                                                                            str(int(check_length,
                                                                                                    16))))
                unhex_data = None

        return unhex_data
