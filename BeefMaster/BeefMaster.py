"""
This Script is only for data parsing for Bodegon Beef Masters.
Expected an excel file
If the Bodegon changes your billing format this script doesn't work
"""
import pandas as pd
import time

class BeefMaster:
    def __init__(self, file):
        if file.split('.')[-1] != 'xls' and file.split('.')[-1] != 'xlsx':
            raise Exception('Expected Excel format given {}'.format(file.split('.')[-1])) 
        self.file = file
        self.data = pd.read_excel(file)
        self.indices =  self.data[self.data['Fecha Emisión'] == '-'].index
    
    def to_csv(self):
        start = time.time()
        print('Preprocessing Data...')

        dicty_data = {
            'Code': [],
            'Date': [],
            'ID': [],
            'Name': [],
            'Product':[],
            'Quantity':[],
            'Price':[]
        }

        for i in range(len(self.indices)):

            if self.indices[i] == self.indices[-1]:
                bill     = self.data.iloc[self.indices[i]:]
                products = [str(item).strip().lower() for item in bill['Unnamed: 3'][2:] if str(item) != 'nan']
                codes    = [item for item in bill['Unnamed: 1'][2:] if str(item)!= 'nan']
                qty      = [str(item) for item in bill['Unnamed: 10'][2:-2] if str(item) != 'nan']
                price    = [str(item) for item in bill['Unnamed: 12'][2:-2] if str(item) != 'nan']
            
                if len(products) == len(codes) == len(qty) == len(price):
                    for j in range(len(products)):
                        dicty_data['Name'].append(bill['Nombre'][self.indices[i]].strip().lower())
                        dicty_data['ID'].append(bill['Código'][self.indices[i]])
                        dicty_data['Date'].append(bill['Unnamed: 1'][self.indices[i]])
                        dicty_data['Product'].append(products[j])
                        dicty_data['Code'].append(codes[j])
                        dicty_data['Quantity'].append(qty[j])
                        dicty_data['Price'].append(price[j])


            else:
            #if index is not the last index

                bill     = self.data.iloc[self.indices[i]:self.indices[i+1]]
                products = [str(item).strip().lower() for item in bill['Unnamed: 3'][2:] if str(item) != 'nan']
                codes    = [item for item in bill['Unnamed: 1'][2:] if str(item)!= 'nan']
                qty      = [str(item) for item in bill['Unnamed: 10'][2:-1] if str(item) != 'nan']
                price    = [str(item) for item in bill['Unnamed: 12'][2:-1] if str(item) != 'nan']
                
                if len(products) == len(codes) == len(qty) == len(price):
                    for j in range(len(products)):
                        dicty_data['Name'].append(bill['Nombre'][self.indices[i]].strip().lower())
                        dicty_data['ID'].append(bill['Código'][self.indices[i]])
                        dicty_data['Date'].append(bill['Unnamed: 1'][self.indices[i]])
                        dicty_data['Product'].append(products[j])
                        dicty_data['Code'].append(codes[j])
                        dicty_data['Quantity'].append(qty[j])
                        dicty_data['Price'].append(price[j])
                
        df = pd.DataFrame(dicty_data)
        filename = self.file.split('.')[0] + str('.csv')
        df.to_csv(filename, index = False)
        end = time.time()
        time_ = (end - start)
        print('Data has been preprocessed succesfully, time: {}s'.format(time_))
