#!/usr/bin/python
# -*- coding: utf-8 -*-

########################################################################################################
# get_explorers                                                                                        #
########################################################################################################
GET_EXPLORERS_DESCRIPTION = 'Get the list of explorer_ids that are configured on the spellbook server.'
GET_EXPLORERS_EPILOG = '''
examples:
  - spellbook.py get_explorers
    -> Get a list of configured explorers
'''

########################################################################################################
# save_explorer                                                                                        #
########################################################################################################
SAVE_EXPLORER_DESCRIPTION = 'Save or update the configuration of an explorer in the spellbook.'
SAVE_EXPLORER_EPILOG = '''
examples:
  - spellbook.py save_explorer blockchain.info Blockchain.info https://blockchain.info 1
    -> Save or update an explorer with name 'blockchain.info' in the spellbook with priority 1
    
  - spellbook.py save_explorer blockchain.info Blockchain.info https://testnet.blockchain.info 1 --TESTNET
    -> Save or update an explorer with name 'blockchain.info' in the spellbook with priority 1 to use the testnet instead of mainnet
    
  - spellbook.py save_explorer blocktrail Blocktrail.com https://api.blocktrail.com/v1 2 -b='ABC123'
    -> Save or update an explorer with name 'blocktrail.com' in the spellbook with priority 2 and given blocktrail api key    
   
  - spellbook.py save_explorer ... -k=<myapikey> -s=<myapisecret>
    -> Use given api key and api secret to authenticate with the REST API
'''

########################################################################################################
# get_explorer_config                                                                                  #
########################################################################################################
GET_EXPLORER_CONFIG_DESCRIPTION = 'Get configuration info about a specific explorer.'
GET_EXPLORER_CONFIG_EPILOG = '''
examples:
  - spellbook.py get_explorer_config blocktrail.com
    -> Get configuration info about a specific explorer with id 'blocktrail.com'
    
  - spellbook.py get_explorer_config ... -k=<myapikey> -s=<myapisecret>
    -> Use given api key and api secret to authenticate with the REST API
'''

########################################################################################################
# delete_explorer                                                                                      #
########################################################################################################
DELETE_EXPLORER_DESCRIPTION = 'Delete a specific explorer.'
DELETE_EXPLORER_EPILOG = '''
examples:
  - spellbook.py delete_explorer blocktrail.com
    -> Delete the explorer with id 'blocktrail.com'
  
  - spellbook.py delete_explorer ... -k=<myapikey> -s=<myapisecret>
    -> Use given api key and api secret to authenticate with the REST API
'''

########################################################################################################
# get_latest_block                                                                                     #
########################################################################################################
GET_LATEST_BLOCK_DESCRIPTION = 'Get the latest block.'
GET_LATEST_BLOCK_EPILOG = '''
examples:
  - spellbook.py get_latest_block
    -> Get the latest block using the default explorer
    
  - spellbook.py get_latest_block --explorer=blockchain.info
    -> Get the latest block using the blockchain.info explorer to retrieve the data    
'''

########################################################################################################
# get_block                                                                                            #
########################################################################################################
GET_BLOCK_DESCRIPTION = 'Get a block by a block hash or a block height.'
GET_BLOCK_EPILOG = '''
examples:
  - spellbook.py get_block 488470
    -> Get block at height 488470 using the default explorer
  
  - spellbook.py get_block 000000000000000000f6af507822a695390bada30cbd0c517c12442effb277af
    -> Get block with hash 000000000000000000f6af507822a695390bada30cbd0c517c12442effb277af using the default explorer
  
  - spellbook.py get_block 488470 --explorer=blockchain.info
    -> Get block at height 488470 using the blockchain.info explorer to retrieve the data
'''

########################################################################################################
# get_prime_input_address                                                                              #
########################################################################################################
GET_PRIME_INPUT_ADDRESS_DESCRIPTION = 'Get the prime input address of a transaction. This is the input address that comes first alphabetically.'
GET_PRIME_INPUT_ADDRESS_EPILOG = '''
examples:
  - spellbook.py get_prime_input_address 39bb5f5d50882227f93b980df15ea676414f0363770a0174a13c8f55c877b598
    -> Get the prime input address of tx 39bb5f5d50882227f93b980df15ea676414f0363770a0174a13c8f55c877b598 using the default explorer
    
  - spellbook.py get_prime_input_address 39bb5f5d50882227f93b980df15ea676414f0363770a0174a13c8f55c877b598 --explorer=blockchain.info
    -> Get the prime input address of tx 39bb5f5d50882227f93b980df15ea676414f0363770a0174a13c8f55c877b598 using the blockchain.info explorer to retrieve the data
'''

