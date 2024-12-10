<template>
  <v-app>
    <v-app-bar color="primary">
      <v-container class="d-flex align-center">
        <!-- Email Fetch button -->
        <v-btn @click="currentPage = 'EmailFetcher'" variant="text">
          Email Fetch
        </v-btn>

        <!-- Statistics button -->
        <v-btn @click="currentPage = 'Statistics'" variant="text">
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
      messages: [],  // Your fetched messages data
      statistics: [] // Your statistics data
    };
  },
  methods: {
    // Fetch messages when needed
    fetchEmails() {
      // Simulate fetching data
      this.messages = [/* fetched messages here */];
    },
    fetchStatistics() {
      // Simulate fetching statistics data
      this.statistics = [/* fetched statistics data here */];
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
