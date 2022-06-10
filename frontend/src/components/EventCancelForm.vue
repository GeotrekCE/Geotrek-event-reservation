<template>
  <v-dialog v-model="dialogCancel" max-width="600px">
    <template v-slot:activator="{ editedItem }">
      <v-btn color="error" dark v-bind="editedItem" @click="editItem">
        {{ titleCancel }}
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span v-if="!this.canceled" class="text-h5">Annuler animation</span>
        <span v-else class="text-h5">Etes vous sur de vouloir dé-annuler l'animation?</span>
      </v-card-title>
      <v-card-text>
        <v-container v-if="!this.canceled">
          <v-form ref="cancel_form" v-model="formValid" lazy-validation>
            <v-row>
              <v-col cols="12">
                <v-textarea outlined label="Raison annulation"
                  v-model="editedItem.raison_annulation" :rules="[rules.required]"></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-container>
        <v-container v-else>
          <strong></strong>
        </v-container>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="dialogCancel = false">
          Fermer
        </v-btn>
        <v-btn color="blue darken-1" text @click="cancelAnimation" :disabled="!formValid">
          Enregistrer
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters } from 'vuex';
import { postOneBilan } from '@/services/appli_api.js'
import { rulesFct } from '@/utils/fields.js'

export default {

  data() {
    return {
      dialogCancel: false,
      editedItem: {},
      formValid: false,
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
    },
    rules() {
      return rulesFct;
    }
  },
  mounted() {
    setTimeout(() => {
      if (this.$refs.cancel_form) {
        (this.$refs.cancel_form).validate();
      }
    }, 2000);
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
      console.log(this.editedItem.canceled)
      if (this.editedItem.annulation === false) {
        this.editedItem.raison_annulation = '';
      }
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
