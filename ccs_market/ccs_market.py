"""
This script allow to translate excel data bill only from Caracas Market 

file: Only an excel file from Caracas makarket

"""

import pandas as pd 
import time

class CcsMarket:
  def __init__(self, file):
    self.file = file

  def to_csv(self):
  # excel file expected
    
    start = time.time()
    if self.file.split('.')[-1] != 'xls' and self.file.split('.')[-1] != 'xlsx':
      raise Exception('Expected an excel file')
    data = pd.read_excel(self.file)
    #Each bill starts with a cell "Codigo" store a list with indexs where there are "Codigo"
    print('Preprosessing Data...')
    casillas_codigo = data[data['INVERSIONES NUEVAVZLA, C.A'] == 'Código'].index
    casillas_codigo -= 1

    #Important informatio to store from bill
    data_dict = {
      'Code':[],
      'Date':[],
      'Product':[],
      'Quantity':[],
      'Price':[]    
    }

    for i in range(len(casillas_codigo)):
      if casillas_codigo[i] == casillas_codigo[-1]:
              data_dict['Code'].append(data.iloc[casillas_codigo[i]]['INVERSIONES NUEVAVZLA, C.A'])
              data_dict['Date'].append(data.iloc[casillas_codigo[i]]['Unnamed: 7'])
              data_dict['Product'].append(data.iloc[casillas_codigo[i]+2]['Unnamed: 3'])
              data_dict['Quantity'].append(data.iloc[casillas_codigo[i]+2]['Unnamed: 10'])
              data_dict['Price'].append(data.iloc[casillas_codigo[i]+2]['Unnamed: 13'])
          
      elif data.iloc[casillas_codigo[i]]['INVERSIONES NUEVAVZLA, C.A'] != 'Número':
          for k in data.iloc[casillas_codigo[i]:casillas_codigo[i+1]]\
                  .where(~data.iloc[casillas_codigo[i]:casillas_codigo[i+1]]['Unnamed: 3'].isnull())['Unnamed: 3']\
                  .where(data.iloc[casillas_codigo[i]:casillas_codigo[i+1]]['Unnamed: 3'] != 'Descripción').dropna().index:
              
              data_dict['Code'].append(data.iloc[casillas_codigo[i]]['INVERSIONES NUEVAVZLA, C.A'])
              data_dict['Date'].append(data.iloc[casillas_codigo[i]]['Unnamed: 7'])
              data_dict['Product'].append(data.iloc[k]['Unnamed: 3'])
              data_dict['Quantity'].append(data.iloc[k]['Unnamed: 10'])
              data_dict['Price'].append(data.iloc[k]['Unnamed: 13'])
      
      else:
          for k in data.iloc[casillas_codigo[i]:casillas_codigo[i+1]].where(~data.iloc[casillas_codigo[i]:casillas_codigo[i+1]]['Unnamed: 3'].isnull())['Unnamed: 3'].where(data.iloc[casillas_codigo[i]:casillas_codigo[i+1]]['Unnamed: 3'] != 'Descripción').dropna().index:
              
              data_dict['Code'].append(data.iloc[casillas_codigo[i-1]]['INVERSIONES NUEVAVZLA, C.A'])
              data_dict['Date'].append(data.iloc[casillas_codigo[i-1]]['Unnamed: 7'])
              data_dict['Product'].append(data.iloc[k]['Unnamed: 3'])
              data_dict['Quantity'].append(data.iloc[k]['Unnamed: 10'])
              data_dict['Price'].append(data.iloc[k]['Unnamed: 13'])
    
    name = self.file.split('.')[0]
  
    name = ''.join(name) + '.csv'
    df = pd.DataFrame(data_dict)
    df.to_csv(name, index=False)
    end = time.time()
    time_ = end - start
    print('Data has been preprocessed succesfully, time: {}s'.format(time_))
