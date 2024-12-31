from decimal import Decimal
import os
import flask
import base64
import requests
import psycopg2
from psycopg2 import sql
from flask_cors import CORS
from dotenv import load_dotenv
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from datetime import datetime, timedelta
from main import extracter, write_to_sheets
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from datetime import datetime, timedelta

#self functions
from stats import Total_amount, DayWiseExpenses, Pie

load_dotenv('../.env')
CLIENT_SECRETS_FILE = "backend/client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
API_SERVICE_NAME = os.getenv('API_SERVICE_NAME')
API_VERSION = os.getenv('API_VERSION')
range_name = os.getenv('RANGE_NAME')
sender_id = os.getenv('SENDER_ID')

sheet_id = os.getenv('SHEET_ID')
sheet_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'backend/service_acc.json'


app = flask.Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = os.getenv('SECRET_KEY')

# Directory to store text files
STORE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


# def store_credentials_in_db(user_id, credentials):
#     try:
#         # Connect to the PostgreSQL database
#         conn = psycopg2.connect(
#             host="localhost",
#             database="webpay",
#             user="webpayuser",
#             password="yourpassword"  # Replace with your actual password
#         )
#         cursor = conn.cursor()

#         # Prepare SQL query to insert credentials
#         query = """
#         INSERT INTO user_credentials (user_id, access_token, refresh_token, expires_at)
#         VALUES (%s, %s, %s, %s);
#         """
        
#         # Calculate expiration time (assuming expires_in is in seconds)
#         expires_at = datetime.now()

#         # Execute the query
#         cursor.execute(query, (user_id, credentials.token, credentials.refresh_token, expires_at))
        
#         # Commit the changes
#         conn.commit()

#     except Exception as e:
#         print(f"An error occurred while storing credentials: {e}")
    
#     finally:
#         # Close the database connection
#         cursor.close()
#         conn.close()

def reset_transaction_totals():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="webpay",
            user="webpayuser",
            password="yourpassword"
        )
        cursor = conn.cursor()
        
        # Reset the `sent` and `reci` columns for all rows
        cursor.execute("UPDATE sender_names SET sent = 0, reci = 0")
        
        conn.commit()
    except Exception as e:
        print(f"An error occurred while resetting transaction totals: {e}")
    finally:
        cursor.close()
        conn.close()

def store_sent_rect(updated_name, amount, is_debited):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="webpay",
            user="webpayuser",
            password="yourpassword" 
        )
        cursor = conn.cursor()

        if is_debited:
            # Add amount to existing value in `sent` column
            cursor.execute(
                "UPDATE sender_names SET sent = sent + %s WHERE updated_name = %s",
                (amount, updated_name)
            )
        else:
            # Add amount to existing value in `reci` column
            cursor.execute(
                "UPDATE sender_names SET reci = reci + %s WHERE updated_name = %s",
                (amount, updated_name)
            )

        conn.commit()
    except Exception as e:
        print(f"An error occurred while storing sender name: {e}")
    finally:
        cursor.close()
        conn.close()

def store_sender_name(original_name, updated_name):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="webpay",
            user="webpayuser",
            password="yourpassword" 
        )
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM sender_names WHERE updated_name = %s", (original_name,))
        existing_name = cursor.fetchone()

        if existing_name:
            if existing_name[1] != updated_name:  
                cursor.execute(
                    "UPDATE sender_names SET updated_name = %s WHERE previous_name = %s",
                    (updated_name, existing_name[1])         
                )
            
        else:
            # If it doesn't exist, insert it with the updated_name same as original_name
            cursor.execute(
                "INSERT INTO sender_names (original_name, updated_name, previous_name) VALUES (%s, %s, %s)",
                (original_name, original_name, original_name)
            )

        conn.commit()
    except Exception as e:
        print(f"An error occurred while storing sender name: {e}")

    finally:
            cursor.close()
            conn.close()

@app.route('/')
def index():
    return print_index_table()

# @app.route('/test')
# def test_api_request():
#     fulldata = {}
#     if 'credentials' not in flask.session:
#         return flask.redirect('authorize')

#     credentials = google.oauth2.credentials.Credentials(
#         **flask.session['credentials'])

#     service = googleapiclient.discovery.build(
#         'gmail', 'v1', credentials=credentials)

