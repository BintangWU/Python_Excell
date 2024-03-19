from data_base import Data_Base
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional
import datetime

'''
BIN UNBIN CONTR
{
    "reqCode": {{$timestamp}},
    "ctnrTyp": "3",
    "stgBinCode": "111111ME501013",
    "indBind": "1"
}

BIN UNBIN POD
{
    "reqCode": {{$timestamp}},
    "reqTime": "",
    "clientCode": "",
    "tokenCode": "",
    "podCode": "101010",
    "positionCode": "055070ME067000",
    "podDir": "0",
    "indBind": "1"
}
'''

db = Data_Base('./workstation.xls')
app = FastAPI()

class POD(BaseModel):
    reqCode: Optional[str] = "Star" + datetime.datetime.now().strftime("%H:%M:%S-%a, %d %B %Y")
    podCode: Optional[str] = ""
    clientCode: Optional[str] = ""
    tokenCode: Optional[str] = ""
    podCode: str
    positionCode: str
    podDir: Optional[str] = ""
    indBind: str

class CONTR(BaseModel):
    reqCode: Optional[str] = "Star" + datetime.datetime.now().strftime("%H:%M:%S-%a, %d %B %Y")
    podCode: Optional[str] = ""
    ctnrTyp: str
    stgBinCode: str
    indBind: str

class BIN_UNBIN(BaseModel ):
    positionName: list[str] = []
    sheet: str
    indBind: str


@app.get('/positionCode')
async def all_pos_code(sheet: Optional[str] = None):
    raw = db.raw_data()
    sheetName = list(raw.keys())
    dictPosition = {}
    position = [[] for _ in range(len(sheetName))]
    
    for i in range(len(sheetName)): 
        for j in range(len(raw[f'{sheetName[i]}'])):
            position[i].append([raw[f'{sheetName[i]}']['position name'][j], raw[f'{sheetName[i]}']['position code'][j]])
        dictPosition.update({sheetName[i]: position[i]})

    if sheet in sheetName or sheet == None:
        return {'station': sheet.lower() if sheet in sheetName else 'all', 'position': dictPosition[f'{sheet.lower()}'] if sheet in sheetName else dictPosition, 'msg': 'ok'}
    else:
        return {'station': None, 'position': None,'msg': 'err'}

@app.get('/positionCode/find')
async def find_pos_code(positionName: str, sheet: Optional[str] = 'storage'):
    val = db.get_position_code(positionName, sheet)
    return {'name': positionName.upper(), 'position': val, 'msg': 'ok' if val != None else 'err'}

@app.post('/bin-unbin-pod')
async def bin_unbin_pod(body: BIN_UNBIN):    
    positionName_number_1 = int(body.positionName[0][0:2])
    positionName_idx_1 = int(body.positionName[0][-1])
    sheet = body.sheet.lower()
    processFinish = False
    
    if len(body.positionName) > 1:
        positionName_number_2 = int(body.positionName[1][0:2])
        positionName_idx_2 = int(body.positionName[1][-1])
        
        if (positionName_number_1 <= positionName_number_2) and (positionName_idx_1 <= positionName_idx_2):
            positionData = db.get_range_position_code(body.positionName[0].upper(), body.positionName[1].upper(), sheet)
        else:
            positionData = None
    else:
        positionData = db.get_position_code(body.positionName[0], sheet)
    
    for i in range(len(positionData)):
        print(POD(podCode=positionData[i][0], positionCode=positionData[i][1], indBind=body.indBind).model_dump())
    # print(POD(positionCode='oko', podCode='iui', indBind='9'))
    
    return {'action': 'binPod' if int(body.indBind) is 1 else 'unbinPod', 'position': positionData, 'msg': 'ok' if positionData != None else 'err'}
        
        
    
    

