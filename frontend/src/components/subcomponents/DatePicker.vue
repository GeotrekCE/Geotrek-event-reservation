<template>
    <v-menu
      v-model="menu2"
      :close-on-content-click="false"
      transition="scale-transition"
      offset-y
      max-width="290px"
      min-width="290px"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-text-field
          v-model="computedDateFormatted"
          :label="label"
          persistent-hint
          prepend-icon="mdi-calendar"
          readonly
          v-bind="attrs"
          v-on="on"
        ></v-text-field>
      </template>
      <v-date-picker v-model="date" no-title @input="menu2 = false"
        v-on:input="$emit('input', $event)" ></v-date-picker>
    </v-menu>
</template>
<script>
export default {
  data() {
    return {
      date: this.dateValue,
      dateFormatted: '',
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
      return this.formatDate(this.date);
    },
  },
  methods: {
    handleInput(e) {
      const { value } = e.target.value;
      this.date = value;
      this.$emit('input', value);
    },
    formatDate(dateValue) {
      if (!dateValue) return null;
      const [year, month, day] = dateValue.split('-');
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
