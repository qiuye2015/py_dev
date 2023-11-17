"""
git@github.com:opensafely/hiv-research.git
"""
import time
from urllib.parse import unquote, urlparse

import prestodb
import requests


def presto_connection_from_url(url):
    return ConnectionProxy(
        prestodb.dbapi.connect(**presto_connection_params_from_url(url))
    )


def presto_connection_params_from_url(url):
    parsed = urlparse(url)
    parts = parsed.path.strip("/").split("/")
    if len(parts) != 2 or not all(parts) or parsed.scheme != "presto":
        raise ValueError(
            f"Presto URL not of the form 'presto://host.name/catalog/schema': {url}"
        )
    catalog, schema = parts
    connection_params = {
        "host": parsed.hostname,
        "port": parsed.port or 8080,
        "catalog": catalog,
        "schema": schema,
    }
    if parsed.username:
        user = unquote(parsed.username)
        password = unquote(parsed.password)
        connection_params.update(
            user=user, auth=prestodb.auth.BasicAuthentication(user, password)
        )
    else:
        connection_params["user"] = "ignored"
    return connection_params


def wait_for_presto_to_be_ready(url, test_query, timeout):
    """
    Waits for Presto to be ready to execute queries by repeatedly attempting to
    connect and run `test_query`, raising the last received error after
    `timeout` seconds
    """
    connection_params = presto_connection_params_from_url(url)
    start = time.time()
    while True:
        try:
            connection = prestodb.dbapi.connect(**connection_params)
            cursor = connection.cursor()
            cursor.execute(test_query)
            cursor.fetchall()
            break
        except (
                prestodb.exceptions.PrestoQueryError,
                requests.exceptions.ConnectionError,
        ):
            if time.time() - start < timeout:
                time.sleep(1)
            else:
                raise


class ConnectionProxy:
    """Proxy for prestodb.dbapi.Connection, with a more useful cursor.
    """

    def __init__(self, connection):
        self.connection = connection

    def __getattr__(self, attr):
        """Pass any unhandled attribute lookups to proxied connection."""

        return getattr(self.connection, attr)

    def cursor(self):
        """Return a proxied cursor."""

        return CursorProxy(self.connection.cursor())


class CursorProxy:
    """Proxy for prestodb.dbapi.Cursor.

    Unlike prestodb.dbapi.Cursor:

    * any exceptions caused by an invalid query are raised by .execute() (and
      not later when you fetch the results)
    * the .description attribute is set immediately after calling .execute()
    * you can iterate over it to yield rows
    * .fetchone()/.fetchmany()/.fetchall() are disabled (they are not currently
      used by ACMEBackend, although they could be implemented if required)
    """

    _rows = None

    def __init__(self, cursor, batch_size=10 ** 6):
        """Initialise proxy.

        cursor: the presto.dbapi.Cursor to be proxied
        batch_size: the number of records to fetch at a time (this will need to
            be tuned)
        """

        self.cursor = cursor
        self.batch_size = batch_size

    def __getattr__(self, attr):
        """Pass any unhandled attribute lookups to proxied cursor."""

        return getattr(self.cursor, attr)

    def execute(self, *args, **kwargs):
        """Execute a query/statement and fetch first batch of results.

        This:

        * triggers any exceptions caused by the query/statement
        * populates the .description attribute of the cursor
        """

        self.cursor.execute(*args, **kwargs)
        self._rows = self.cursor.fetchmany()

    def __iter__(self):
        """Iterate over results."""

        while self._rows:
            yield from iter(self._rows)
            self._rows = self.cursor.fetchmany(self.batch_size)

    def fetchone(self):
        raise RuntimeError("Iterate over cursor to get results")

    def fetchmany(self, size=None):
        raise RuntimeError("Iterate over cursor to get results")

    def fetchall(self):
        raise RuntimeError("Iterate over cursor to get results")


# FJP
import csv
import datetime
import os
import re
import uuid

# Characters that are safe to interpolate into SQL (see
# `placeholders_and_params` below)
safe_punctation = r"_.-"
SAFE_CHARS_RE = re.compile(f"^[a-zA-Z0-9{re.escape(safe_punctation)}]+$")


class Backend:
    _db_connection = None
    _current_column_name = None

    def __init__(self, database_url, queries):
        self.database_url = database_url
        self.queries = queries

    def log(self, message):
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        print(f"[{timestamp}] {message}")

    def get_db_connection(self):
        if self._db_connection:
            return self._db_connection
        self._db_connection = presto_connection_from_url(self.database_url)
        return self._db_connection

    def to_csv(self, filename):
        result = self.execute_query()
        unique_check = UniqueCheck()
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([x[0] for x in result.description])
            for row in result:
                unique_check.add(row[0])
                writer.writerow(row)
        unique_check.assert_unique_ids()

    def to_dicts(self):
        result = self.execute_query()
        keys = [x[0] for x in result.description]
        # Convert all values to str as that's what will end in the CSV
        output = [dict(zip(keys, map(str, row))) for row in result]
        unique_check = UniqueCheck()
        for item in output:
            unique_check.add(item["patient_id"])
        unique_check.assert_unique_ids()
        return output

    def to_sql(self):
        """
        Generate a single SQL string.

        Useful for debugging, optimising, etc.
        """
        prepared_sql = ["-- Create codelist tables"]
        for name, query in self.queries:
            prepared_sql.append(f"-- Query for {name}")
            prepared_sql.append(f"{query};\n\n")
        return "\n".join(prepared_sql)

    def execute_query(self):
        cursor = self.get_db_connection().cursor()
        queries = list(self.queries)
        final_query = queries.pop()[1]
        for name, sql in queries:
            self.log(f"Running query: {name}")
            cursor.execute(sql)
        output_table = self.get_output_table_name(os.environ.get("TEMP_DATABASE_NAME"))
        if output_table:
            self.log(f"Running final query and writing output to '{output_table}'")
            sql = f"CREATE TABLE {output_table} AS {final_query}"
            cursor.execute(sql)
            self.log(f"Downloading data from '{output_table}'")
            cursor.execute(f"SELECT * FROM {output_table}")
        else:
            self.log(
                "No TEMP_DATABASE_NAME defined in environment, downloading results "
                "directly without writing to output table"
            )
            cursor.execute(final_query)
        return cursor

    def get_output_table_name(self, temporary_database):
        if not temporary_database:
            return
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")
        return f"{temporary_database}..Output_{timestamp}"

    def get_temp_table_prefix(self):
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime(
            "%Y%m%d_%H%M%S"
        )
        return f"_{timestamp}_{uuid.uuid4().hex}"


class UniqueCheck:
    def __init__(self):
        self.count = 0
        self.ids = set()

    def add(self, item):
        self.count += 1
        self.ids.add(item)

    def assert_unique_ids(self):
        duplicates = self.count - len(self.ids)
        if duplicates != 0:
            raise RuntimeError(f"Duplicate IDs found ({duplicates} rows)")
