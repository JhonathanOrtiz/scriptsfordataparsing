import pandas as pd
import time

class LeMarche:

  def __init__(self, file):
    self.file = file
    self.data = pd.read_excel(file)
    self.indices = [(idx -1) for idx in self.data['INVERSIONES MR CLAUS, C.A.'].index if str(self.data['INVERSIONES MR CLAUS, C.A.'][idx]).strip() == 'Código']

  def to_csv(self):
    print('Preprocessing...')
    start = time.time()
    dicty_data = {
      'Date': [],
      'Client': [],
      'Product': [],
      'Quantity': [],
      'Price': []
    }

    black_list = ['Total Items ...', 'Descripción', 'nan']

    for i in range(len(self.indices)):

      if self.indices[i] == self.indices[-1]:

        bill = self.data.iloc[self.indices[i]:]

        dicty_data['Date'].append(bill['INVERSIONES MR CLAUS, C.A.'][self.indices[i]])
        dicty_data['Client'].append(bill['Unnamed: 4'][self.indices[i]])
        dicty_data['Product'].append([str(item) for item in bill['Unnamed: 5'] if str(item).strip() not in black_list])
        dicty_data['Quantity'].append([item for item in bill['Unnamed: 14'] if str(item) != 'nan'])
        dicty_data['Price'].append([item for item in bill['Unnamed: 18'] if str(item) != 'nan'])
        
      else:

        bill = self.data.iloc[self.indices[i]:self.indices[i+1]]

        dicty_data['Date'].append(bill['INVERSIONES MR CLAUS, C.A.'][self.indices[i]])
        dicty_data['Client'].append(bill['Unnamed: 4'][self.indices[i]])
        dicty_data['Product'].append([str(item) for item in bill['Unnamed: 5'] if str(item).strip() not in black_list])
        dicty_data['Quantity'].append([item for item in bill['Unnamed: 14'] if str(item) != 'nan'])
        dicty_data['Price'].append([item for item in bill['Unnamed: 18'] if str(item) != 'nan'])

    df = pd.DataFrame(dicty_data)
    filename = self.file.split('.')[0] + '.csv'
    df.to_csv(filename, index = False)
    end = time.time()
    print('Preprocessed has been succesfully, time {}s'.format(end-start))

