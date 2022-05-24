<template>
  <v-dialog
    v-model="dialogCancel"
    max-width="600px"
  >
    <template v-slot:activator="{ editedItem }">
      <v-btn
        color="error"
        dark
        v-bind="editedItem"
        @click="editItem"
      >
      {{titleCancel}}
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span class="text-h5">Annuler animation</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col
              cols="12"
            >
              <v-textarea
                outlined
                label="Raison annulation"
                v-model="editedItem.raison_annulation"
                required
              ></v-textarea>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="blue darken-1"
          text
          @click="dialogCancel = false"
        >
          Fermer
        </v-btn>
        <v-btn
          color="blue darken-1"
          text
          @click="cancelAnimation"
        >
          Enregistrer
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters } from 'vuex';
import { postOneBilan } from '@/services/appli_api.js'

export default {

  data() {
    return {
      dialogCancel: false,
      editedItem: {},
    };
  },
  props: ['bilan', 'canceled', 'id_event'],
  computed: {
    ...mapGetters(['user']),
    titleCancel() {
      if (this.canceled) {
        return 'De-annuler';
      }
      return 'Annuler';
    }
  },
  methods: {
    editItem(item) {
      if (this.bilan) {
        this.editedItem = { ...this.bilan };
      }
      this.editedItem.annulation = !this.canceled;
      this.dialogCancel = true;
    },

    cancelAnimation() {
      // Set digitizer
      this.editedItem.id_numerisateur = this.user.id_role;
      this.editedItem.id_event = this.id_event;
      postOneBilan(this.editedItem).then((data) => {
        this.$emit('reloadEvent');
      });

      this.dialogCancel = false
    },
  },
}
</script>

<style>

</style>
