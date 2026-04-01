<template>
  <div class="h-screen flex flex-col bg-white relative">
    <!-- Header -->
    <div class="sticky top-0 z-10 bg-white border-b border-gray-100 px-4 py-3 flex items-center justify-between">
      <UButton
        variant="ghost"
        color="neutral"
        icon="i-heroicons-arrow-left"
        class="!text-black hover:!text-white"
        :to="{ name: 'member-dashboard' }"
      >
        Back
      </UButton>
      <h1 class="text-base font-semibold">CareFlow AI</h1>
      <div class="w-20" />
    </div>

    <!-- Rehydrating state -->
    <div v-if="rehydrating" class="flex-1 flex items-center justify-center">
      <UIcon name="i-heroicons-arrow-path" class="animate-spin w-6 h-6" />
    </div>

    <!-- Message area -->
    <div v-else ref="messagesEl" class="flex-1 overflow-y-auto pb-40">
      <div class="max-w-3xl mx-auto px-4 py-6 space-y-6">

        <!-- Chat messages -->
        <div
          v-for="(msg, i) in messages"
          :key="i"
          :class="msg.role === 'user' ? 'flex justify-end' : 'flex gap-3 items-start'"
        >
          <div
            v-if="msg.role === 'assistant'"
            class="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center shrink-0 mt-0.5"
          >
            <UIcon name="i-heroicons-sparkles" class="w-4 h-4 text-white" />
          </div>
          <div
            :class="[
              msg.role === 'user'
                ? 'text-sm leading-relaxed bg-gray-100 rounded-3xl px-5 py-3 max-w-xl'
                : msg.error
                  ? 'text-sm leading-relaxed text-red-500 max-w-2xl pt-1'
                  : 'text-sm max-w-2xl pt-1',
            ]"
          >
            <template v-if="msg.role === 'assistant' && !msg.error">
              <MarkdownMessage :text="msg.text" />
            </template>
            <template v-else>{{ msg.text }}</template>
          </div>
        </div>

        <!-- Loading indicator -->
        <div v-if="loading" class="flex gap-3 items-start">
          <div class="w-8 h-8 rounded-full bg-primary-500 flex items-center justify-center shrink-0 mt-0.5">
            <UIcon name="i-heroicons-sparkles" class="w-4 h-4 text-white" />
          </div>
          <div class="text-sm pt-1">Thinking…</div>
        </div>

        <!-- Provider selection -->
        <div v-if="step === 'provider_selection' && !loading" class="mt-2">
          <p class="text-xs mb-3">Choose a provider:</p>
          <p v-if="data.providers.length === 0" class="text-sm">No providers found for this specialty.</p>
          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div
              v-for="p in data.providers"
              :key="p.id"
              class="border border-gray-200 rounded-xl p-4 cursor-pointer hover:border-primary-400 hover:bg-primary-50 transition"
              @click="selectProvider(p)"
            >
              <p class="font-medium text-sm">Dr. {{ p.first_name }} {{ p.last_name }}</p>
              <p class="text-xs mt-0.5">{{ specialtyLabel(p.specialty) }}</p>
            </div>
          </div>
        </div>

        <!-- Slot selection -->
        <div v-if="step === 'slot_selection' && !loading" class="mt-2">
          <p class="text-xs mb-3">Choose a time slot:</p>
          <p v-if="data.slots.length === 0" class="text-sm">No slots available for this provider.</p>
          <div v-else class="flex flex-wrap gap-2">
            <button
              v-for="s in data.slots"
              :key="s.id"
              class="text-sm border border-gray-200 rounded-full px-4 py-1.5 hover:border-primary-400 hover:bg-primary-50 transition cursor-pointer"
              @click="selectSlot(s)"
            >
              {{ formatSlot(s) }}
            </button>
          </div>
        </div>

        <!-- Confirmation panel -->
        <div v-if="step === 'confirmation' && !loading" class="mt-2">
          <UCard>
            <template #header>
              <p class="text-sm font-semibold">Booking Summary</p>
            </template>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span>Provider</span>
                <span class="font-medium">Dr. {{ selectedProvider?.first_name }} {{ selectedProvider?.last_name }}</span>
              </div>
              <div class="flex justify-between">
                <span>Specialty</span>
                <span class="font-medium">{{ specialtyLabel(selectedProvider?.specialty) }}</span>
              </div>
              <div class="flex justify-between">
                <span>Date & Time</span>
                <span class="font-medium">{{ selectedSlot ? formatSlot(selectedSlot) : '—' }}</span>
              </div>
              <div v-if="data.draft?.reason" class="flex justify-between">
                <span>Reason</span>
                <span class="font-medium">{{ data.draft.reason }}</span>
              </div>
            </div>
            <template #footer>
              <UButton block @click="confirmBooking">Confirm Booking</UButton>
            </template>
          </UCard>
        </div>

        <!-- Completed panel -->
        <div v-if="step === 'completed'" class="mt-2">
          <UCard>
            <template #header>
              <div class="flex items-center gap-2">
                <UIcon name="i-heroicons-check-circle" class="text-green-400 w-5 h-5" />
                <p class="text-sm font-semibold">Appointment Booked!</p>
              </div>
            </template>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span>Provider</span>
                <span class="font-medium">{{ data.appointment?.provider_name }}</span>
              </div>
              <div class="flex justify-between">
                <span>Date & Time</span>
                <span class="font-medium">{{ data.appointment ? formatAppointmentDate(data.appointment.scheduled_at) : '—' }}</span>
              </div>
              <div class="flex justify-between">
                <span>Status</span>
                <UBadge color="warning" variant="soft" class="capitalize">{{ data.appointment?.status }}</UBadge>
              </div>
            </div>
            <template #footer>
              <UButton block variant="outline" color="neutral" :to="{ name: 'member-dashboard' }">
                Back to Dashboard
              </UButton>
            </template>
          </UCard>
        </div>

      </div>
    </div>

    <!-- Floating input (hidden after booking is completed) -->
    <div v-if="step !== 'completed'" class="absolute bottom-6 left-1/2 -translate-x-1/2 w-full max-w-4xl px-4 z-10">
      <div class="flex items-end gap-3 bg-white rounded-2xl shadow-[0_4px_24px_rgba(0,0,0,0.12)] border border-gray-200 px-4 py-3">
        <UTextarea
          v-model="input"
          placeholder="Message CareFlow AI…"
          :rows="1"
          autoresize
          :disabled="loading"
          class="flex-1 !border-none !shadow-none !ring-0 !bg-transparent resize-none"
          @keydown.enter.exact.prevent="send"
        />
        <UButton
          icon="i-heroicons-arrow-up"
          :disabled="!input.trim() || loading"
          :loading="loading"
          class="cursor-pointer rounded-full w-8 h-8 flex items-center justify-center shrink-0"
          @click="send"
        />
      </div>
      <p class="text-center text-xs mt-2">
        CareFlow AI can make mistakes. Always consult a qualified provider.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch, onMounted } from "vue";
