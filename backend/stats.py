import numpy as np
import pandas as pd
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from datetime import datetime
#For Fetching amount sent or reci

def Total_amount(data):
    names = [(item['updated_name']) for item in data]
    sent = np.array([float(item['sent']) for item in data])  
    received = np.array([float(item['reci']) for item in data]) 
    
    large_sent_index = np.argmax(sent)
    large_reci_index = np.argmax(received)

    # print(sent[large_sent_index], names[large_sent_index]) 
    
    return sum(sent), sum(received), names[large_sent_index]
    

def DayWiseExpenses(rawdata):
    Date = {}  # Dictionary to store total amounts per date
    
    for i in rawdata:
        if i['Amount'] != 'Amount not found':
            date_key = i['Date of Payment']  # Extract the date
            amount = float(i['Amount'])  # Ensure the amount is numeric
            
            # Standardize date format to "DD MMM"
            date_obj = datetime.strptime(date_key, '%d %b')  # Convert to datetime object
            formatted_date = date_obj.strftime('%d %b')  # Format as "DD MMM"
            
            # Update the total for the date
            if formatted_date not in Date:
                Date[formatted_date] = amount
            else:
                Date[formatted_date] += amount
    
    # Sort the dictionary by date
    sorted_dates = sorted(Date.keys(), key=lambda x: datetime.strptime(x, '%d %b'))
    sorted_date_amounts = {date: Date[date] for date in sorted_dates}

    return sorted_date_amounts

#Pie Chart Data
def Pie(data):
    names = [(item['updated_name']) for item in data]
    sent = np.array([float(item['sent']) for item in data])  
    received = np.array([float(item['reci']) for item in data])
    return names, sent / sum(sent), received / sum(received)
    
# def Predict_next(data):
    
#     names = [(item['updated_name']) for item in data]
#     sent = np.array([float(item['sent']) for item in data])  
#     reci = np.array([float(item['reci']) for item in data])

#     # Encode names and normalize amounts
#     le = LabelEncoder()
#     names_encoded = le.fit_transform(names)

#     scaler_sent = MinMaxScaler()
#     scaler_reci = MinMaxScaler()
#     sent = scaler_sent.fit_transform(sent.reshape(-1, 1)).flatten()
#     reci = scaler_reci.fit_transform(reci.reshape(-1, 1)).flatten()

#     # Combine as sequences
#     X = np.column_stack((names_encoded, sent, reci))

#     # Split into train and test sets
#     X_train = X[:-1]  # All but the last transaction for training
#     X_test = X[-1].reshape(1, -1)  # Last transaction for testing
#     # Define RNN model
#     class TransactionRNN(nn.Module):
#         def __init__(self, input_size, hidden_size, output_size):
#             super(TransactionRNN, self).__init__()
#             self.rnn = nn.LSTM(input_size, hidden_size, batch_first=True)
#             # Add ReLU to ensure non-negative outputs
#             self.fc = nn.Sequential(
#                 nn.Linear(hidden_size, output_size),
#                 nn.ReLU()
#             )
        
#         def forward(self, x):
#             _, (hn, _) = self.rnn(x)
#             out = self.fc(hn[-1])
#             return out


#     # Instantiate model, loss, and optimizer
#     input_size = 3
#     hidden_size = 64
#     output_size = 3
#     model = TransactionRNN(input_size, hidden_size, output_size)
#     criterion = nn.MSELoss()
#     optimizer = optim.Adam(model.parameters(), lr=0.001)

#     # Training loop (simplified for illustration)
#     X_train_tensor = torch.Tensor(X_train).unsqueeze(0)  # Add batch dimension
#     y_train_tensor = torch.Tensor(X_train[1:]).view(1, -1, 3)  # Adjust shape
#     print(y_train_tensor)

#     epochs = 100
#     for epoch in range(epochs):
#         model.train()
#         optimizer.zero_grad()
#         output = model(X_train_tensor)
#         loss = criterion(output, y_train_tensor)
#         loss.backward()
#         optimizer.step()

#     # Test the model on the last transaction
#     model.eval()
#     X_test_tensor = torch.Tensor(X_test).unsqueeze(0)
#     predicted = model(X_test_tensor)
#     predicted_values = predicted.detach().numpy().flatten()

#     # Denormalize prediction (if needed)
#     predicted_sent = scaler_sent.inverse_transform([[predicted_values[1]]])[0][0]
#     predicted_reci = scaler_reci.inverse_transform([[predicted_values[2]]])[0][0]
#     predicted_name = le.inverse_transform([int(predicted_values[0])])

#     print(f"Predicted next transaction - Name: {predicted_name[0]}, Sent: {predicted_sent}, Received: {predicted_reci}")
