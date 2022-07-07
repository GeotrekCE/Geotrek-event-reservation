<template>
  <v-menu v-model="menu2" :close-on-content-click="false" transition="scale-transition" offset-y
    max-width="290px" min-width="290px">
    <template v-slot:activator="{ on, attrs }">
      <v-text-field v-model="computedDateFormatted" :label="label" persistent-hint
        prepend-icon="mdi-calendar" readonly v-bind="attrs" v-on="on"></v-text-field>
    </template>
    <v-date-picker v-model="dateSelected" no-title @input="menu2 = false"
      v-on:input="$emit('input', $event)"></v-date-picker>
  </v-menu>
</template>
<script>
export default {
  data() {
    return {
      dateFormatted: '',
      dateSelected: this.dateValue,
      menu2: false,
    };
  },
  props: {
    label: {
      type: String,
      required: true,
    },
    dateValue: {
      required: true,
    },
  },
  computed: {
    computedDateFormatted() {
      return this.formatDate(this.dateValue);
    },
  },
  methods: {
    handleInput(e) {
      const { value } = e.target.value;
      this.dateSelected = value;
      this.$emit('input', value);
    },
    formatDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split('-');
      return `${day}/${month}/${year}`;
    },
    focusDate() {
      setTimeout(() => {
        if (!this.dateMenu) {
          this.dateMenu = true;
        }
      }, 200);
    },
    blurDate() {
      setTimeout(() => {
        if (this.dateMenu) {
          this.dateMenu = false;
        }
      }, 200);
    },
  },
};
</script>
