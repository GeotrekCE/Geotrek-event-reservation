<template>
  <v-container name="event-list">
    <v-card>
      <v-card-title>
          Bilan de l'animation
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="dialogBilan = true">{{ btnTitle }}</v-btn>
      </v-card-title>
      <v-card-text>
        <div v-if="event.bilan">
          <div
            v-for="(field, index) in liste_champs_nb"
            :key="index"
          >
            <strong>{{ field }}</strong> : {{ event.bilan[index] }}
          </div>
          <div><strong>Commentaire</strong> : {{ event.bilan.commentaire }}</div>
        </div>
      </v-card-text>
    </v-card>

    <v-dialog v-model="dialogBilan" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">
              Bilan
            </v-card-title>
            <v-card-text>
              <v-form>
                <v-row>
                  <v-col
                    cols="12" sm="6" md="6"
                    v-for="(field, index) in liste_champs_nb"
                    :key="index">
                    <v-text-field v-model="editedItem[index]"
                      min="0"
                      :rules="[rules.integer]"
                      :label="field">
                    </v-text-field>
                  </v-col>
                </v-row>
                <v-row>
                    <v-textarea outlined v-model="editedItem.commentaire" label="Commentaire">
                    </v-textarea>
                </v-row>
              </v-form>
            </v-card-text>
            <v-spacer></v-spacer>
            <v-card-actions>
              <v-btn color="blue darken-1" text @click="closeModal">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="save">OK</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import { fieldsClasseAge, rulesFct } from '@/utils/fields.js'

import { postOneBilan } from '@/services/appli_api'

export default {
  props: ['event'],
  data() {
    return {
      dialogBilan: false,
      editedItem: {}
    }
  },
  computed: {
    ...mapGetters(['user']),

    btnTitle() {
      if (this.event.bilan) {
        return 'Modifier bilan';
      }
      return 'Saisir bilan';
    },
    liste_champs_nb() {
      return fieldsClasseAge
    },
    rules() {
      return rulesFct
    },
    defaultItem() {
      const fieldsnb = Object.keys(
        this.liste_champs_nb
      ).reduce((o, key) => ({ ...o, [key]: 0 }), {});
      console.log(fieldsnb)
      return {
        ...{
          commentaire: '',
          id_event: this.event.id,
          id_numerisateur: this.user.id_role
        },
        ...fieldsnb
      }
    },
    formTitle() {
      return this.editedItem.id_bilan === undefined ? 'Saisir bilan' : 'Editer bilan'
    },
  },
  watch: {
    dialogBilan(val) {
      if (val) {
        if (this.event.bilan) {
          this.editItem();
        } else {
          this.addItem();
        }
      } else {
        this.closeModal();
      }
    },
  },
  mounted() {
    setTimeout(() => {
      if (this.$refs.reservation_form) {
        (this.$refs.reservation_form).validate();
      }
    }, 2000);
  },
  methods: {
    addItem() {
      this.editedItem = { ...this.defaultItem };
      this.numerisateurName = undefined;
      this.dialogBilan = true;
    },

    editItem() {
      this.editedItem = { ...this.event.bilan };
      // this.numerisateurName = this.event.bilan.numerisateur
      //   ? this.event.bilan.numerisateur.identifiant
      //   : undefined;

      this.editedItem.id_numerisateur = this.user.id_role;
      this.dialogBilan = true;
    },

    closeModal() {
      this.dialogBilan = false
      this.$nextTick(() => {
        this.editedItem = this.defaultItem;
      })
    },

    save() {
      // Set digitizer
      this.editedItem.id_numerisateur = this.user.id_role;

      postOneBilan(this.editedItem).then((data) => {
        this.$emit('reloadEvent');
      })
      this.closeModal()
    },
  }
}
</script>
