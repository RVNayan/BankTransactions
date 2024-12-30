<template>
  <v-app>
    <v-app-bar color="primary">
      <v-container class="d-flex align-center">
        <v-btn @click="currentPage = 'EmailFetcher'" variant="text">
          Email Fetch
        </v-btn>
        <v-btn @click="fetchStatistics" variant="text">
          Statistics
        </v-btn>
      </v-container>
    </v-app-bar>

    <v-main>
      <v-container>
        <!-- Use v-show to keep both components in the DOM -->
        <EmailFetcher v-show="currentPage === 'EmailFetcher'" :messages="messages" />
        <StatisticsPage
          v-show="currentPage === 'Statistics'"
          :statistics="statistics"
          :key="statistics ? statistics.id : 'default'"/>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import axios from 'axios';
import EmailFetcher from './components/EmailFetcher.vue';
import StatisticsPage from './components/StatisticsPage.vue';

export default {
  name: 'App',
  components: {
    EmailFetcher,
    StatisticsPage,
  },
  data() {
    return {
      currentPage: 'EmailFetcher',
      messages: [],
      statistics: { barStats: [], pieStats: [] } // Ensure this matches the expected format
    };
  },
  methods: {
    fetchEmails() {
      // Simulate fetching data
      this.messages = [/* fetched messages here */];
    },
    fetchStatistics() {
      this.currentPage = 'Statistics';

      // Axios request to backend for statistics
      axios
        .get('http://localhost:8080/statistics')
        .then(response => {
          this.statistics = response.data; // Assign fetched data
        })
        .catch(error => {
          console.error('Error fetching statistics:', error);
        });
    }
  },
  mounted() {
    this.fetchEmails();
  }
};
</script>
