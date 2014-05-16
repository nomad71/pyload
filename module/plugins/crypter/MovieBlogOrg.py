# -*- coding: utf-8 -*-

import re
import random
from module.plugins.Crypter import Crypter

class MovieBlogOrg(Crypter):
    __name__ = "MovieBlogOrg"
    __type__ = "crypter"
    __pattern__ = r'http://(?:www\.)?(movie-blog.org)/\d*/.*?'
    __version__ = "0.02"
    __config__ = [("randomPreferred", "bool", "Randomize Preferred-List", False),
                  ("hosterListMode", "OnlyOne;OnlyPreferred(One);OnlyPreferred(All);All",
                   "Use for hosters (if supported)", "All"),
                  ("hosterList", "str", "Preferred Hoster list (comma separated)",
                   "ShareOnlineBiz,UploadedNet,UploadedTo,FiredriveCom,ZippyshareCom,NetloadIn,RapidshareCom"),
                  ("ignoreList", "str", "Ignored Hoster list (comma separated)", "MegauploadCom"),
                  ("loadImage", "bool", "Load Image", True)]
    __description__ = """Movie-Blog.org decrypter plugin"""
    __author_name__ = ("nomad71")
    __author_mail__ = ("nomad71REMOVETHIS@gmx.net")

    FOLDER_NAME_PATTERN = r'<span class="?item"?><span class="?fn"?>(?P<name>.*)<\/span><\/a>'
    LINK_PATTERN = r'<strong>.*<\/strong>\s*<a target="?_blank"? href="?(?P<url>.*?)"? >(?P<hoster>.*)<\/a><br[>| \>]'
    IMAGE_PATTERN = r'<p><img(?:.*) src=[\'\"]?(?P<image>.*?)[ \'\"](?:.*)?>'
    
    
    def setup(self):
        self.multiDL = True

    def decrypt(self, pyfile):
        self.html = self.load(pyfile.url, decode=True)

        #find package name and folder
        name = folder = re.search(self.FOLDER_NAME_PATTERN, self.html)
        if name:
            name = name.group('name')
            self.logDebug('name: ' + name)
        else:
            name = "MovieBlogOrg"
            self.logDebug('No name or folder found! \'MovieBlogOrg\' used instead.')

        links = re.findall(self.LINK_PATTERN, self.html)
        if links:
            preferredList = self.getpreferred(links)
        else:
            self.fail(_("No Hoster was found"))

        if len(preferredList) == 0:
            self.fail(_("No Hoster matched your criteria. Please adjust your settings"))    

        #find cover image (optional)
        if self.getConfig("loadImage"):
            image = re.search(self.IMAGE_PATTERN, self.html)
            if image:
                image = image.group('image')
                preferredList.append(image)
                self.logDebug('image: ' + image)
            else:
                self.logDebug('No Image found!')

        self.logDebug("preferredList: " + str(preferredList))

        self.packages.append((name, preferredList, name))

    #taken and modified from SerienjunkiesOrg plugin.
    #selects the preferred hoster, after that selects any hoster (ignoring the one to ignore)
    def getpreferred(self, hosterlist):

        result = []
        preferredList = self.getConfig("hosterList").strip().lower().replace(
            '|', ',').replace('-', '').replace('.', '').replace(';', ',').split(',')
        if (self.getConfig("randomPreferred") is True) and (
                self.getConfig("hosterListMode") in ["OnlyOne", "OnlyPreferred(One)"]):
            random.shuffle(preferredList)
            # we don't want hosters be read two times
        hosterlist2 = hosterlist[:] #copy the list

        for preferred in preferredList:
            for Hoster in hosterlist:
                if preferred == Hoster[1].lower().replace('.', '').replace('-', ''):
                    self.logDebug("selected " + Hoster[1])
                    result.append(str(Hoster[0]))
                    del (hosterlist2[hosterlist2.index(Hoster)])
                    if self.getConfig("hosterListMode") in ["OnlyOne", "OnlyPreferred(One)"]:
                        return result

        ignorelist = self.getConfig("ignoreList").strip().lower().replace(
            '|', ',').replace('-', '').replace('.', '').replace(';', ',').split(',')
        if self.getConfig('hosterListMode') in ["OnlyOne", "All"]:
            for Hoster in hosterlist2:
                if Hoster[1].strip().lower().replace('.', '').replace('-', '') not in ignorelist:
                    self.logDebug("selected2 " + Hoster[1])
                    result.append(str(Hoster[0]))
                    if self.getConfig('hosterListMode') == "OnlyOne":
                        return result
        return result
