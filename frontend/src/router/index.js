import { createRouter, createWebHistory } from "vue-router";

import MemberLoginView from "../views/member/MemberLoginView.vue";
import MemberSignupView from "../views/member/MemberSignupView.vue";
import MemberDashboardView from "../views/member/MemberDashboardView.vue";
import MemberChatView from "../views/member/MemberChatView.vue";
import ProviderLoginView from "../views/provider/ProviderLoginView.vue";
import ProviderSignupView from "../views/provider/ProviderSignupView.vue";
import ProviderDashboardView from "../views/provider/ProviderDashboardView.vue";
import ProviderAvailabilityView from "../views/provider/ProviderAvailabilityView.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login",            name: "member-login",           component: MemberLoginView },
  { path: "/signup",           name: "member-signup",          component: MemberSignupView },
  { path: "/member/dashboard", name: "member-dashboard",       component: MemberDashboardView },
  { path: "/member/chat",      name: "member-chat",            component: MemberChatView },
  { path: "/provider/login",   name: "provider-login",         component: ProviderLoginView },
  { path: "/provider/signup",  name: "provider-signup",        component: ProviderSignupView },
  { path: "/provider/dashboard",    name: "provider-dashboard",     component: ProviderDashboardView },
  { path: "/provider/availability", name: "provider-availability",  component: ProviderAvailabilityView },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
