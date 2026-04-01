import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useAuthStore = defineStore("auth", () => {
  const accessToken = ref(localStorage.getItem("access_token") || null);
  const refreshToken = ref(localStorage.getItem("refresh_token") || null);
  const user = ref(JSON.parse(localStorage.getItem("user") || "null"));

  const isAuthenticated = computed(() => !!accessToken.value);

  function setAuth(data) {
    accessToken.value = data.access;
    refreshToken.value = data.refresh;
    user.value = {
      id: data.id,
      email: data.email,
      role: data.role,
      first_name: data.first_name,
      last_name: data.last_name,
    };

    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    localStorage.setItem("user", JSON.stringify(user.value));
  }

  function clearAuth() {
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
  }

  return { accessToken, refreshToken, user, isAuthenticated, setAuth, clearAuth };
});
