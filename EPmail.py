import requests


class EPmail:
    def __init__(self, apiurl='https://api.mailgun.net/v3/mail.easypatents.cl/messages',
                 apikey='key-a4953915dffa936b1e83070c0de3c3ef'):
        self.apiurl = apiurl
        self.apikey = apikey

    def send_simple_message(self, mto='', mfrom='', msjt='', mmsg=''):
        return requests.post(
                self.apiurl,
                auth=("api",    self.apikey),
                data={"from":   mfrom,
                    "to":     mto,
                    "subject":msjt,
                    "text":   mmsg})

    def send_complex_message(self, mto='', mfrom='', msjt='', mmsg='', mformat='', fpath=''):
        return requests.post(
            self.apiurl,
            auth=("api",self.apikey),
            files=[("attachment", (mformat, open(fpath, "rb").read()))],
            data={"from":   mfrom,
                  "to":     mto,
                  "subject":msjt,
                  "text":   mmsg})