import requests
import logging

def keep_alive(host_url):

    try:
        res = requests.get(host_url)
        if res.status_code == 200:
            logging.info(f"Pinged {host_url}")
        else:
            logging.error(f"Failed to ping {host_url}")
    except Exception as e:
        logging.error(f"Failed to ping {host_url}")
        logging.error(str(e))
