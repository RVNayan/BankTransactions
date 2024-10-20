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
          <!-- Updated Table Display -->
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
              <tr v-for="(message, index) in messages" :key="index" 
                  :style="{ backgroundColor: message.IsDebited ? 'lightcoral' : 'lightgreen' }"> <!-- Set background color based on IsDebited -->
                <td>{{ message['Date of Payment'] }}</td>
                <td>{{ message['Amount'] }}</td>
                <td>{{ message['Receiver'] }}</td>
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
      messages: [], // Array to hold fetched messages
      dialog: false,
      dialogMessage: '',
      authorized: false // To change toolbar color on successful authorization
    };
  },
  methods: {
    authorize() {
      // Redirect to the authorization endpoint
      window.location.href = 'http://localhost:8080/authorize';
    },
    async fetchEmails() {
      try {
        const response = await fetch('http://localhost:8080/fetch_emails', {
          method: 'GET',
          credentials: 'include' // Ensure credentials are sent with the request
        });
        const data = await response.json();
        
        if (data.messages) {  // Check if messages exist in the response
          this.messages = data.messages;  // Update the messages property
          console.log(data.messages);
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
          this.authorized = true; // Set toolbar to green if authorized
        }
      } catch (error) {
        console.error('Authorization check failed:', error);
      }
    }
  },
  mounted() {
    this.checkAuthorization(); // Check authorization status on page load
  }
};
</script>

<style scoped>
.v-toolbar {
  background-color: #1976D2; /* Default toolbar color */
  color: white; /* Text color */
}

.v-toolbar.green {
  background-color: green; /* Color for successful authorization */
}

v-table {
  width: 100%; /* Ensure the table takes full width */
  border-collapse: collapse; /* Collapses borders for a cleaner look */
}

th, td {
  border: 1px solid #ccc; /* Border for table cells */
  padding: 8px; /* Padding inside cells */
  text-align: left; /* Align text to the left */
}

th {
  background-color: lightgrey; /* Background color for header cells */
}
</style>
