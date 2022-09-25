import pandas as pd

class FileManager:
        
        @staticmethod
        def read_from_excel(file_name, sheet_name):
                data = pd.read_excel (r'Data/'+file_name, sheet_name=sheet_name)
                return data
