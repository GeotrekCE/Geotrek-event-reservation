<template>
  <v-container>
    <div v-html="markdownToHtml"></div>
  </v-container>
</template>

<script>
import { marked } from 'marked';

export default {
  data() {
    return {
      markdownToHtml: 'Aucun contenu'
    };
  },
  computed: {
  },
  mounted() {
    fetch('informations.md')
      .then((response) => response.text())
      .then((textString) => {
        this.markdownToHtml = marked(textString);
      }).catch((error) => {
        this.markdownToHtml = 'Error when retrive informations.md'
      });
  }
}

</script>
