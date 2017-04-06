import subprocess

subprocess.call('netsh wlan set hostednetwork mode=allow ssid=rishav key=password',shell=True)
subprocess.call('netsh wlan start hostednetwork ',shell=True)