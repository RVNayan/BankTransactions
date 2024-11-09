import numpy as np


def Total_amount(data):
    names = [(item['updated_name']) for item in data]
    sent = np.array([float(item['sent']) for item in data])  
    received = np.array([float(item['reci']) for item in data]) 
    
    return sum(sent), sum(received)
    