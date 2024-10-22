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
                <td>
                  <span v-if="editingIndex !== index">{{ message['Receiver'] }}</span>
                  <v-text-field
                    v-else
                    v-model="editingName[index]"
                    @keyup.enter="saveName(message['Receiver'], index, 'Receiver')"
                    @blur="stopEditing"
                    solo
                    hide-details
                  />
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
    };
  },
  methods: {
    authorize() {
      window.location.href = 'http://localhost:8080/authorize';
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
            acc[index] = message['Receiver']; // Initialize with the original names
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

mounted() {
  this.checkAuthorization();
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
</style>
