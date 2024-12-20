<template>
  <v-app>
    <v-app-bar color="primary">
      <v-container class="d-flex align-center">
        <!-- Email Fetch button -->
        <v-btn @click="currentPage = 'EmailFetcher'" variant="text">
          Email Fetch
        </v-btn>

        <!-- Statistics button -->
        <v-btn @click="fetchStatistics" variant="text">
          Statistic
        </v-btn>
      </v-container>
    </v-app-bar>

    <v-main>
      <v-container>
        <!-- Use v-show to keep both components in the DOM -->
        <EmailFetcher v-show="currentPage === 'EmailFetcher'" :messages="messages" />
        <StatisticsPage v-show="currentPage === 'Statistics'" :statistics="statistics" />
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
      messages: [], // Your fetched messages data
      statistics: [] // Your statistics data
    };
  },
  methods: {
    // Fetch messages when needed

    goToStatisticsPage() {
      this.$router.push('/statistics');
    },
    
    fetchEmails() {
      // Simulate fetching data
      this.messages = [/* fetched messages here */];
    },
    fetchStatistics() {
      // Trigger fetching of statistics and switch page
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
    // Fetch initial data when the page is mounted
    this.fetchEmails();
  }
};
</script>

<style scoped>
/* Add any styles specific to App.vue */
</style>
