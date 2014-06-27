# -*- coding: utf-8 -*-

import re
import httplib
import urlparse
from module.plugins.Crypter import Crypter

class FeedproxyGoogleCom(Crypter):
    __name__ = "FeedproxyGoogleCom"
    __type__ = "crypter"
    __pattern__ = r'https?:\/\/feedproxy.google.com/[\/~\w]+'
    __version__ = "0.01"
    __description__ = """feedproxy.Google.com crypter plugin"""
    __author_name__ = ("nomad71")
    __author_mail__ = ("nomad71REMOVETHIS@gmx.net")

    def setup(self):
        self.multiDL = True

    # By Pedro Loureiro and Andy Jackson
    # From http://stackoverflow.com/questions/7153096/how-can-i-un-shorten-a-url-using-python

    def unshorten_url(self, url):
        parsed = urlparse.urlparse(url)
        h = httplib.HTTPConnection(parsed.netloc)
        resource = parsed.path
        if parsed.query != "":
            resource += "?" + parsed.query
        h.request('HEAD', resource )
        response = h.getresponse()
        if response.status/100 == 3 and response.getheader('Location'):
            return self.unshorten_url(response.getheader('Location')) # changed to process chains of short urls
        else:
            return url

    def decrypt(self, pyfile):
        name = __name__
        url = pyfile.url

        self.logDebug("Feedproxy URL: " + url)

        url = self.unshorten_url(url)

        self.logDebug("Resolved URL: " + url)

        urls = []
        urls.append(url)

        self.packages.append((name, urls, name))