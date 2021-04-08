#!/usr/bin/python
# -*- coding: utf8 -*-

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

import re
import html
from typing import List


class Model(object):
    def __init__(self, client, **kwargs):
        self.client = client
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

    def __init__(self, client, **kwargs):
        super().__init__(client, **kwargs)


class MessageHistory(Model):
    incoming = None
    outgoing = None
    message = None
    date = None


class Entry(Model):
    id = None
    author = None
    topic = None
    entry = None
    date = None
    edited = None
    fav_count = None
    comment = None

    def dict(self):
        return self.__dict__

    def url(self):
        return f'https://eksisozluk.com/entry/{self.id}'

    def text(self):
        """
        Entry yazı haline çevirir.
        """

        _ = self.entry.html()
        linkler = self.entry("a")
        for link in linkler.items():
            if link.attr('class') == "b":
                _ = _.replace(html.unescape(link.outerHtml()),
                              f"`{link.text()}`")
                continue
            _ = _.replace(link.outerHtml(),
                          f"[{link.attr('href')} {link.text()}]")
            _ = html.unescape(_).replace("<br/>", "\n")
        return _

    def html(self):
        return self.entry.html()

    def __str__(self):
        return self.text()  # md(str(self.entry).strip())[1:]

    def fav(self) -> int:
        """
        Entry favoriler.
        """

        return self.client.favEntry(self)

    def unfav(self) -> int:
        """
        Entry favorisi kaldırır.
        """

        return self.client.unfavEntry(self)

    def delete(self) -> bool:
        """
        Entry siler.
        """

        return self.client.deleteEntry(self)

    def up(self) -> bool:
        """
        Entry upvote atar.
        """

        return self.client.upVoteEntry(self)

    def down(self) -> bool:
        """
        Entry downvote atar.
        """

        return self.client.downVoteEntry(self)


class Topic(Model):
    id = None
    title = None
    giri = None
    current_page = None
    max_page = None
    slug = None
    url = None

    async def getUrl(self):
        """
        Başlığın adresini getirir.
        """

        if self.url == None:
            return (await self.client.convertToTopic(self.title))
        else:
            return self.url

    def dict(self):
        return self.__dict__

    def __str__(self):
        return self.title

    def __init__(self, client, **kwargs):
        super().__init__(client, **kwargs)

    def getEntrys(self, page=1, day=None, sukela=None) -> List[Entry]:
        """
        Başlığın entrylerini getirir.
        """

        return self.client.getEntrys(self, page, day, sukela)

    def sendEntry(self, entry: str, hidden: bool = False) -> Entry:
        """
        Entry gönderir.
        """

        return self.client.sendEntry(self, entry, hidden)


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
