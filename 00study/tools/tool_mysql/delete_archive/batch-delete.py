import subprocess
import re
import time


def delete():
    delete_stmt = [
        "mysql",
        "-h",
        "...",
        "-u",
        "...",
        "--password=...",
        "table_abc",
        "--skip-column-names",
        "-e",
        "delete from ... where ...;",
        "-vvv",
    ]

    result = subprocess.run(delete_stmt, stdout=subprocess.PIPE)
    output = result.stdout.decode("utf-8")

    print(output)

    match = re.search(r"(\d*) rows affected", output)
    _affected_rows = int(match.group(1))
    return _affected_rows


affected_rows = 1000

while affected_rows > 0:
    affected_rows = delete()
    time.sleep(2)
