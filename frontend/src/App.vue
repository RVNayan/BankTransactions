<template>
  <div id="app">
    <EmailFetcher />
  </div>
</template>

<script>
import EmailFetcher from './components/EmailFetcher.vue';
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css'; 

export default {
  components: {
    EmailFetcher
  }
};
</script>

<style>
/* Add global styles here if needed */
</style>
