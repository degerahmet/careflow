import { createRouter, createWebHistory } from "vue-router";

import ProviderLoginView from "../views/provider/ProviderLoginView.vue";
import ProviderSignupView from "../views/provider/ProviderSignupView.vue";
import ProviderDashboardView from "../views/provider/ProviderDashboardView.vue";
import ProviderAvailabilityView from "../views/provider/ProviderAvailabilityView.vue";
import MemberLoginView from "../views/member/MemberLoginView.vue";

const routes = [
  { path: "/", redirect: "/provider/login" },
  { path: "/provider/login", name: "provider-login", component: ProviderLoginView },
  { path: "/provider/signup", name: "provider-signup", component: ProviderSignupView },
  { path: "/provider/dashboard", name: "provider-dashboard", component: ProviderDashboardView },
  { path: "/provider/availability", name: "provider-availability", component: ProviderAvailabilityView },
  { path: "/member/login", name: "member-login", component: MemberLoginView },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