########################################################################################################
# get_transactions                                                                                     #
########################################################################################################
GET_TRANSACTIONS_DESCRIPTION = 'Get all transactions that a specific address has received or sent.'
GET_TRANSACTIONS_EPILOG = '''
examples:
  - spellbook.py get_transactions 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8
    -> Get all transactions of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 using the default explorer

  - spellbook.py get_transactions 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 --explorer=blockchain.info
    -> Get all transactions of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 using the blockchain.info explorer to retrieve the data
'''

########################################################################################################
# get_balance                                                                                          #
########################################################################################################
GET_BALANCE_DESCRIPTION = 'Get the current balance of an address. This includes the final balance, the total received balance and total sent balance'
GET_BALANCE_EPILOG = '''
examples:
  - spellbook.py get_balance 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8
    -> Get the balance of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 using the default explorer

  - spellbook.py get_balance 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 --explorer=blockchain.info
    -> Get the balance of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 using the blockchain.info explorer to retrieve the data
'''

########################################################################################################
# get_utxos                                                                                            #
########################################################################################################
GET_UTXOS_DESCRIPTION = 'Get the UTXOs of an address with at least the specified number of confirmations (default=1).'
GET_UTXOS_EPILOG = '''
examples:
  - spellbook.py get_utxos 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8
    -> Get the UTXOs of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with at least 1 confirmation using the default explorer

  - spellbook.py get_utxos 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 -c=6
    -> Get the UTXOs of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with at least 6 confirmations using the default explorer

  - spellbook.py get_utxos 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 --explorer=blockchain.info
    -> Get the UTXOs of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 using the blockchain.info explorer to retrieve the data
'''

########################################################################################################
# get_sil                                                                                              #
########################################################################################################
GET_SIL_DESCRIPTION = 'Get the Simplified Inputs List (SIL) of an address.'
GET_SIL_EPILOG = '''
examples:
  - spellbook.py get_sil 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8
    -> Get the SIL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 using the default explorer

  - spellbook.py get_sil 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 -b=478000
    -> Get the SIL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 at block height 478000 using the default explorer

  - spellbook.py get_sil 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 --explorer=blockchain.info
    -> Get the SIL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 using the blockchain.info explorer to retrieve the data
'''

########################################################################################################
# get_profile                                                                                          #
########################################################################################################
GET_PROFILE_DESCRIPTION = 'Get the profile of an address.'
GET_PROFILE_EPILOG = '''
examples:
  - spellbook.py get_profile 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8
    -> Get the profile of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 using the default explorer

  - spellbook.py get_profile 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 -b=478000
    -> Get the profile of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 at block height 478000 using the default explorer

  - spellbook.py get_profile 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 --explorer=blockchain.info
    -> Get the profile of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 using the blockchain.info explorer to retrieve the data
'''

########################################################################################################
# get_sul                                                                                              #
########################################################################################################
GET_SUL_DESCRIPTION = 'Get the Simplified UTXO List (SUL) of an address.'
GET_SUL_EPILOG = '''
examples:
  - spellbook.py get_sul 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8
    -> Get the SUL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 using the default explorer

  - spellbook.py get_sul 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 -c=6
    -> Get the SUL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with at least 6 confirmations using the default explorer

  - spellbook.py get_sul 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 --explorer=blockchain.info
    -> Get the SUL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 using the blockchain.info explorer to retrieve the data
'''

########################################################################################################
# get_lal                                                                                              #
########################################################################################################
GET_LAL_DESCRIPTION = 'Get the Linked Address List (LAL) of an address and an xpub key.'
GET_LAL_EPILOG = '''
examples:
  - spellbook.py get_lal 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD
    -> Get the LAL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with xpub key xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD using the default explorer

  - spellbook.py get_lal 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD -b=478000
    -> Get the LAL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with xpub key xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD at block height 478000 using the default explorer

  - spellbook.py get_lal 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD --explorer=blockchain.info
    -> Get the LAL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with xpub key xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD using the blockchain.info explorer to retrieve the data
'''

