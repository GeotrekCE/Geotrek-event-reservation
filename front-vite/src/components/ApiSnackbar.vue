<template>
  <v-snackbar
    :color="props.snackbarColor"
    timeout="-1"
  >
    {{ props.snackbarMessage }}
    <template v-slot:actions>
      <v-btn @click="emits('close')">
        <v-icon>mdi-window-close</v-icon>
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script setup lang="ts">
const props = defineProps({
  snackbarMessage: String,
  snackbarColor: String
})
const emits = defineEmits(['close'])
</script>