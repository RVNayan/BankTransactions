import numpy as np


def Total_amount(data):
    sent = np.array([float(item['sent']) for item in data])  
    received = np.array([float(item['reci']) for item in data]) 
    
    return sum(sent)
    