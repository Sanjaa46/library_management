import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null,
    user: null
  }),

  actions: {
    setToken(access_token, refresh_token) {
      this.accessToken = access_token;
      this.refresh_token = refresh_token;
    },
    clearAuth() {
      this.accessToken = null;
      this.refresh_token = null;
      this.user = null;
    },
  },
});