#     target_sender = sender_id
#     filtered_messages = []

#     now = datetime.utcnow()
#     past_week = now - timedelta(days=4)
#     past_week_str = past_week.strftime("%Y/%m/%d")

#     results = service.users().messages().list(userId='me', q=f"from:{target_sender} after:{past_week_str}").execute()
#     messages = results.get('messages', [])

#     if not messages:
#         return flask.jsonify({'error': 'No messages found in the past week.'})
#     else:
#         for index, message in enumerate(messages):
#             msg = service.users().messages().get(userId='me', id=message['id']).execute()
#             headers = msg['payload']['headers']
#             sender_found = any(header['name'] == 'From' and target_sender in header['value'] for header in headers)

#             if sender_found:
#                 full_message = ""
#                 for part in msg['payload']['parts']:
#                     if 'data' in part['body']:
#                         raw_data = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', 'ignore')
#                         full_message += raw_data + "\n"
#                 DAT = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'Date')
#                 data = extracter(full_message + DAT)
#                 unitdata = {"Date of Payment": data[0], "Amount": data[1], "Receiver": data[2], "Time": data[3]}
#                 fulldata[f'message_{index}'] = unitdata

#                 # Write data to Google Sheets
#                 # write_to_sheets(data, sheet_id, range_name, sheet_SCOPES, SERVICE_ACCOUNT_FILE)

                
#     fetch_stats()
#     flask.session['credentials'] = credentials_to_dict(credentials)
#     return flask.jsonify({'messages':filtered_messages})

# Remaining routes and functions omitted for brevity

@app.route('/labels')
def list_labels():
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    service = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    label_data = []
    if not labels:
        label_data.append('No labels found.')
    else:
        for label in labels:
            label_data.append(label['name'])

    flask.session['credentials'] = credentials_to_dict(credentials)
    
    return flask.jsonify(label_data)

@app.route('/authorize')
def authorize():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)

    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true')

    flask.session['state'] = state

    return flask.redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = flask.session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=None, state=state)
    flow.redirect_uri = flask.url_for('oauth2callback', _external=True)

    authorization_response = flask.request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    flask.session['credentials'] = credentials_to_dict(credentials)

    # user_id = credentials.client_id  
    # store_credentials_in_db(user_id, credentials) #push to database
    # print("Token: ",credentials.client_id)

    return flask.redirect('http://localhost:8081/')

@app.route('/revoke')
def revoke():
    if 'credentials' not in flask.session:
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
                           params={'token': credentials.token},
                           headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return('Credentials successfully revoked.' + print_index_table())
    else:
        return('An error occurred.' + print_index_table())

@app.route('/clear')
def clear_credentials():
    if 'credentials' in flask.session:
        del flask.session['credentials']
    return ('Credentials have been cleared.<br><br>' +
            print_index_table())

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
    

@app.route('/authorized')
def check_authorization():
    if 'credentials' in flask.session:
        return flask.jsonify({'authorized': True})
    return flask.jsonify({'authorized': False})


def print_index_table():
    return ('<table>' +
            '<tr><td><a href="/authorize">Authorize the app</a></td>' +
            '<td>Authorize the application to access your Gmail account. ' +
            '    This is required before any API requests can be made.</td></tr>' +
            '<tr><td><a href="/fetch_emails">Fetch Emails</a></td>' +
            '<td>Fetch emails from the specified sender after authorization.</td></tr>' +
            '<tr><td><a href="/revoke">Revoke current credentials</a></td>' +
            '<td>Revoke the access token associated with the current user ' +
            '    session. After revoking credentials, you will need to reauthorize the application.</td></tr>' +
            '<tr><td><a href="/clear">Clear Flask session credentials</a></td>' +
            '<td>Clear the access token currently stored in the user session. ' +
            '    After clearing the token, you will need to reauthorize the application.</td></tr></table>')


