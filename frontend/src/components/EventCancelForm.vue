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
      console.log(this.bilan, this.editedItem);
    },

    cancelAnimation() {
      // Set digitizer
      this.editedItem.id_numerisateur = this.user.id_role;
      this.editedItem.id_event = this.id_event;
      console.log(this.editedItem);
      postOneBilan(this.editedItem).then((data) => {
        // this.snackbarInfo = {
        //   message: 'Données sauvegardées',
        //   color: 'success',
        //   show: true
        // };
        this.$emit('reloadEvent');
      }).catch((error) => {
        // this.snackbarInfo = {
        //   message: 'Erreur dans la sauvegarde',
        //   color: 'error',
        //   show: true
        // }
        console.error('There was an error!', error);
      });
      console.log('cancel');
      this.dialogCancel = false
    },
  },
}
</script>

<style>

</style>
