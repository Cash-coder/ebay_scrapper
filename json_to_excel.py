JSON_FILE = 'ebay-spider-output.json'
EXCEL_FILE = 'ebay_spider_excel.xlsx'

def json_to_excel(json_file, excel_file='json_to_excel.xlsx'):
    import pandas
    pandas.read_json(json_file).to_excel(excel_file)

json_to_excel(JSON_FILE, EXCEL_FILE)