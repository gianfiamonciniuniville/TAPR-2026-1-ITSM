import os


def _connect(role):
    import pyodbc

    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={os.getenv('SQL_SERVER_' + role)};"
        f"DATABASE={os.getenv('SQL_DATABASE_' + role)};"
        f"UID={os.getenv('SQL_USER_' + role)};"
        f"PWD={os.getenv('SQL_PASSWORD_' + role)};"
        "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )
    return pyodbc.connect(conn_str)


def get_source_connection():
    return _connect("SOURCE")


def get_target_connection():
    return _connect("TARGET")
