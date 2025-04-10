import re
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'service_acc.json'

# Function to extract data from email message
def extracter(email_message):
    date_pattern = r"(\d{1,2} [A-Za-z]{3}) 20\d{2}"  # change Year
    amount_pattern = r"Rs\. ?([\d,]+\.\d{2})"
    receiver_pattern = r"VPA (\S+)"
    time_pattern = r"\b([01]?[0-9]|2[0-3]):[0-5][0-9]\b"

    date_match = re.search(date_pattern, email_message)
    date_of_payment = date_match.group(1) if date_match else "Date not found"

    amount_match = re.search(amount_pattern, email_message)
    amount = amount_match.group(1) if amount_match else "Amount not found"

    receiver_match = re.search(receiver_pattern, email_message)
    receiver = receiver_match.group(1) if receiver_match else "Receiver not found"

    time_match = re.search(time_pattern, email_message)
    time_of_payment = time_match.group(0) if time_match else "Time not found"
    debited = bool(re.search("debited", email_message))

    
    return [date_of_payment, amount, receiver, time_of_payment,debited] # Debited to check if its recieved or sent

def find_first_empty_cell(service, sheet_id, range_name):
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])

    if not values:
        return 1  # If no data, start from the first row

    # Find the first empty cell in column A
    for i, row in enumerate(values):
        if not row:  # If row is empty
            return i + 1  # Return the row index (1-based)

    return len(values) + 1  # If no empty rows found, append after the last row

def write_to_sheets(data, sheet_id, range_name,SCOPES, SERVICE_ACCOUNT_FILE):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)

    # Find the first empty cell in column A
    start_row = find_first_empty_cell(service, sheet_id, range_name)

    # Construct the new range to append data
    new_range = f"{range_name}!A{start_row}"

    # Prepare the data to be appended
    data_to_append = {
        'range': new_range,
        'majorDimension': 'ROWS',
        'values': [data],
    }

    try:
        # Append the data
        result = service.spreadsheets().values().append(
            spreadsheetId=sheet_id, range=new_range,
            valueInputOption='RAW', body=data_to_append).execute()
        print("Data appended successfully.")
    except Exception as e:
        print(f"Error writing data: {e}")
