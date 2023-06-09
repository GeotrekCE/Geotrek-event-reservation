<template>
  <v-container>
    <div v-if="loading">Loading...</div>
    <div v-html="markdownToHTML" v-else></div>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { marked } from 'marked';

const markdownToHTML = ref('')
const loading = ref(false)

onMounted(async() => {
  loading.value = true
  const response = await fetch('informations.md')
  const text = await response.text()
  markdownToHTML.value = marked(text) || 'Error when retrive informations.md'
  loading.value = false
})
</script>
