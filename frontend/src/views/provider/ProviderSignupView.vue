<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="w-full max-w-md space-y-4">
      <h2 class="text-2xl font-bold text-gray-900 text-center">Provider Signup</h2>
      <UCard>
      <template #header>
        <h1 class="text-xl font-semibold text-gray-900">Create Provider Account</h1>
      </template>

      <form class="space-y-4" @submit.prevent="handleSubmit">
        <div class="grid grid-cols-2 gap-4">
          <UFormField label="First name" required>
            <UInput
              v-model="firstName"
              type="text"
              autocomplete="given-name"
              placeholder="Jane"
              :disabled="loading"
              class="w-full"
            />
          </UFormField>

          <UFormField label="Last name" required>
            <UInput
              v-model="lastName"
              type="text"
              autocomplete="family-name"
              placeholder="Smith"
              :disabled="loading"
              class="w-full"
            />
          </UFormField>
        </div>

        <UFormField label="Email" required>
          <UInput
            v-model="email"
            type="email"
            autocomplete="email"
            placeholder="you@example.com"
            :disabled="loading"
            class="w-full"
          />
        </UFormField>

        <UFormField label="Password" required>
          <UInput
            v-model="password"
            type="password"
            autocomplete="new-password"
            placeholder="Min. 8 characters"
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
          Create account
        </UButton>
      </form>

      <template #footer>
        <div class="text-sm">
          <RouterLink
            :to="{ name: 'provider-login' }"
            class="text-primary-500 hover:underline"
          >
            Already have an account? Sign in
          </RouterLink>
        </div>
      </template>
      </UCard>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { providerSignup } from "../../api/auth.js";
import { useAuthStore } from "../../stores/auth.js";

const router = useRouter();
const authStore = useAuthStore();

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const password = ref("");
const loading = ref(false);
const error = ref(null);

async function handleSubmit() {
  loading.value = true;
  error.value = null;

  try {
    const data = await providerSignup(email.value, password.value, firstName.value, lastName.value);
    authStore.setAuth(data);
    router.push({ name: "provider-dashboard" });
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}
</script>
