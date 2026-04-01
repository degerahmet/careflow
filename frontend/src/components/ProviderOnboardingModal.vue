<template>
  <UModal
    :open="true"
    :dismissible="false"
    :close="false"
    title="Complete Your Profile"
    description="Tell patients a bit about yourself before continuing."
  >
    <template #body>
      <form class="space-y-4" @submit.prevent="handleSubmit">
        <UFormField label="Specialty" required>
          <USelect
            v-model="specialty"
            :items="SPECIALTIES"
            value-key="value"
            label-key="label"
            placeholder="Select a specialty"
            :disabled="loading"
            class="w-full"
          />
        </UFormField>

        <UFormField label="Bio" required>
          <UTextarea
            v-model="bio"
            placeholder="Describe your background, experience, and approach to care…"
            :rows="4"
            :disabled="loading"
            class="w-full"
          />
        </UFormField>

        <UAlert
          v-if="error"
          color="error"
          variant="soft"
          :description="error"
        />

        <UButton type="submit" block :loading="loading">
          Save and continue
        </UButton>
      </form>
    </template>
  </UModal>
</template>

<script setup>
import { ref } from "vue";
import { SPECIALTIES } from "../constants/specialties.js";
import { updateProfile } from "../api/provider.js";

const emit = defineEmits(["complete"]);

const specialty = ref("");
const bio = ref("");
const loading = ref(false);
const error = ref(null);

async function handleSubmit() {
  if (!specialty.value || !bio.value.trim()) {
    error.value = "Both specialty and bio are required.";
    return;
  }

  loading.value = true;
  error.value = null;

  try {
    await updateProfile(specialty.value, bio.value.trim());
    emit("complete");
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}
</script>
