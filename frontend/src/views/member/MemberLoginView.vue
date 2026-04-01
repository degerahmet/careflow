<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <UCard class="w-full max-w-md">
      <template #header>
        <h1 class="text-xl font-semibold text-gray-900">Member Login</h1>
      </template>

      <p class="text-gray-500 text-sm">Member login — coming soon.</p>

      <template #footer>
        <div class="text-sm">
          <RouterLink
            :to="{ name: 'provider-login' }"
            class="text-primary-500 hover:underline"
          >
            Provider login
          </RouterLink>
        </div>
      </template>
    </UCard>
  </div>
</template>
