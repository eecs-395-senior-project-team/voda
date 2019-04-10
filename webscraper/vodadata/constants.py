"""
Constants defining the access information for the database.
"""
import os


DBNAME = os.environ['POSTGRES_DB']
USER = os.environ['POSTGRES_USER']
PASSWORD = os.environ['POSTGRES_PASSWORD']
HOST = os.environ['POSTGRES_HOST']
PORT = os.environ['POSTGRES_PORT']
