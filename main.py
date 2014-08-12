#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ExportWXR import *
import unidecode
import re


class MyExportWXR(ExportWXR):
    def __init__(self):
        super().__init__(host="localhost", user="root", password="root", database="dewep")

    def get_articles(self):
        data = []
        with closing( self.db.cursor() ) as cursor:
            cursor.execute("SELECT `id`, `title`, `date` FROM `dewep_blog_articles` WHERE `is_active` = 1;")
            for row in cursor.fetchall():
                slug = unidecode.unidecode(row["title"])
                slug = re.sub(r'\W+', '-', slug)
                subdata = dict()
                subdata["id"] = row["id"]
                subdata["title"] = row["title"]
                subdata["link"] = "http://www.dewep.net/Blog/Article-%d/%s" % (row["id"], slug)
                subdata["date"] = row["date"]
                subdata["status"] = "open"
                data.append(subdata)
        return data

    def get_comments(self, id_article):
        data = []
        with closing( self.db.cursor() ) as cursor:
            cursor.execute("SELECT `id`, `date`, `email`, `name`, `website`, `content`, `ip`, `is_active` FROM `dewep_blog_commentaires` WHERE `id_article` = %d;" % id_article)
            for row in cursor.fetchall():
                subdata = dict()
                subdata["id"] = row["id"]
                subdata["author_name"] = row["name"]
                subdata["author_email"] = row["email"]
                subdata["author_website"] = row["website"]
                subdata["author_ip"] = row["ip"]
                subdata["date"] = row["date"]
                subdata["content"] = row["content"]
                subdata["approved"] = row["is_active"]
                subdata["parent"] = "0"
                data.append(subdata)
        return data


with MyExportWXR() as export:
    export.xml_open()
    export.xml_content()
    export.xml_close()