import { useAuthStore } from "../../stores/auth.js";
import { sendChatMessage, getSessionId, setSessionId, clearSessionId, getSession } from "../../api/agent.js";
import MarkdownMessage from "../../components/MarkdownMessage.vue";

const SPECIALTY_LABELS = {
  GEN: "General Practice",
  CARD: "Cardiology",
  DERMA: "Dermatology",
  ENDO: "Endocrinology",
  GAST: "Gastroenterology",
  NEUR: "Neurology",
  PED: "Pediatrics",
  PSY: "Psychiatry",
  RAD: "Radiology",
  SURG: "Surgery",
};

const authStore = useAuthStore();
const firstName = authStore.user?.first_name ?? "there";

const messages  = ref([
  {
    role: "assistant",
    text: `Hi ${firstName}! I'm here to help you book the right appointment. What brings you in today?`,
  },
]);
const input            = ref("");
const loading          = ref(false);
const step             = ref("collecting_intent");
const data             = ref({ providers: [], slots: [], appointment: null, draft: {} });
const selectedProvider = ref(null);
const selectedSlot     = ref(null);
const messagesEl       = ref(null);
const rehydrating      = ref(false);

onMounted(async () => {
  const sessionId = getSessionId();
  if (!sessionId) return;

  rehydrating.value = true;
  try {
    const session = await getSession(sessionId);
    messages.value = [
      { role: "assistant", text: `Hi ${firstName}! I'm here to help you book the right appointment. What brings you in today?` },
      ...session.messages,
    ];
    step.value = session.step;
    data.value = session.data;
  } catch {
    clearSessionId();
  } finally {
    rehydrating.value = false;
    scrollToBottom();
  }
});

function scrollToBottom() {
  nextTick(() => {
    messagesEl.value?.scrollTo({ top: messagesEl.value.scrollHeight, behavior: "smooth" });
  });
}

watch(messages, scrollToBottom, { deep: true });

function specialtyLabel(code) {
  return SPECIALTY_LABELS[code] ?? code;
}

function formatSlot(slot) {
  const d = new Date(`${slot.date}T${slot.start_time}`);
  return d.toLocaleString(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatAppointmentDate(iso) {
  return new Date(iso).toLocaleString(undefined, {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function selectProvider(p) {
  selectedProvider.value = p;
  input.value = `I'd like to book with Dr. ${p.first_name} ${p.last_name} (provider ID: ${p.id})`;
  send();
}

function selectSlot(s) {
  selectedSlot.value = s;
  input.value = `I'll take the slot on ${s.date} at ${s.start_time} (slot ID: ${s.id})`;
  send();
}

function confirmBooking() {
  input.value = "Yes, please confirm my booking";
  send();
}

async function send() {
  const text = input.value.trim();
  if (!text || loading.value) return;

  messages.value.push({ role: "user", text });
  input.value = "";
  loading.value = true;

  try {
    const sessionId = getSessionId();
    const res = await sendChatMessage(sessionId, text);
    if (res.step === "completed") {
      clearSessionId();
    } else {
      setSessionId(res.session_id);
    }
    step.value = res.step;
    data.value = res.data;
    messages.value.push({ role: "assistant", text: res.reply });
  } catch (err) {
    messages.value.push({ role: "assistant", text: err.message, error: true });
  } finally {
    loading.value = false;
  }
}
</script>
