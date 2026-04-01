<template>
  <aside
    class="flex flex-col bg-white border-r border-gray-200 transition-all duration-200 shrink-0"
    :class="collapsed ? 'w-16' : 'w-64'"
  >
    <!-- Brand -->
    <div class="flex items-center h-16 px-4 border-b border-gray-100">
      <UIcon name="i-lucide-heart-pulse" class="text-primary-500 text-xl shrink-0" />
      <span v-if="!collapsed" class="ml-3 font-semibold text-gray-900 truncate">Careflow</span>
    </div>

    <!-- Nav -->
    <nav class="flex-1 px-2 py-4 space-y-1">
      <RouterLink
        v-for="item in NAV_ITEMS"
        :key="item.name"
        :to="{ name: item.name }"
        class="flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
        :class="$route.name === item.name
          ? 'bg-primary-50 text-primary-700'
          : 'text-gray-600 hover:bg-gray-100'"
      >
        <UIcon :name="item.icon" class="text-lg shrink-0" />
        <span v-if="!collapsed" class="truncate">{{ item.label }}</span>
      </RouterLink>
    </nav>

    <!-- Collapse toggle -->
    <div class="px-2 pb-3">
      <button
        class="flex items-center justify-center w-full px-3 py-2 rounded-lg text-sm text-gray-500 hover:bg-gray-100 transition-colors"
        @click="$emit('toggle')"
      >
        <UIcon
          :name="collapsed ? 'i-lucide-chevron-right' : 'i-lucide-chevron-left'"
          class="text-lg"
        />
        <span v-if="!collapsed" class="ml-2">Collapse</span>
      </button>
    </div>

    <!-- Provider info + logout -->
    <div class="px-3 py-3 border-t border-gray-100 space-y-2">
      <div v-if="!collapsed" class="px-1 min-w-0">
        <p class="text-sm font-medium text-gray-900 truncate">{{ fullName }}</p>
        <p class="text-xs text-gray-500 truncate">{{ user?.email }}</p>
      </div>
      <UIcon v-else name="i-lucide-user-circle" class="text-gray-400 text-xl mx-auto block" />

      <button
        class="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-sm text-red-500 hover:bg-red-50 transition-colors"
        @click="logout"
      >
        <UIcon name="i-lucide-log-out" class="text-lg shrink-0" />
        <span v-if="!collapsed">Sign out</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "../stores/auth.js";

const NAV_ITEMS = [
  { name: "provider-dashboard",    label: "Dashboard",    icon: "i-lucide-layout-dashboard" },
  { name: "provider-availability", label: "Availability", icon: "i-lucide-calendar-days" },
];

defineProps({
  collapsed: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["toggle"]);

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const user = authStore.user;
const fullName = computed(() =>
  [user?.first_name, user?.last_name].filter(Boolean).join(" ") || user?.email
);

function logout() {
  authStore.clearAuth();
  router.push({ name: "provider-login" });
}
</script>
