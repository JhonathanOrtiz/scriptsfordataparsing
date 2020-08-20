"""
The following scripts run only with bills data from Bodegon Shu
WARNING: This script has been created with windows and Vscode the .txt must be encoden in ANSI format
         for me, how ever on Google Colab run with UTF-8 encoding, if you have any trouble try to change
         encoding format. 
"""

import re
import pandas as pd
import time

class Shu:

    def __init__(self, file):

        self.file = file

        with open(file) as f:
            self.data = f.read()

        self.list_ = self.data.split(' ')
        self.cleanned = [word.strip().lower() for word in self.list_ if word != '']      

        #Each bill start with (el) so, if we take the index of this string we know where the bill starts
        self.indices = []
        for idx, word in enumerate(self.cleanned):
            if word == 'el':
                self.indices.append(idx)


    def products_information(self, i):
        """
        i: index
        this functions takes an index and take the corresponding value from inices list (view __init__)
        this list store index too about where start each bill
        return: a dictionary with product, quantity and price
        """
        
        reg = r'^[0-9]*?[(]?[a-z]+[)]?'
        code_reg_1 = r'^[0-9][0-9][0-9]+$'
        code_reg_2 = r'^[a-z]+[-][0-9]$'

        sub_sub_set = []
        sub_indices = []
        product ={

            'producto':[],
            'cantidad':[],
            'precio':[]
        }

        if self.indices[i] == self.indices[-1]:

            for idx, word in enumerate(self.cleanned[self.indices[i]:][34:len(self.cleanned[self.indices[i]:])]):
                if word == 'neto':
                    sub_indices.append(idx+34)
                elif word == 'origen:':
                    sub_indices.append(idx+34)

            for idx, word in enumerate(self.cleanned[self.indices[i]:][sub_indices[0]:sub_indices[1]-1]):
                if re.match(code_reg_1, word) or re.match(code_reg_2, word):
                    sub_sub_set.append(sub_indices[0]+idx)
            sub_sub_set.append(sub_indices[1])

            for j in range(len(sub_sub_set)-1):
                line = self.cleanned[self.indices[i]:][sub_sub_set[j]:sub_sub_set[j+1]]
                nombre = [word.strip() for word in line if re.match(reg,word) and word not in ['und','tasa','origen:','base', 'imponible', 'i.v.a.'] ]
                product['producto'].append(' '.join(nombre))

                for k in range(len(self.cleanned[self.indices[-1]:][sub_sub_set[j]:sub_sub_set[j+1]])):
                    if self.cleanned[self.indices[i]:][sub_sub_set[j]+k] == 'und':
                        product['cantidad'].append(self.cleanned[self.indices[i]:][sub_sub_set[j]+k-1])
                        product['precio'].append(self.cleanned[self.indices[i]:][sub_sub_set[j]+k+1])
            
            return product



        for idx, word in enumerate(self.cleanned[self.indices[i]:self.indices[i+1]][34:len(self.cleanned[self.indices[i]:self.indices[i+1]])]):
            if word == 'neto':
                sub_indices.append(idx+34)
            elif word == 'origen:':
                sub_indices.append(idx+34)

        
        #print(cleanned[indices[i]:indices[i+1]][34:len(cleanned[indices[i]:indices[i+1]])])
        for idx, word in enumerate(self.cleanned[self.indices[i]:self.indices[i+1]][sub_indices[0]:sub_indices[1]-1]):
            if re.match(code_reg_1, word) or re.match(code_reg_2, word):
                sub_sub_set.append(sub_indices[0]+idx)
        sub_sub_set.append(sub_indices[1])
        

        for j in range(len(sub_sub_set)-1):
            #print(' '.join(cleanned[indices[i]:indices[i+1]][sub_sub_set[j]:sub_sub_set[j+1]]))
            line = self.cleanned[self.indices[i]:self.indices[i+1]][sub_sub_set[j]:sub_sub_set[j+1]]
            nombre = [word.strip() for word in line if re.match(reg,word) and word not in ['und','tasa','origen:','base', 'imponible', 'i.v.a.'] ]

            product['producto'].append(' '.join(nombre))
            for k in range(len(self.cleanned[self.indices[i]:self.indices[i+1]][sub_sub_set[j]:sub_sub_set[j+1]])):
                if self.cleanned[self.indices[i]:self.indices[i+1]][sub_sub_set[j]+k] == 'und':
                    product['cantidad'].append(self.cleanned[self.indices[i]:self.indices[i+1]][sub_sub_set[j]+k-1])
                    product['precio'].append(self.cleanned[self.indices[i]:self.indices[i+1]][sub_sub_set[j]+k+1])
      
        return product

    def cliente_name(self, i):

        cliente = []

        if self.indices[i] == self.indices[-1]:
            for a in self.cleanned[self.indices[i]:][21:25]:
            
                if a == 'condic.':
                    break
                else:
                    cliente.append(a)
        
            return ' '.join(cliente)

        else:

            for a in self.cleanned[self.indices[i]:self.indices[i+1]][21:25]:

                if a == 'condic.':
                    break
                else:
                    cliente.append(a)

            return ' '.join(cliente)

    def vendedor_code(self, i):

        vendedor = []
        if self.indices[i] == self.indices[-1]:

            x = self.cleanned[self.indices[i]:][26:34]
        
            for idx,j in enumerate(x):
                if j == 'vendedor:':
                    vendedor.append(x[idx+1])
            return vendedor[0]    

        else:
            x = self.cleanned[self.indices[i]:self.indices[i+1]][26:34]
           
            for idx,j in enumerate(x):
                if j == 'vendedor:':
                    vendedor.append(x[idx+1])
            return vendedor[0]    

    def codigo_compra(self, i):
        if self.indices[i] == self.indices[-1]:
            return self.cleanned[self.indices[i]:][8]
        else:
            return self.cleanned[self.indices[i]:self.indices[i+1]][8]

    def fecha_compra(self, i):
        if self.indices[i] == self.indices[-1]:
            return self.cleanned[self.indices[i]:][18]
        else:
            return self.cleanned[self.indices[i]:self.indices[i+1]][18]

    def identificacion_cliente(self, i):
        if self.indices[i] == self.indices[-1]:
            return self.cleanned[self.indices[i]:][20]
        else:
            return self.cleanned[self.indices[i]:self.indices[i+1]][20]
    
    def to_csv(self):
        start = time.time()
        print('Preprocessing....')
        dicty_data = {
            'Code': [],
            'Date':[],
            'ID':[],
            'Client': [],
            'Teller':[],
            'Product':[],
            'Quantity': [],
            'Price': []
        }

        for i in range(len(self.indices)):
            
            productos = self.products_information(i)
            nombre_productos = productos['producto']
            cantidad_productos = productos['cantidad']
            precio_productos = productos['precio']

            

            if len(nombre_productos) == len(cantidad_productos) == len(precio_productos):
                for j in range(len(nombre_productos)):           
                    dicty_data['Code'].append(self.codigo_compra(i))
                    dicty_data['Date'].append(self.fecha_compra(i))
                    dicty_data['ID'].append(self.identificacion_cliente(i))
                    dicty_data['Client'].append(self.cliente_name(i))
                    dicty_data['Teller'].append(self.vendedor_code(i))
                    dicty_data['Product'].append(nombre_productos[j])
                    dicty_data['Quantity'].append(cantidad_productos[j])
                    dicty_data['Price'].append(precio_productos[j])  


        df = pd.DataFrame(dicty_data)
        filename = str(self.file.split('.')[0]) + '.csv'
        df.to_csv(filename, index=False)
        end = time.time()
        print('Data has been prerprocessed succesfully, time: {}s'.format(end-start))
