<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-3xl mx-auto px-4 py-8 space-y-6">
      <!-- Header -->
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-2xl font-bold">
            Welcome, {{ authStore.user?.first_name }}
          </h1>
          <p class="text-sm mt-1">Your appointments</p>
        </div>
        <div class="flex items-center gap-3">
          <UButton :to="{ name: 'member-chat' }" icon="i-heroicons-plus">
            New Appointment
          </UButton>
          <UButton variant="outline" color="neutral" class="cursor-pointer !border-gray-800 !border-2 hover:!bg-gray-600" @click="logout">
            Sign out
          </UButton>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="flex justify-center py-16">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin text-primary-500 w-8 h-8" />
      </div>

      <!-- Error -->
      <UAlert v-else-if="error" color="error" variant="soft" :description="error" />

      <!-- Empty -->
      <div v-else-if="appointments.length === 0" class="text-center py-16">
        <UIcon name="i-heroicons-calendar" class="w-12 h-12 text-gray-300 mx-auto mb-3" />
        <p>No appointments yet.</p>
        <UButton class="mt-4" :to="{ name: 'member-chat' }">
          Book your first appointment
        </UButton>
      </div>

      <!-- Appointment list -->
      <div v-else class="space-y-3">
        <UCard
          v-for="appt in appointments"
          :key="appt.id"
          class="w-full"
        >
          <div class="flex items-start justify-between gap-4">
            <div class="space-y-1">
              <p class="font-semibold">
                Dr. {{ appt.provider.first_name }} {{ appt.provider.last_name }}
              </p>
              <p class="text-sm">{{ specialtyLabel(appt.provider.specialty) }}</p>
              <p class="text-sm">{{ formatDate(appt.scheduled_at) }}</p>
              <p v-if="appt.reason" class="text-sm mt-2">{{ appt.reason }}</p>
            </div>
            <UBadge :color="STATUS_COLOR[appt.status] ?? 'neutral'" variant="soft" class="shrink-0 capitalize">
              {{ appt.status }}
            </UBadge>
          </div>
        </UCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth.js";
import { getMemberAppointments } from "../../api/appointments.js";
import { STATUS_COLOR } from "../../constants/status.js";

const SPECIALTY_LABELS = {
  GEN: "General Practice",
  CARD: "Cardiology",
  DERM: "Dermatology",
  NEUR: "Neurology",
  ORTH: "Orthopedics",
  PEDS: "Pediatrics",
  PSYC: "Psychiatry",
  OB: "OB/GYN",
  ONCO: "Oncology",
  ENDO: "Endocrinology",
};

const router = useRouter();
const authStore = useAuthStore();

const appointments = ref([]);
const loading = ref(true);
const error = ref(null);

function logout() {
  authStore.clearAuth();
  router.push({ name: "member-login" });
}

function specialtyLabel(code) {
  return SPECIALTY_LABELS[code] ?? code;
}


function formatDate(iso) {
  return new Date(iso).toLocaleString(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

onMounted(async () => {
  try {
    appointments.value = await getMemberAppointments();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});
</script>
