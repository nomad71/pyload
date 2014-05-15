# -*- coding: utf-8 -*-
############################################################################
# This program is free software: you can redistribute it and/or modify     #
# it under the terms of the GNU Affero General Public License as           #
# published by the Free Software Foundation, either version 3 of the       #
# License, or (at your option) any later version.                          #
#                                                                          #
# This program is distributed in the hope that it will be useful,          #
# but WITHOUT ANY WARRANTY; without even the implied warranty of           #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
# GNU Affero General Public License for more details.                      #
#                                                                          #
# You should have received a copy of the GNU Affero General Public License #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
############################################################################

import re

from module.plugins.internal.SimpleHoster import SimpleHoster, create_getInfo

class NineGagCom(SimpleHoster):
    __name__ = "NineGagCom"
    __type__ = "hoster"
    __pattern__ = r'http:\/\/(?:www\.)?9gag\.com\/gag\/\w+'
    __version__ = "0.01"
    __description__ = """9Gag.com hoster plugin"""
    __author_name__ = ("nomad71")
    __author_mail__ = ("nomad71REMOVETHIS@gmx.net")

    FILE_NAME_PATTERN = r'<title>(?P<name>.*) - 9GAG<\/title>'
    LINK_PATTERN = r'<link rel="image_src" href="(?P<link>.*)" \/>'
    GIF_PATTERN = r'<img class="badge-item-animated-img" \n\s*src=\"(?P<gif>.*)\"'
    FILE_OFFLINE_PATTERN = r'<p>Sorry, the page you\'re looking for doesn\'t exist.</p>'

    def setup(self):
        self.multiDL = True

    def process(self, pyfile):
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
        
        self.pyfile.name = name + "." + link.split('.')[-1]
        
        self.logDebug(self.pyfile.name)
        
        self.download(link)