@app.route('/fetch_emails', methods=['GET'])
def fetch_emails():
    reset_transaction_totals()
    if 'credentials' not in flask.session:
        return flask.redirect('authorize')

    credentials = google.oauth2.credentials.Credentials(
        **flask.session['credentials'])

    service = googleapiclient.discovery.build(
        'gmail', 'v1', credentials=credentials)

    target_sender = sender_id
    filtered_messages = []

    # Calculate the date range for searching
    now = datetime.utcnow()
    past_week = now - timedelta(days=5) # Change Days in the Backend!
    past_week_str = past_week.strftime("%Y/%m/%d")

    # Retrieve all messages from the past week
    results = service.users().messages().list(userId='me', q=f"from:{target_sender} after:{past_week_str}").execute()
    messages = results.get('messages', [])

    if not messages:
        return flask.jsonify({'error': 'No messages found in the past week.'})

    for index, message in enumerate(messages):
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        headers = msg['payload']['headers']
        sender_found = any(header['name'] == 'From' and target_sender in header['value'] for header in headers)

        if sender_found:
            # Initialize variable to accumulate message content
            full_message = ""

            # Iterate through parts to accumulate content
            for part in msg['payload']['parts']:
                if 'data' in part['body']:
                    raw_data = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', 'ignore')
                    full_message += raw_data + "\n"  # Append each part's content
            
            DAT = next(header['value'] for header in msg['payload']['headers'] if header['name'] == 'Date')
            data = extracter(full_message + DAT)

            # Check the database for the sender name
            updated_name = fetch_sender_name(data[2])  # Fetch the updated name
            store_sent_rect(updated_name, data[1], data[4]) # Store the amount Sent/Recieved for the given time duration
            store_sender_name(data[2], updated_name)  # Store the sender name in the database
            
                   
            unitdata = {"Date of Payment": data[0], "Amount": data[1], "Receiver": updated_name, "Time": data[3], "IsDebited": data[4], "OriginalName": data[2]}
            filtered_messages.append(unitdata)  # Individual Transaction Data / Use for previous Stats
            # Write data to Google Sheets
            # write_to_sheets(data, sheet_id, range_name, sheet_SCOPES, SERVICE_ACCOUNT_FILE)

    save_filtered_messages(filtered_messages)
        
    flask.session['credentials'] = credentials_to_dict(credentials)
    return flask.jsonify({'messages': filtered_messages})


@app.route('/update_name', methods=['POST'])
def update_name():
    data = flask.request.json
    original_name = data['originalName']
    new_name = data['newName']
    type = data['type']  # Could be 'sender' or 'receiver'

    try:
        conn = psycopg2.connect(
            host="localhost",
            database="webpay",
            user="webpayuser",
            password="yourpassword"
        )
        cursor = conn.cursor()
        

        store_sender_name(original_name, new_name)
        
        print(original_name, new_name)
        return flask.jsonify({'success': True})

    except Exception as e:
        return flask.jsonify({'success': False, 'error': str(e)})

    finally:
        cursor.close()
        conn.close()

@app.route('/reset_name', methods=['POST'])
def reset_name():
    data = flask.request.json
    # name = data['originalName']
    name = data['name']  # Assuming you may want to use this later
    #print(type)
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="webpay",
            user="webpayuser",
            password="yourpassword"
        )
        cursor = conn.cursor()
        reset_sender_name(getoriginal(name)) 

        return flask.jsonify({'success': True})

    except Exception as e:
        return flask.jsonify({'success': False, 'error': str(e)})

    finally:
        cursor.close()
        conn.close()

@app.route('/fetch_transactions', methods=['GET'])
def fetch_transaction_data():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="webpay",
            user="webpayuser",
            password="yourpassword"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT updated_name, sent, reci FROM sender_names")
        rows = cursor.fetchall()

        # Format the data into a list of dictionaries
        transactions = [{'updated_name': row[0], 'sent': row[1], 'reci': row[2]} for row in rows]

        return flask.jsonify(transactions)
    except Exception as e:
        return flask.jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/allstats', methods=['GET'])
def fetch_stats():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="webpay",
            user="webpayuser",
            password="yourpassword"
        )
        cursor = conn.cursor()

        cursor.execute("SELECT updated_name, sent, reci FROM sender_names")
        rows = cursor.fetchall()

        # Format the data into a list of dictionaries
        transactions = [{'updated_name': row[0], 'sent': row[1], 'reci': row[2]} for row in rows]
        T_sent, T_reci, Highest_sender = Total_amount(transactions) #from stats.py
        
        # file_path = "texts/all_transactions.json"
    
        # try:
        #     with open(file_path, 'w') as file:
        #         flask.json.dump(transactions, file, indent=4) 
        #     print(f"Filtered messages successfully saved to {file_path}")
        # except Exception as e:
        #     print(f"Error writing to file: {e}")
            
        
        Stats = [{'Total_amount_sent':T_sent, 'Total_amount_reci':T_reci, 'Largest_sender':Highest_sender}]
        return flask.jsonify(Stats)
    except Exception as e:
        return flask.jsonify({'error': str(e)})
    finally:
        cursor.close()
        conn.close()
        
