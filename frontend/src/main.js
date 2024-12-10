import { createApp } from 'vue';
import App from './App.vue';
import { createVuetify } from 'vuetify';
import router from './router/index.js';  // Import the router

// Vuetify setup
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css';
import { aliases, mdi } from 'vuetify/iconsets/mdi';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi },
  },
  theme: {
    defaultTheme: 'light',
  },
});

// Create Vue app instance
createApp(App)
  .use(vuetify)  // Use Vuetify
  .use(router)   // Use Vue Router
  .mount('#app');