########################################################################################################
# get_lbl                                                                                              #
########################################################################################################
GET_LBL_DESCRIPTION = 'Get the Linked Balance List (LBL) of an address and an xpub key.'
GET_LBL_EPILOG = '''
examples:
  - spellbook.py get_lbl 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD
    -> Get the LBL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with xpub key xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD using the default explorer

  - spellbook.py get_lbl 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD -b=478000
    -> Get the LBL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with xpub key xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD at block height 478000 using the default explorer

  - spellbook.py get_lbl 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD --explorer=blockchain.info
    -> Get the LBL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with xpub key xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD using the blockchain.info explorer to retrieve the data
'''

########################################################################################################
# get_lrl                                                                                              #
########################################################################################################
GET_LRL_DESCRIPTION = 'Get the Linked Received List (LRL) of an address and an xpub key.'
GET_LRL_EPILOG = '''
examples:
  - spellbook.py get_lrl 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD
    -> Get the LRL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with xpub key xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD using the default explorer

  - spellbook.py get_lrl 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD -b=478000
    -> Get the LRL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with xpub key xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD at block height 478000 using the default explorer

  - spellbook.py get_lrl 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD --explorer=blockchain.info
    -> Get the LRL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with xpub key xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD using the blockchain.info explorer to retrieve the data
'''

########################################################################################################
# get_lsl                                                                                              #
########################################################################################################
GET_LSL_DESCRIPTION = 'Get the Linked Sent List (LSL) of an address and an xpub key.'
GET_LSL_EPILOG = '''
examples:
  - spellbook.py get_lsl 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD
    -> Get the LSL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with xpub key xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD using the default explorer

  - spellbook.py get_lsl 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD -b=478000
    -> Get the LSL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with xpub key xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD at block height 478000 using the default explorer

  - spellbook.py get_lsl 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD --explorer=blockchain.info
    -> Get the LSL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with xpub key xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD using the blockchain.info explorer to retrieve the data
'''

########################################################################################################
# get_random_address                                                                                   #
########################################################################################################
GET_RANDOM_ADDRESS_DESCRIPTION = 'Get a random address from SIL, LBL, LRL or LSL where the chance of an address being picked is proportional to its value in the list.'
GET_RANDOM_ADDRESS_EPILOG = '''
examples:
  - spellbook.py get_random_address SIL 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 480000
    -> Get a random address from the SIL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 using the blockhash of block 480000 as a random number

  - spellbook.py get_random_address SIL 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 480000 --block_height=450000
    -> Get a random address from the SIL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 at block 450000 using the blockhash of block 480000 as a random number

  - spellbook.py get_random_address LBL 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 480000 --xpub=xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD
    -> Get a random address from the LBL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with given xpub key using the blockhash of block 480000 as a random number

  - spellbook.py get_random_address LRL 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 480000 --xpub=xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD
    -> Get a random address from the LRL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with given xpub key using the blockhash of block 480000 as a random number

  - spellbook.py get_random_address LSL 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 480000 --xpub=xpub6CUvzHsNLcxthhGJesNDPSh2gicdHLPAAeyucP2KW1vBKEMxvDWCYRJZzM4g7mNiQ4Zb9nG4y25884SnYAr1P674yQipYLU8pP5z8AmahmD
    -> Get a random address from the LSL of address 1BAZ9hiAsMdSyw8CMeUoH4LeBnj7u6D7o8 with given xpub key using the blockhash of block 480000 as a random number
'''

########################################################################################################
# get_triggers                                                                                         #
########################################################################################################
GET_TRIGGERS_DESCRIPTION = 'Get the list of configured triggers.'
GET_TRIGGERS_EPILOG = '''
examples:
  - spellbook.py get_triggers
    -> Get the list of all configured triggers

  - spellbook.py get_triggers --active
    -> Get the list of active triggers
'''

