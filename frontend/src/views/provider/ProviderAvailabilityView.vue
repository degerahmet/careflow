<template>
  <div class="flex min-h-screen bg-gray-50">
    <ProviderSidebar :collapsed="sidebarCollapsed" @toggle="sidebarCollapsed = !sidebarCollapsed" />

    <main class="flex-1 overflow-y-auto">
      <div class="p-6 max-w-3xl mx-auto space-y-6">
        <h1 class="text-xl font-semibold">Availability</h1>

        <!-- Date picker -->
        <div class="space-y-1">
          <label class="text-sm font-medium">Select date</label>
          <input
            v-model="selectedDate"
            type="date"
            class="block border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 [color-scheme:light]"
            @change="selected = new Set()"
          />
        </div>
        <!-- Legend -->
         <div class="flex items-center gap-4 text-xs">
           <span class="flex items-center gap-1">
             <span class="w-3 h-3 rounded bg-green-100 border border-green-400 inline-block" />
             Saved (click to remove)
           </span>
           <span class="flex items-center gap-1">
             <span class="w-3 h-3 rounded bg-primary-100 border border-primary-400 inline-block" />
             Selected
           </span>
           <span class="flex items-center gap-1">
             <span class="w-3 h-3 rounded bg-white border border-gray-300 inline-block" />
             Available
           </span>
         </div>

        <!-- Loading -->
        <div v-if="loading" class="flex items-center justify-center py-16">
          <UIcon name="i-lucide-loader-circle" class="animate-spin text-3xl" />
        </div>

        <!-- Error -->
        <div v-else-if="error" class="space-y-3">
          <UAlert color="error" variant="soft" :description="error" />
          <UButton variant="outline" size="sm" @click="load">Try again</UButton>
        </div>
        

        <!-- Slot grid -->
        <div v-else class="space-y-4">
          <div class="grid grid-cols-4 gap-2 sm:grid-cols-5">
            <button
              v-for="slot in ALL_SLOTS"
              :key="slot"
              type="button"
              :class="slotClass(slot)"
              :disabled="saving"
              @click="toggleSlot(slot)"
            >
              <span class="text-xs font-medium">{{ formatSlotLabel(slot) }}</span>
              <UIcon
                v-if="savedStartTimes.has(slot)"
                name="i-lucide-x"
                class="text-xs ml-1 shrink-0 "
              />
            </button>
          </div>

         

          <!-- Save button -->
          <div class="pt-2">
            <UButton
              :disabled="selected.size === 0 || saving"
              :loading="saving"
              @click="saveSlots"
            >
              Save {{ selected.size > 0 ? `${selected.size} slot${selected.size > 1 ? 's' : ''}` : 'slots' }}
            </UButton>
          </div>

          <!-- Save error -->
          <UAlert v-if="saveError" color="error" variant="soft" :description="saveError" />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import { getAvailability, createSlot, deleteSlot } from "../../api/availability.js";
import ProviderSidebar from "../../components/ProviderSidebar.vue";

const sidebarCollapsed = ref(false);

// Today as YYYY-MM-DD
function today() {
  return new Date().toISOString().slice(0, 10);
}

// "08:00:00" → "08:30:00"
function addThirtyMin(time) {
  const [h, m] = time.split(":").map(Number);
  const total = h * 60 + m + 30;
  return `${String(Math.floor(total / 60)).padStart(2, "0")}:${String(total % 60).padStart(2, "0")}:00`;
}

// 08:00 – 17:30, 20 slots
const ALL_SLOTS = Array.from({ length: 20 }, (_, i) => {
  const total = i * 30 + 480; // 480 = 8*60
  return `${String(Math.floor(total / 60)).padStart(2, "0")}:${String(total % 60).padStart(2, "0")}:00`;
});

function formatSlotLabel(time) {
  const [h, m] = time.split(":");
  return `${h}:${m}`;
}

const selectedDate = ref(today());
const allSlots = ref([]);
const selected = ref(new Set());
const loading = ref(false);
const error = ref(null);
const saving = ref(false);
const saveError = ref(null);

const savedForDate = computed(() =>
  allSlots.value.filter((s) => s.date === selectedDate.value)
);

const savedStartTimes = computed(() =>
  new Set(savedForDate.value.map((s) => s.start_time))
);

function slotClass(slot) {
  const base = "flex items-center justify-center rounded-lg px-2 py-2 border transition-colors";
  if (savedStartTimes.value.has(slot)) {
    return `${base} bg-green-50 border-green-400 text-green-700 hover:bg-green-100`;
  }
  if (selected.value.has(slot)) {
    return `${base} bg-primary-50 border-primary-400 text-primary-700 hover:bg-primary-100`;
  }
  return `${base} bg-white border-gray-300 hover:bg-gray-50`;
}

function toggleSlot(slot) {
  if (savedStartTimes.value.has(slot)) {
    removeSavedSlot(slot);
    return;
  }
  const next = new Set(selected.value);
  if (next.has(slot)) {
    next.delete(slot);
  } else {
    next.add(slot);
  }
  selected.value = next;
}

async function removeSavedSlot(startTime) {
  const slot = savedForDate.value.find((s) => s.start_time === startTime);
  if (!slot) return;
  try {
    await deleteSlot(slot.id);
    allSlots.value = allSlots.value.filter((s) => s.id !== slot.id);
  } catch (err) {
    saveError.value = err.message;
  }
}

async function saveSlots() {
  saving.value = true;
  saveError.value = null;
  try {
    for (const start of selected.value) {
      const end = addThirtyMin(start);
      const created = await createSlot(selectedDate.value, start, end);
      allSlots.value = [...allSlots.value, created];
    }
    selected.value = new Set();
  } catch (err) {
    saveError.value = err.message;
  } finally {
    saving.value = false;
  }
}

async function load() {
  loading.value = true;
  error.value = null;
  try {
    allSlots.value = await getAvailability();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}

load();
</script>
