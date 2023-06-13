<template>
  <v-dialog v-model="dialogCancel" max-width="600px">
    <template v-slot:activator="{ props }">
      <v-btn color="error" dark v-bind="props" @click="editItem">
        {{ titleCancel }}
      </v-btn>
    </template>
    <v-card>
      <v-card-title>
        <span v-if="!canceled" class="text-h5">Annuler animation</span>
        <span v-else class="text-h5">Etes vous sur de vouloir dé-annuler l'animation?</span>
      </v-card-title>
      <v-card-text>
        <v-container v-if="!canceled">
          <v-form ref="form" v-model="formValid" lazy-validation>
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
        <v-btn color="blue darken-1" @click="dialogCancel = false">
          Fermer
        </v-btn>
        <v-btn color="blue darken-1" @click="cancelAnimation" :disabled="!formValid">
          Enregistrer
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import type { ResaBilan } from '@/declaration';
import { postBilan } from '@/utils/appli_api'
import { rulesFct } from '@/utils/fields'

export default {

  data() {
    return {
      dialogCancel: false,
      editedItem: {} as ResaBilan,
      formValid: true
    };
  },
  props: ['bilan', 'canceled', 'id_event', 'user'],
  computed: {
    titleCancel() {
      if (this.canceled) {
        return 'De-annuler';
      }
      return 'Annuler';
    },
    rules() {
      return rulesFct;
    },
  },
  mounted() {
  },
  methods: {
    editItem() {
      if (this.bilan) {
        this.editedItem = { ...this.bilan };
      }
      this.editedItem.annulation = !this.canceled;
      if (this.editedItem.annulation) {
        setTimeout(() => {
          // @ts-expect-error
          this.$refs.form?.validate();
        }, 500);
      }
      this.dialogCancel = true;
    },

    cancelAnimation() {
      // Set digitizer
      this.editedItem.id_numerisateur = this.user.id_role;
      this.editedItem.id_event = this.id_event;
      if (this.editedItem.annulation === false) {
        this.editedItem.raison_annulation = '';
      }
      postBilan(this.editedItem).then(() => {
        this.$emit('reloadEvent');
      });

      this.dialogCancel = false
    },
  },
}
</script>

<style>

</style>
