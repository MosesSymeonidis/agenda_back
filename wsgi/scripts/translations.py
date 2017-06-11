from app import app
import os
import click
from flask.cli import FlaskGroup
from Models.Translations import Translation


with app.app_context():
    Translation.importFromCSV()
