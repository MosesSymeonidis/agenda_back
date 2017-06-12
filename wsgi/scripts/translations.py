from app import app
from Models.Translations import Translation


with app.app_context():
    csv = Translation.downloadCSV()
    Translation.importFromCSVFile(csv)
