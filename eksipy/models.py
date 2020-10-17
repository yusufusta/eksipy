# Unofficial Ekşi Sözlük private API.

# Copyright (C) 2020 Yusuf Usta
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from unidecode import unidecode
import re
from markdownify import markdownify as md

class Model(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

class Message(Model):
    id = None
    from_user = None
    message = None
    preview = None
    date = None
    read = None
    unread = None
    thread_id = None

class MessageHistory(Model):
    incoming = None
    outgoing = None
    message = None
    date = None

class Topic(Model):
    id = None
    title = None
    giri = None
    current_page = None
    max_page = None

    def url(self):
        if id == None:
            return f'https://eksisozluk.com/?q={self.title}'
        else:
            bosluk = unidecode(self.title).replace(" ", "-")
            baslik = re.sub('[^A-Za-z0-9-]+', '', bosluk)
            return f'https://eksisozluk.com/{baslik}--{self.id}'

    def slug(self):
        bosluk = unidecode(self.title).replace(" ", "-")
        baslik = re.sub('[^A-Za-z0-9-]+', '', bosluk)
        return baslik

    def __str__(self):
        if id == None:
            return f'https://eksisozluk.com/?q={self.title}'
        else:
            bosluk = unidecode(self.title).replace(" ", "-")
            baslik = re.sub('[^A-Za-z0-9-]+', '', bosluk)
            return f'https://eksisozluk.com/{baslik}--{self.id}'

class Entry(Model):
    id = None
    author = None
    entry = None
    date = None
    edited = None
    fav = None
    author_id = None
    comment = None
    topic = None

    def dict(self):
        return {
            'id': self.id, 
            'author': self.author, 
            'author_id': self.author_id,
            'fav': self.fav,
            'comment': self.comment,
            'entry': self.entry
        }

    def url(self):
        return f'https://eksisozluk.com/entry/{self.id}'

    def text(self):
        return self.entry.get_text().strip()
    
    def html(self):
        return self.entry()

    def md(self):
        return md(str(self.entry))[1:]

    def __str__(self):
        return md(str(self.entry).strip())[1:]

class User(Model):
    id = None
    nick = None
    total_entry = None
    last_month = None
    last_week = None
    today = None
    last_entry = None
    pinned_entry = None
    badges = []

    def url(self):
        return f'https://eksisozluk.com/biri/{self.nick}'
    def __str__(self):
        return f'https://eksisozluk.com/biri/{self.nick}'