<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="w-full max-w-md space-y-4">
      <h2 class="text-2xl font-bold text-gray-900 text-center">Member Login</h2>
      <UCard>
      <template #header>
        <h1 class="text-xl font-semibold text-gray-900">Member Login</h1>
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

        <UAlert v-if="error" color="error" variant="soft" :description="error" />

        <UButton type="submit" block :loading="loading">
          Sign in
        </UButton>
      </form>

      <template #footer>
        <div class="flex flex-col gap-3">
          <UButton block variant="outline" color="neutral" :to="{ name: 'member-signup' }">
            Sign up
          </UButton>
          <UButton block variant="outline" color="neutral" class="!border !border-white/40 !font-bold" :to="{ name: 'provider-login' }">
            I'm a provider
          </UButton>
        </div>
      </template>
      </UCard>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { memberLogin } from "../../api/auth.js";
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
    const data = await memberLogin(email.value, password.value);
    authStore.setAuth(data);
    router.push({ name: "member-dashboard" });
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
}
</script>
