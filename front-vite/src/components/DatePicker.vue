<template>
  <v-menu
    v-model="menu2"
    :close-on-content-click="false"
    transition="scale-transition"
    offset-y
    max-width="290px"
    min-width="290px"
  >
    <template v-slot:activator="{ props }">
      <v-text-field
        v-model="computedDateFormatted"
        :label="label"
        persistent-hint
        prepend-icon="mdi-calendar"
        readonly
        v-bind="props"
      />
    </template>
    <v-date-picker
      v-model="dateSelected"
      no-title
      @input="menu2 = false"
      v-on:input="$emit('input', $event)"
    />
  </v-menu>
</template>
<script lang="ts">
export default {
  props: {
    label: {
      type: String,
      required: true,
    },
    dateValue: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      dateSelected: this.dateValue,
      menu2: false,
    };
  },
  computed: {
    computedDateFormatted() {
      if (!this.dateValue) return null;
      const [year, month, day] = this.dateValue.split('-');
      return `${day}/${month}/${year}`;
    },
  },
};
</script>
