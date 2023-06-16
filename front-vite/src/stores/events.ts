import { ref } from 'vue'
import { defineStore } from 'pinia'
import type { ResaEventFilters } from '@/declaration';

export const useEventStore = defineStore('event', () => {
  const filters = ref<Partial<ResaEventFilters>>({
      begin_date: undefined,
      end_date: undefined,
      search_name: undefined,
      cancelled: undefined,
      published: true,
    })

  function resetFilters() {
    (Object.keys(filters.value) as Array<keyof ResaEventFilters>)
    .forEach(key => {
      filters.value[key] = undefined
    });
    filters.value.published = true;
  }

  return { filters, resetFilters }
})
