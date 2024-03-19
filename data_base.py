import pandas as pd
from typing import Optional

class Data_Base():
    def __init__(self, file_name: str) -> None:
        self._df = pd.read_excel(file_name, sheet_name=None, usecols='A:B')
        self._find = False
        self._lock_find = False

    
    def raw_data(self, sheet: Optional[str] = None):
        if sheet == None:
            return self._df
        else:
            return self._df[sheet.lower()].values
    
    def get_position_code(self, positionName: str, sheet: str,) -> str:
        self._find = False
        raw_data = self._df[sheet.lower()].values
        
        for i in range(len(raw_data)):
            if raw_data[i][0].lower() == positionName.lower():
                # print(f'Match: {raw_data[i]}')
                self._find = False
                return [raw_data[i][0], raw_data[i][1]]
        
        if not self._find:
            return None
        
    def get_range_position_code(self, positionName_1: str, positionName_2: str, sheet: str) -> list:
        self._find = False
        raw_data = self._df[sheet.lower()].values
        positionCode_range = []
        
        for i in range(len(raw_data)):
            if raw_data[i][0].lower() == positionName_1.lower():
                self._find = True
            elif raw_data[i][0].lower() == positionName_2.lower():
                positionCode_range.append([raw_data[i][0], raw_data[i][1]])
                self._find = False
                
            if self._find:
                # position name, position code
                positionCode_range.append([raw_data[i][0], raw_data[i][1]])
        return positionCode_range

if __name__ == '__main__':
    db = Data_Base('./workstation.xls')
    
    val = db.get_range_position_code('04stg1', '04stg4', 'storage')
    print(val)



    