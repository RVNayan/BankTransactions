<template>
  <v-app>
    <v-container>
      <v-toolbar :color="authorized ? 'green' : 'primary'" dark>
        <v-toolbar-title>{{ authorized ? 'Authorized Successfully' : 'Gmail Fetcher' }}</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn v-if="!authorized" @click="authorize">Authorize API Access</v-btn>
      </v-toolbar>

      <v-card>
        <v-card-title>Email Messages</v-card-title>
        <v-card-text>
          <v-table>
            <thead>
              <tr>
                <th>Date</th>
                <th>Amount</th>
                <th>Sender/Receiver</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(message, index) in messages"
                :key="index"
                :style="{ backgroundColor: message.IsDebited ? 'lightcoral' : 'lightgreen' }"
              >
                <td>{{ message['Date of Payment'] }}</td>
                <td>{{ message['Amount'] }}</td>
                <td class="floating-expand">
                <span v-if="editingIndex !== index">{{ message['Receiver'] }}</span>
                
                <v-text-field
                  v-else
                  v-model="editingName[index]"
                  @keyup.enter="saveName(message['Receiver'], index, 'Receiver')"
                  @blur="stopEditing"
                  solo
                  hide-details
                />
                <div class="hover-container">
              <span class="hover-text">
                  ID: {{ message['OriginalName'] }}<br>
                  Sent: {{ getSentAmount(index) }}<br>
                  Received: {{ getReceivedAmount(index) }}
              </span>
          </div>
                <v-icon small class="ml-2" @click="editName(index, message['Receiver'])">mdi-pencil</v-icon>
                <v-icon small class="ml-2" @click="resetName(index, message['Receiver'])">mdi-eraser</v-icon>
              </td>
              <td>{{ message['Time'] }}</td>
            </tr>
            </tbody>
          </v-table>

          <v-btn @click="fetchEmails" color="primary">Fetch Emails</v-btn>
        </v-card-text>
      </v-card>

      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>Authorization Status</v-card-title>
          <v-card-text>{{ dialogMessage }}</v-card-text>
          <v-card-actions>
            <v-btn text @click="dialog = false">Close</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      messages: [],
      dialog: false,
      dialogMessage: '',
      authorized: false,
      editingIndex: null,
      editingName: {},
      OriginalNameDisplay: [],
      transactions: [],
    };
  },
  methods: {
    authorize() {
      window.location.href = 'http://localhost:8080/authorize';
    },

    async fetchTransactionData() {
            try {
                const response = await fetch('http://localhost:8080/fetch_transactions', {
                    method: 'GET',
                    credentials: 'include',
                });
                const data = await response.json();
 
                this.transactions = data; // Store fetched transactions

                
            } catch (error) {
                console.error('Error fetching transactions:', error);
            }
        },

        getSentAmount(index) {
            const receiver = this.messages[index]['Receiver'];
            const transaction = this.transactions.find(tx => tx.updated_name === receiver);
            return transaction ? transaction.sent : 0; // Return 0 if no transaction found
        },
        
        getReceivedAmount(index) {
            const receiver = this.messages[index]['Receiver'];
            const transaction = this.transactions.find(tx => tx.updated_name === receiver);
            return transaction ? transaction.reci : 0; // Return 0 if no transaction found
        },

    async fetchEmails() {
  try {
    const response = await fetch('http://localhost:8080/fetch_emails', {
      method: 'GET',
      credentials: 'include',
    });
    const data = await response.json();

    if (data.messages) {
      this.messages = data.messages;
      // Initialize editingName with the current receiver names
      this.editingName = this.messages.reduce((acc, message, index) => {
        acc[index] = message['Receiver']; // Initialize with the updated names
        return acc;
      }, {});
      this.originalName = this.messages.reduce((acc, message, index) => {
        acc[index] = message['OriginalName']; // Store original names
        return acc;
      }, {});
      this.OriginalNameDisplay = this.messages.reduce((acc, message, index) => {
          acc[index] = message['OriginalName']; // For OriginalNameDisplay
          return acc;
      }, {});
    } else if (data.error) {
      this.dialogMessage = data.error;
      this.dialog = true;
    } else {
      this.dialogMessage = 'Unexpected response structure';
      this.dialog = true;
    }
  } catch (error) {
    this.dialogMessage = 'Error fetching emails: ' + error.message;
    this.dialog = true;
  }
},

    async checkAuthorization() {
      try {
        const response = await fetch('http://localhost:8080/authorized', {
          method: 'GET',
          credentials: 'include',
        });
        const data = await response.json();

        if (data.authorized) {
          this.authorized = true;
        }
      } catch (error) {
        console.error('Authorization check failed:', error);
      }
    },
    editName(index, currentName) {
      this.editingIndex = index; // Set the index of the row being edited
      this.editingName[index] = currentName; // Set the current name to the input field
    },
    async saveName(originalName, index, column) {
      try {
        const response = await fetch('http://localhost:8080/update_name', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ originalName, newName: this.editingName[index], type: column }),
        });

        const result = await response.json();
        if (result.success) {
          // Update the displayed name
          this.messages[index][column] = this.editingName[index];
          this.stopEditing(); // Stop editing
        } else {
          this.dialogMessage = result.error || 'Error updating name';
          this.dialog = true;
        }
      } catch (error) {
        this.dialogMessage = 'Error saving name: ' + error.message;
        this.dialog = true;
      }
    },
    stopEditing() {
      this.editingIndex = null; // Reset editing index
      // No need to reset editingName[index] since it's already bound to the v-text-field
    },
    async resetName(index, column) {
  // Read the current name from the messages array
  const currentName = this.messages[index][column]; // Get the current name from the cell
  try {
    const response = await fetch('http://localhost:8080/reset_name', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({name: column }), // Send current name as originalName
    });

    // Check if the response is OK
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const result = await response.json();
    if (result.success) {
      // Update the displayed name to original name
      this.messages[index][column] = currentName; // Restore original name
      this.editingName[index] = currentName; // Reset the editing name to original

      // Optionally, you could also reset the editing index if you are in editing mode
      if (this.editingIndex === index) {
        this.stopEditing(); // Stop editing if applicable
      }
    } else {
      // Show the error message in the dialog
      this.dialogMessage = result.error || 'Error resetting name';
      this.dialog = true;
    }
  } catch (error) {
    // Handle any error that occurs during fetch or response processing
    this.dialogMessage = 'Error resetting name: ' + error.message;
    this.dialog = true;
  }
},

},

  async mounted() {
  this.checkAuthorization();
  await this.fetchTransactionData();
}, 
};
</script>

<style scoped>
.v-toolbar {
  background-color: #1976D2;
  color: white;
}

.v-table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

th {
  background-color: lightgrey;
}

.v-icon {
  cursor: pointer;
}

.floating-expand {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
  position: relative;
  background-color: #f0f0f0; /* Make sure the cell and hover text match */
  padding: 8px;
}

.floating-expand:hover {
  transform: scale(1.05); /* Slight expansion */
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 10;
}

.hover-text {
    position: absolute;  /* Position it relative to the closest positioned ancestor */
    background-color: black;
    color: white;
    padding: 8px;
    border-radius: 4px;
    font-size: 0.9em;
    white-space: nowrap;
    right: 0;             /* Aligns the box to the right */
    display: none;        /* Initially hidden */
    z-index: 10;          /* Ensures it appears above other elements */
}

.hover-container {
    position: relative;   /* Ensures .hover-text is positioned relative to this container */
    display: inline-block;
}

.hover-container:hover .hover-text {
    display: block; }

.floating-expand:hover .hover-text {
  display: block;
}

</style>