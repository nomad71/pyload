# -*- coding: utf-8 -*-

import re
import HTMLParser
from module.plugins.Crypter import Crypter

class ImgurCom(Crypter):
    __name__ = "ImgurCom"
    __type__ = "crypter"
    __pattern__ = r'https?:\/\/(?:www\.|m\.)?imgur\.com\/(gallery|a)\/\w+'
    __version__ = "0.01"
    __description__ = """Imgur.com crypter plugin"""
    __author_name__ = ("nomad71")
    __author_mail__ = ("nomad71REMOVETHIS@gmx.net")

    FILE_NAME_PATTERN = r'<meta property="og:title" content="(?P<name>.*?)"\/>'
    ALBUM_LINK_PATTERN = r'<a href="//(?P<link>.*)" target="_blank">View full resolution<\/a>'
    GALLERY_LINK_PATTERN = r'<img src="//(?P<link>.*)" alt="" \/>'
    FILE_OFFLINE_PATTERN = r'<h1>Zoinks! You\'ve taken a wrong turn\.<\/h1>'
    THERE_IS_MORE_PATTERN = r'<div id="album-truncated" class="small textbox album-truncated"><a target="_blank" href="\/\/(?P<more>.*?)\?gallery">View the entire album'


    def setup(self):
        self.multiDL = True

    def decrypt(self, pyfile):
        self.html = self.load(pyfile.url, decode=True)
        
        # Check if Site is online
        if re.search(self.FILE_OFFLINE_PATTERN, self.html):
            self.offline()

        # Check if there is a bigger Album
        more = re.search(self.THERE_IS_MORE_PATTERN, self.html)
            
        if more:
            pyfile.url = "http://" + more.group('more')
            self.html = self.load(pyfile.url, decode=True)
            self.logDebug("Changing to Album")
        
        # Find a name for the package
        name = re.search(self.FILE_NAME_PATTERN, self.html)

        if name:
            name = name.group('name')
            h = HTMLParser.HTMLParser()
            name = h.unescape(name)
            #valid_chars = "ƒ‹÷‰¸ˆﬂ!+,;&#-_.() %s%s" % (string.ascii_letters, string.digits)
            #name = ''.join(c for c in name if c in valid_chars)
            invalid_chars = "\/:<>?|*\""
            name = ''.join(c for c in name if c not in invalid_chars)
            self.logDebug(name)
        else:
            self.fail(_("No name was found!"))

        # Determine whether album or gallery
        variant = re.search(self.__pattern__, pyfile.url)
        
        if variant:
            variant = variant.group(1)
        
        # Find links for the package
        if (variant == "gallery"):
            links = re.findall(self.GALLERY_LINK_PATTERN, self.html)
        elif (variant == "a"):
            links = re.findall(self.ALBUM_LINK_PATTERN, self.html)
        else:
            self.fail(_("Wrong URL!"))

        if not links:
            self.fail(_("No Link was found!"))
             
        for i in range(len(links)):
            links[i] = "http://" + links[i]

        self.packages.append((name, links, name))