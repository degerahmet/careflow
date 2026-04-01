<template>
  <div class="flex min-h-screen bg-gray-50">
    <ProviderSidebar :collapsed="sidebarCollapsed" @toggle="sidebarCollapsed = !sidebarCollapsed" />

    <main class="flex-1 overflow-y-auto">
      <!-- Profile loading -->
      <div v-if="profileLoading" class="flex items-center justify-center h-full min-h-screen">
        <UIcon name="i-lucide-loader-circle" class="animate-spin text-gray-400 text-3xl" />
      </div>

      <!-- Profile fetch error -->
      <div v-else-if="profileError" class="flex items-center justify-center h-full p-6">
        <div class="w-full max-w-sm space-y-4 text-center">
          <UAlert color="error" variant="soft" :description="profileError" />
          <UButton variant="outline" @click="loadProfile">Try again</UButton>
        </div>
      </div>

      <!-- Dashboard content -->
      <div v-else class="p-6 max-w-4xl mx-auto space-y-6">
        <div class="flex items-center justify-between">
          <h1 class="text-xl font-semibold text-gray-900">Appointments</h1>
        </div>

        <!-- Appointments loading -->
        <div v-if="apptLoading" class="flex items-center justify-center py-16">
          <UIcon name="i-lucide-loader-circle" class="animate-spin text-gray-400 text-3xl" />
        </div>

        <!-- Appointments error -->
        <div v-else-if="apptError" class="space-y-3">
          <UAlert color="error" variant="soft" :description="apptError" />
          <UButton variant="outline" size="sm" @click="loadAppointments">Try again</UButton>
        </div>

        <!-- Empty state -->
        <div v-else-if="appointments.length === 0" class="flex flex-col items-center justify-center py-16 text-center">
          <UIcon name="i-lucide-calendar-x" class="text-gray-300 text-5xl mb-4" />
          <p class="text-gray-500 text-sm">No appointments yet.</p>
        </div>

        <!-- Appointment cards -->
        <div v-else class="space-y-4">
          <UCard
            v-for="appt in appointments"
            :key="appt.id"
          >
            <div class="flex items-start justify-between gap-4">
              <div class="min-w-0 space-y-1">
                <p class="font-medium text-gray-200 truncate">{{ appt.member_email }}</p>
                <p class="text-sm text-gray-500">{{ formatDate(appt.scheduled_at) }}</p>
              </div>
              <UBadge
                :color="STATUS_COLOR[appt.status] ?? 'neutral'"
                variant="soft"
                class="capitalize shrink-0"
              >
                {{ appt.status }}
              </UBadge>
            </div>

            <div class="mt-3 space-y-1">
              <p class="text-sm text-gray-300">
                <span class="font-medium">Reason: </span>{{ appt.reason }}
              </p>
              <p v-if="appt.ai_summary" class="text-sm text-gray-500 italic">
                {{ appt.ai_summary }}
              </p>
            </div>
          </UCard>
        </div>
      </div>

      <!-- Forced onboarding modal -->
      <ProviderOnboardingModal v-if="showOnboarding" @complete="onOnboardingComplete" />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getProfile } from "../../api/provider.js";
import { getProviderAppointments } from "../../api/appointments.js";
import ProviderOnboardingModal from "../../components/ProviderOnboardingModal.vue";
import ProviderSidebar from "../../components/ProviderSidebar.vue";

const sidebarCollapsed = ref(false);

// Profile / onboarding state
const profileLoading = ref(true);
const profileError = ref(null);
const showOnboarding = ref(false);

// Appointments state
const apptLoading = ref(false);
const apptError = ref(null);
const appointments = ref([]);

const STATUS_COLOR = {
  pending: "warning",
  confirmed: "success",
  cancelled: "error",
};

function formatDate(iso) {
  const d = new Date(iso);
  return (
    d.toLocaleDateString(undefined, { dateStyle: "medium" }) +
    " at " +
    d.toLocaleTimeString(undefined, { timeStyle: "short" })
  );
}

async function loadProfile() {
  profileLoading.value = true;
  profileError.value = null;

  try {
    const profile = await getProfile();
    const isIncomplete = !profile.specialty || !profile.bio;
    showOnboarding.value = isIncomplete;
    if (!isIncomplete) {
      loadAppointments();
    }
  } catch (err) {
    profileError.value = err.message;
  } finally {
    profileLoading.value = false;
  }
}

async function loadAppointments() {
  apptLoading.value = true;
  apptError.value = null;

  try {
    appointments.value = await getProviderAppointments();
  } catch (err) {
    apptError.value = err.message;
  } finally {
    apptLoading.value = false;
  }
}

function onOnboardingComplete() {
  showOnboarding.value = false;
  loadAppointments();
}

onMounted(loadProfile);
</script>
