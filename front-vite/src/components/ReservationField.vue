<template>
  <span v-if="value">
    <label class="block text-sm font-medium leading-6 text-gray-900">{{ field.label }} : </label>
    <span v-if="field.type === 'boolean'">
      {{ Boolean(value) === true ? 'oui' : (Boolean(value) === false ? 'non' : 'pas de valeur') }}
    </span>
    <span v-else-if="field.type === 'date'">
      {{ formatDateTimeString(value as string) }}
    </span>
    <template v-else-if="field.type === 'paragraph'">
      <p
        v-for="comment in (value as string).split('\n')"
        :key="comment"
      >
        {{ comment }}
      </p>
    </template>
    <span v-else>
      {{ value }}
    </span>
  </span>
</template>

<script setup lang="ts">
import type { ResaField } from '@/declaration'
import { formatDateTimeString } from '@/utils/formatDate'

defineProps<{
  field: ResaField
  value: string | number | boolean
}>()
</script>