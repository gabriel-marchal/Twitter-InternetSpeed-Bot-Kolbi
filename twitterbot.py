from TwitterAPI import TwitterAPI

import speedtest
import sched
import time
import os
from dotenv import load_dotenv
load_dotenv()

### CONFIG VARIABLES ###

consumer_key = os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token_key = os.getenv("access_token_key")
access_token_secret = os.getenv("access_token_secret")

advertised_download = 50  #in Mbps
advertised_upload = 10    #in Mbps

running_interval = 450    #in seconds

#########################



api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)

def check_speeds():
	speedtester = speedtest.Speedtest()



	# returned as bits, converted to megabits
	download_speed = int(speedtester.download() / 1000000)
	upload_speed = int(speedtester.upload() / 1000000)

	print("Download Speed: " + str(download_speed) + "Mbps")
	print("Upload Speed: " + str(upload_speed) + "Mbps")


	# # Uncomment code to create triaged messaging
	# thresholds = {'first':0.8, 'second':0.5}
	# messages = {'first':'[enter polite message]', 'second': '[enter stern message]'}
	# if download_speed < advertised_download * thresholds['first'] or upload_speed < advertised_upload * thresholds['first']:
	#     tweet = messages['first']
	#     api.request("statuses/update", {"status": tweet})
	# elif download_speed < advertised_download * thresholds['second'] or upload_speed < advertised_upload * thresholds['second']:
	#     tweet = messages['second']
	#     api.request("statuses/update", {"status": tweet})

	# If using triaged messaging, above, then comment out the conditional block, below.
	if download_speed < advertised_download * 0.75:
		tweet = "@kolbi_cr su internet es una basura! Por que me llegan solamente " + str(download_speed) + " en vez de los " + str(advertised_download) + "Mbps que me cobran? Arreglen su servicio.."
		api.request("statuses/update", {"status": tweet})
		print("Tweet sent:\n" + tweet)
		print("\n")
	else:
		print("Speeds OK, no tweet")
		print("\n")

scheduler = sched.scheduler(time.time, time.sleep)

def periodic_check(scheduler, interval, action, arguments=()):
	scheduler.enter(interval, 1, periodic_check, (scheduler, interval, action, arguments))
	action()


periodic_check(scheduler, running_interval, check_speeds)
scheduler.run()