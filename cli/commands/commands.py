#!/usr/bin/env python3

import pandas as pd
import sqlite3

from nubia import argument, command


@command("show")
class ShowCommand:
    def __init__(self) -> None:
        self.file = "/tmp/ngx-stats.db"
        self.conn = sqlite3.connect(self.file)

    @command("filter-by-visitor")
    @argument("vhost", description="Virtual host")
    @argument("overall", description="The sum of visitors per virtual host")
    def visitors(self, vhost: str, overall: bool = False):
        """
        Get stats for a specified virtual host
        """
        query = "SELECT timestamp, vhost, visitors FROM stats WHERE vhost = '{}' ORDER BY timestamp DESC LIMIT 10".format(
            vhost
        )
        if overall:
            query = "SELECT timestamp, vhost, SUM(visitors) as visitors FROM stats WHERE vhost = '{}' ORDER BY timestamp DESC LIMIT 10".format(
                vhost
            )
        df = pd.read_sql_query(
            query,
            self.conn,
        )
        data = pd.DataFrame(df)
        data["timestamp"] = pd.to_datetime(data["timestamp"], unit="s")
        self.conn.close()
        print(data)

    @command("show-topn-virtual-hosts")
    @argument("topn", description="The number of TopN to show")
    @argument("overall", description="The sum of visitors per virtual host")
    def topn(self, topn: int, overall: bool = False):
        """
        Get TopN virtual hosts by visitors
        """
        query = "SELECT timestamp, vhost, visitors FROM stats ORDER BY visitors DESC LIMIT {}".format(
            topn
        )
        if overall:
            query = "SELECT timestamp, vhost, SUM(visitors) as visitors FROM stats GROUP BY vhost ORDER BY visitors DESC LIMIT {}".format(
                topn
            )
        df = pd.read_sql_query(
            query,
            self.conn,
        )
        df = pd.read_sql_query(query, self.conn)
        data = pd.DataFrame(df)
        data["timestamp"] = pd.to_datetime(data["timestamp"], unit="s")
        self.conn.close()
        print(data)
