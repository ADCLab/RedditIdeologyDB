import pandas as pd


df = pd.read_csv (r'Path where the CSV file is saved\File Name.csv')
df.to_json (r'Path where the new JSON file will be stored\New File Name.json')