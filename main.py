import requests
import sys
import random
import time

print("TT RPS Player")
print("Optimizing the fun out of RPS since 2020")
print("Loading...")

# ids used by the api of doom
rock = 0
paper = 1
scissors = 2

# just to make our print statements nicer

moveset = ['rock', 'paper', 'scissors']

api_url = "http://gangadiddle.com/rpsapi.php"; # current url of the api

if len(sys.argv) == 1:
	print("Enter HFMN: ")
	HFMN = input('>> ')
else:
	HFMN = sys.argv[1]

print("Asking gangadiddle.com about HFMN...")

HFMN_check_post = {'magicNo': HFMN}
HFMN_check_req = requests.post(api_url, data=HFMN_check_post).json()
HFMN_check_msg = HFMN_check_req['responseCode']

if HFMN_check_msg == 3: # blank userMsg, based on tests, assuming it means valid.
	print('Valid HFMN!')
	session_id = HFMN_check_req['rpsSession']
elif HFMN_check_msg == 5: # HFMN not found
	print('Invalid HFMN.')
	sys.exit()
elif HFMN_check_msg == 6:
	print('Not a number at all!')
	sys.exit()
else:
	print('unknown error.')
	print(HFMN_check_req)
	sys.exit()

print('Session ID: {}'.format(session_id))

print('Getting move...')

move_id = random.randrange(0, 3) # random move 0-2, somewhat similar to TT's move generator.

print('Move: {}'.format(moveset[move_id]))

def sendMove(move_id, session_id):
	print('Sending move...')
	move_json = {
		'playerMove': move_id,
		'rpsSessionId': session_id
	}
	try:
		move_req = requests.post(api_url, data=move_json)
		move_req_json = move_req.json()
	except:
		print(move_req.text) # strange error.
	if move_req.text == '':
		print('Unknown error sending move. You probably have been ratelimited. Wait.')
		sys.exit()
	move_req = move_req_json
	move_status = move_req['responseCode']
	if move_status == 1:
		print('Session expired.')
	elif move_status == 7:
		print('Too fast. Waiting 2 sec and repeating request.')
		time.sleep(2)
		return sendMove(move_id, session_id)
	elif move_status == 8:
		print('Received move!')
		return move_req
	elif move_status == 9:
		print('Received move!')
		return move_req
	elif move_status == 10:
		print('Received move!')
		return move_req

move_req = sendMove(move_id, session_id)
#print(move_req)
if move_req['responseCode'] == 8:
	print("ooh cool you got a key")
	print(move_req['magicKey'])
elif move_req['responseCode'] == 9:
	print('ya lost. play again?')
elif move_req['responseCode'] == 10:
	print('its a tie. run it again now')
else:
	print('i suck at programming')
	print('file a bug report with the following json data')
	print(move_req)

print('')
print('kthxbai')