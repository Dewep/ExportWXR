#!/usr/bin/python3.4
# -*- coding: utf-8 -*-

import pymysql
from contextlib import closing


class ExportWXR(object):
    def __init__(self, host, user, password, database):
        self.db = connection = pymysql.connect(host, user, password, database, cursorclass=pymysql.cursors.DictCursor)
        with closing( self.db.cursor() ) as cursor:
            cursor.execute("SET character_set_client='utf8'")
            cursor.execute("SET character_set_results='utf8'")
            cursor.execute("SET collation_connection='utf8_general_ci'")

    def __enter__(self):
        return self

    """
    Must be override. The response format:
    [
        {
            "id": ..., # Identifier
            "title": ..., # Title
            "link": ..., # URL
            "date": ..., # Date (format: Y-m-d H:i:s)
            "status": ... # Status ("open" or "closed")
        },
        ...
    ]
    """
    def get_articles(self):
        return []

    """
    Must be override. The response format:
    [
        {
            "id": ..., # Identifier
            "author_name": ..., # Name of author
            "author_email": ..., # Email of author
            "author_website": ..., # Website of author
            "author_ip": ..., # IP of author
            "date": ..., # Date
            "content": ..., # Content
            "approved": ..., # Approved (0 ou 1)
            "parent": ... # Parent identifier (0 if no parent)
        },
        ...
    ]
    """
    def get_comments(self, ref_article):
        return []

    def xml_open(self):
        print('<?xml version="1.0" encoding="UTF-8"?>')
        print('<rss version="2.0"')
        print('  xmlns:content="http://purl.org/rss/1.0/modules/content/"')
        print('  xmlns:dsq="http://www.disqus.com/"')
        print('  xmlns:dc="http://purl.org/dc/elements/1.1/"')
        print('  xmlns:wp="http://wordpress.org/export/1.0/">')
        print('  <channel>')

    def xml_content(self):
        articles = self.get_articles()
        for article in articles:
            comments = self.get_comments(article["id"])
            print('    <item>')
            print('      <title>%s</title>' % article["title"])
            print('      <link>%s</link>' % article["link"])
            print('      <dsq:thread_identifier>%s</dsq:thread_identifier>' % article["id"])
            print('      <wp:post_date_gmt>%s</wp:post_date_gmt>' % article["date"])
            print('      <wp:comment_status>%s</wp:comment_status>' % article["status"])
            for comment in comments:
                print('      <wp:comment>')
                print('        <wp:comment_id>%d</wp:comment_id>' % comment["id"])
                print('        <wp:comment_author>%s</wp:comment_author>' % comment["author_name"])
                print('        <wp:comment_author_email>%s</wp:comment_author_email>' % comment["author_email"])
                print('        <wp:comment_author_url>%s</wp:comment_author_url>' % comment["author_website"])
                print('        <wp:comment_author_IP>%s</wp:comment_author_IP>' % comment["author_ip"])
                print('        <wp:comment_date_gmt>%s</wp:comment_date_gmt>' % comment["date"])
                print('        <wp:comment_content><![CDATA[%s]]></wp:comment_content>' % comment["content"].replace("]]>", "]]]]><![CDATA[>"))
                print('        <wp:comment_approved>%s</wp:comment_approved>' % comment["approved"])
                print('        <wp:comment_parent>%s</wp:comment_parent>' % comment["parent"])
                print('      </wp:comment>')
            print('    </item>')

    def xml_close(self):
        print('  </channel>')
        print('</rss>')

    def __exit__(self, type, value, traceback):
        self.db.close()