########################################################################################################
# get_trigger_config                                                                                   #
########################################################################################################
GET_TRIGGER_CONFIG_DESCRIPTION = 'Get the configuration of specified trigger.'
GET_TRIGGER_CONFIG_EPILOG = '''
examples:
  - spellbook.py get_trigger_config mytrigger
    -> Get the configuration of the trigger with id 'mytrigger'

  - spellbook.py get_trigger ... -k=<myapikey> -s=<myapisecret>
    -> Use given api key and api secret to authenticate with the REST API
'''

########################################################################################################
# delete_trigger                                                                                       #
########################################################################################################
DELETE_TRIGGER_DESCRIPTION = 'Delete a specified trigger.'
DELETE_TRIGGER_EPILOG = '''
examples:
  - spellbook.py delete_trigger mytrigger
    -> Delete the trigger with id 'mytrigger'

  - spellbook.py delete_trigger ... -k=<myapikey> -s=<myapisecret>
    -> Use given api key and api secret to authenticate with the REST API
'''

########################################################################################################
# activate_trigger                                                                                     #
########################################################################################################
ACTIVATE_TRIGGER_DESCRIPTION = "Activate a specified manual trigger. The trigger must be of type 'Manual' or 'DeadMansSwitch'"
ACTIVATE_TRIGGER_EPILOG = '''
examples:
  - spellbook.py activate_trigger mytrigger
    -> Activate the trigger with id 'mytrigger'

  - spellbook.py activate_trigger ... -k=<myapikey> -s=<myapisecret>
    -> Use given api key and api secret to authenticate with the REST API
'''

########################################################################################################
# send_signed_message                                                                                  #
########################################################################################################
SEND_SIGNED_MESSAGE_DESCRIPTION = "Send a signed message to a trigger. The trigger must be of type 'SignedMessage'"
SEND_SIGNED_MESSAGE_EPILOG = '''
examples:
  - spellbook.py send_signed_message mytrigger <address> <message> <signature>
    -> Send a signed message to the trigger with id 'mytrigger'
       If <message> contains an existing filename, then the contents of that file are sent as message.
'''

########################################################################################################
# check_triggers                                                                                       #
########################################################################################################
CHECK_TRIGGERS_DESCRIPTION = "Check triggers and activate them if conditions have been fulfilled."
CHECK_TRIGGERS_EPILOG = '''
examples:
  - spellbook.py check_triggers
    -> Check all triggers and activate them if conditions have been fulfilled

  - spellbook.py check_triggers mytrigger
    -> Check the trigger with id 'mytrigger' and activate it if conditions have been fulfilled

  - spellbook.py check_triggers mytrigger --explorer=blocktrail.com
    -> Check the trigger with id 'mytrigger' and activate it if conditions have been fulfilled using the blocktrail.com explorers

  - spellbook.py check_triggers ... -k=<myapikey> -s=<myapisecret>
    -> Use given api key and api secret to authenticate with the REST API
'''

########################################################################################################
# get_actions                                                                                          #
########################################################################################################
GET_ACTIONS_DESCRIPTION = "Get the list of configured action_ids."
GET_ACTIONS_EPILOG = '''
examples:
  - spellbook.py get_actions
    -> Get the list of all configured action_ids

  - spellbook.py get_actions --trigger_id=mytrigger
    -> Get the list of all configured action_ids on trigger 'mytrigger'
'''

########################################################################################################
# get_action_config                                                                                    #
########################################################################################################
GET_ACTION_CONFIG_DESCRIPTION = 'Get the configuration of specified action.'
GET_ACTION_CONFIG_EPILOG = '''
examples:
  - spellbook.py get_action_config myaction
    -> Get the configuration of the action 'myaction'

  - spellbook.py get_action_config ... -k=<myapikey> -s=<myapisecret>
    -> Use given api key and api secret to authenticate with the REST API
'''

########################################################################################################
# delete_action                                                                                        #
########################################################################################################
DELETE_ACTION_DESCRIPTION = 'Delete a specified action.'
DELETE_ACTION_EPILOG = '''
examples:
  - spellbook.py delete_action myaction
    -> Delete the action with id 'myaction'

  - spellbook.py delete_action ... -k=<myapikey> -s=<myapisecret>
    -> Use given api key and api secret to authenticate with the REST API
'''