#Helper Funcs, Unable to store the global Transaction history, The page is getting refreshed when switched to Statistics section
@app.route('/statistics', methods=['GET'])
def get_statistics():
    # Load filtered messages from the JSON file
    stats = load_filtered_messages() 
    
    
    day_wise_expenses = DayWiseExpenses(stats) # loading for Barchart (Chart1)

    response = fetch_transaction_data()         # Using Prexisting Data For Pie Chart Instead of Storing in json
    if isinstance(response, flask.Response):
        Piechartdata1 = response.get_json()  
    else:
        Piechartdata1 = flask.json.loads(response)

    day_wise_expenses = DayWiseExpenses(stats)

    combined_data = {
        "barStats": day_wise_expenses,  # Data for bar chart
        "pieStats": Piechartdata1     
    }
    # Return the combined data as JSON
    return flask.jsonify(combined_data)

def fetch_sender_name(original_name):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="webpay",
            user="webpayuser",
            password="yourpassword"  # Replace with your actual password
        )
        cursor = conn.cursor()

        # Check if the original name exists in the database
        cursor.execute("SELECT updated_name FROM sender_names WHERE previous_name = %s", (original_name,))
        result = cursor.fetchone()

        if result is not None:
            # If the name exists, fetch the updated name
            updated_name = result[0]  
            return updated_name # Return updated name or original if null
        else:
            return original_name  # If not found, return original name

    except Exception as e:
        print(f"An error occurred while fetching sender name: {e}")
        return original_name  # Return original name in case of error

    finally:
        # Close the database connection
        cursor.close()
        conn.close()


def reset_sender_name(name):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="webpay",
            user="webpayuser",
            password="yourpassword"  # Replace with your actual password
        )
        cursor = conn.cursor()

        # Fetch current updated name and previous name
        cursor.execute("SELECT original_name FROM sender_names WHERE previous_name = %s", (name,))
        result = cursor.fetchone()

        if result:
                cursor.execute("UPDATE sender_names SET updated_name = %s WHERE original_name = %s",(name, name))
    
        else:
            print("Original name not found in the database.")

        # Commit the changeshello
        conn.commit()

    except Exception as e:
        print(f"An error occurred while resetting sender name: {e}")
    
    finally:
        # Close the database connection
        cursor.close()
        conn.close()


def getoriginal(updated_name):
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host="localhost",
            database="webpay",
            user="webpayuser",
            password="yourpassword"  # Replace with your actual password
        )
        cursor = conn.cursor()

        # Check if the original name exists in the database
        cursor.execute("SELECT original_name FROM sender_names WHERE updated_name = %s", (updated_name,))
        result = cursor.fetchone()

        
        return result

    except Exception as e:
        print(f"An error occurred while fetching sender name: {e}")
        return updated_name  # Return original name in case of error

    finally:
        # Close the database connection
        cursor.close()
        conn.close()
    

def save_filtered_messages(filtered_messages):
    file_path = "texts/filtered_messages.json"
    
    try:
        with open(file_path, 'w') as file:
            flask.json.dump(filtered_messages, file, indent=4) 
        print(f"Filtered messages successfully saved to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def load_filtered_messages():
    file_path = "texts/filtered_messages.json"
    
    try:
        with open(file_path, 'r') as file:
            filtered_messages = flask.json.load(file)
        print(f"Filtered messages successfully loaded from {file_path}")
        return filtered_messages
    except FileNotFoundError:
        print(f"File not found at {file_path}")
        return None
    except flask.json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

def clear_filtered_messages():
    """Clears the content of the filtered_messages.json file."""
    file_path = "texts/filtered_messages.json"
    try:
        with open(file_path, "w") as file:
            file.write("{}") 
    except Exception as e:
        print(f"Failed to clear the file: {e}")
        
if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run('localhost', 8080, debug=True)