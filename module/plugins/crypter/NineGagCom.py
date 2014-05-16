# -*- coding: utf-8 -*-

import re
from module.plugins.Crypter import Crypter

class NineGagCom(Crypter):
    __name__ = "NineGagCom"
    __type__ = "crypter"
    __pattern__ = r'http:\/\/(?:www\.)?9gag\.com\/gag\/\w+'
    __version__ = "0.01"
    __description__ = """9Gag.com crypter plugin"""
    __author_name__ = ("nomad71")
    __author_mail__ = ("nomad71REMOVETHIS@gmx.net")

    FILE_NAME_PATTERN = r'<title>(?P<name>.*)<\/title>'
    LINK_PATTERN = r'data-img="(?P<link>.*)"'
    GIF_PATTERN = r'<img class="badge-item-animated-img" \n\s*src=\"(?P<gif>.*)\"'
    FILE_OFFLINE_PATTERN = r'<p>Sorry, the page you\'re looking for doesn\'t exist.</p>'
    
    
    def setup(self):
        self.multiDL = True

    def decrypt(self, pyfile):
        self.html = self.load(pyfile.url, decode=True)
        #self.getFileInfo()

        # Check if Site is online
        if re.search(self.FILE_OFFLINE_PATTERN, self.html):
            self.offline()

        name = re.search(self.FILE_NAME_PATTERN, self.html)

        if name:
            name = name.group('name')
            #self.logDebug("Name: " + name)
        else:
            self.fail(_("No name was found!"))

        gif = re.search(self.GIF_PATTERN, self.html)

        if gif:
            link = gif.group('gif')
            self.logDebug("GIF found")
        else:
            link = re.search(self.LINK_PATTERN, self.html)
            if link:
                link = link.group('link')
            else:
                self.fail(_("No Link was found!"))

        links = []
        links.append(str(link))

        self.packages.append((name, links, name))