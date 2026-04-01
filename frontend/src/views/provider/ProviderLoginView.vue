<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <UCard class="w-full max-w-md">
      <template #header>
        <h1 class="text-xl font-semibold text-gray-900">Provider Login</h1>
      </template>

      <form class="space-y-4" @submit.prevent="handleSubmit">
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
            autocomplete="current-password"
            placeholder="••••••••"
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
          Sign in
        </UButton>
      </form>

      <template #footer>
        <div class="flex flex-col gap-2 text-sm">
          <RouterLink
            :to="{ name: 'provider-signup' }"
            class="text-primary-500 hover:underline"
          >
            Create a provider account
          </RouterLink>
          <RouterLink
            :to="{ name: 'member-login' }"
            class="text-gray-500 hover:underline"
          >
            Member login
          </RouterLink>
        </div>
      </template>
    </UCard>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { providerLogin } from "../../api/auth.js";
import { useAuthStore } from "../../stores/auth.js";

const router = useRouter();
const authStore = useAuthStore();

const email = ref("");
const password = ref("");
const loading = ref(false);
const error = ref(null);

async function handleSubmit() {
  loading.value = true;
  error.value = null;

  try {
    const data = await providerLogin(email.value, password.value);
    authStore.setAuth(data);
    router.push({ name: "provider-dashboard" });
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}
</script>
