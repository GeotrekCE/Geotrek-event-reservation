<template>
  <vv-form @submit="values => emits('submit', values)" class="mt-4" :validation-schema="formSchema"
    :initial-values="formValues" v-slot="{ errors }">
  
    <div class="card flex justify-content-center">
      <button @click="showTemplate()" label="Save">Save</button>
    </div>
    <div class="space-y-12">
  
      <div class="border-b border-gray-900/10 pb-12">
        <h2 class="text-base font-medium leading-7 text-gray-900">Informations personnelles</h2>
        <p class="mt-1 text-sm leading-6 text-gray-600">Utilisez une adresse mail sur laquelle vous pouvez vous connecter.
        </p>
        
        <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
        
          <div class="col-span-1 sm:col-span-3">
            <label for="prenom" class="block text-sm font-medium leading-6 text-gray-900">Prénom</label>
            <div class="mt-2">
              <vv-field type="text" name="prenom" id="prenom" autocomplete="given-name"
                class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6" />
              <vv-error-message name="prenom" />
            </div>
          </div>
        
          <div class="col-span-1 sm:col-span-3">
            <label for="nom" class="block text-sm font-medium leading-6 text-gray-900">Nom</label>
            <div class="mt-2">
              <vv-field type="text" name="nom" id="nom" autocomplete="family-name"
                class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6" />
              <vv-error-message name="nom" />
            </div>
          </div>
        
          <div class="col-span-1 sm:col-span-2">
            <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email</label>
            <div class="mt-2">
              <vv-field id="email" name="email" type="email" autocomplete="email"
                class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6" />
              <vv-error-message name="email" />
            </div>
          </div>
        
          <div class="col-span-1 sm:col-span-2">
            <label for="tel" class="block text-sm font-medium leading-6 text-gray-900">Téléphone</label>
            <div class="mt-2">
              <vv-field type="text" name="tel" id="tel" autocomplete="tel"
                class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6" />
              <vv-error-message name="tel" />
            </div>
          </div>
        
          <div class="col-span-1 sm:col-span-2">
            <label for="num_departement" class="block text-sm font-medium leading-6 text-gray-900">Lieu d'origine</label>
            <div class="mt-2">
              <vv-field id="num_departement" name="num_departement" autocomplete="num_departement" as="select"
                class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 text-sm leading-6 h-10">
                <option v-for="o in origins" :key="o.value" :value="o.value">
                  {{ o.label }}
                </option>
              </vv-field>
              <vv-error-message name="num_departement" />
            </div>
          </div>
        
        </div>
        </div>
        
        <div class="border-b border-gray-900/10 pb-12">
          <h2 class="text-base font-medium leading-7 text-gray-900">Informations sur les participants</h2>
          <p class="mt-1 text-sm leading-6 text-gray-600">
            Merci de préciser le nombre de participants par tranche d'âge.
          </p>
        
          <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-10">
            <div class="sm:col-span-2">
              <label for="nb_adultes" class="block text-sm font-medium leading-6 text-gray-900">Adulte(s)</label>
              <div class="mt-2">
                <vv-field type="number" name="nb_adultes" id="nb_adultes" min="0"
                  class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6" />
        
                <vv-error-message name="nb_adultes" />
              </div>
            </div>
            <div class="sm:col-span-2">
              <label for="nb_moins_6_ans" class="block text-sm font-medium leading-6 text-gray-900">Moins de 6 ans</label>
              <div class="mt-2">
                <vv-field type="number" name="nb_moins_6_ans" id="nb_moins_6_ans" min="0"
                  class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6" />
        
                <vv-error-message name="nb_moins_6_ans" />
              </div>
            </div>
            <div class="sm:col-span-2">
              <label for="nb_6_8_ans" class="block text-sm font-medium leading-6 text-gray-900">6 - 8 ans</label>
              <div class="mt-2">
                <vv-field type="number" name="nb_6_8_ans" id="nb_6_8_ans" min="0"
                  class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6" />
        
                <vv-error-message name="nb_6_8_ans" />
              </div>
            </div>
            <div class="sm:col-span-2">
              <label for="nb_9_12_ans" class="block text-sm font-medium leading-6 text-gray-900">9 - 12 ans</label>
              <div class="mt-2">
                <vv-field type="number" name="nb_9_12_ans" id="nb_9_12_ans" min="0"
                  class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6" />
        
                <vv-error-message name="nb_9_12_ans" />
              </div>
            </div>
            <div class="sm:col-span-2">
              <label for="nb_plus_12_ans" class="block text-sm font-medium leading-6 text-gray-900">Plus de 12 ans</label>
              <div class="mt-2">
                <vv-field type="number" name="nb_plus_12_ans" id="nb_plus_12_ans" min="0"
                  class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6" />
        
                <vv-error-message name="nb_plus_12_ans" />
              </div>
            </div>
        
            <div class="sm:col-span-12">
              <vv-error-message name="nb_total" />
            </div>
          </div>
        </div>
        
        <div class="border-b border-gray-900/10 pb-12" v-if="displayAdminFields">
          <h2 class="text-base font-medium leading-7 text-gray-900">Informations administrateurs</h2>
          <p class="mt-1 text-sm leading-6 text-gray-600">
            Informations saisissables uniquement par les administrateurs.
          </p>
        
          <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-10">
            <div class="sm:col-span-2">
              <label for="liste_attente" class="block text-sm font-medium leading-6 text-gray-900">En liste
                d'attente</label>
              <div class="mt-2">
                <vv-field name="liste_attente" id="liste_attente" as="select"
                  class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 text-sm leading-6 h-10">
                  <option :value="true">Sur liste d'attente</option>
                  <option :value="false">Comptabilisée</option>
                </vv-field>
        
                <vv-error-message name="liste_attente" />
              </div>
            </div>
            <div class="sm:col-span-2">
              <label for="confirmed" class="block text-sm font-medium leading-6 text-gray-900">Confirmée par le
                créateur</label>
              <div class="mt-2">
                <vv-field name="confirmed" id="confirmed" as="select"
                  class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 text-sm leading-6 h-10">
                  <option :value="true">Confirmée</option>
                  <option :value="false">En attente de confirmation</option>
                </vv-field>
        
                <vv-error-message name="confirmed" />
              </div>
            </div>
          </div>
        </div>
        
        <div class="border-b border-gray-900/10 pb-12">
          <h2 class="text-base font-medium leading-7 text-gray-900">Commentaire</h2>
          <p class="mt-1 text-sm leading-6 text-gray-600">
            Vous souhaitez préciser certains points sur votre réservation, vous pouvez les inscrire ici.
          </p>
        
        
          <div class="col-span-full">
            <div class="mt-2">
              <vv-field id="commentaire" name="commentaire" rows="3" as="textarea"
                class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 sm:text-sm sm:leading-6" />
              <vv-error-message name="commentaire" />
            </div>
          </div>
        </div>
        </div>
        
        <div class="my-6 flex flex-col items-end gap-x-6">
          <div class="flex">
            <button class="rounded-sm mr-4 px-3 py-2 text-sm font-medium text-white shadow-sm bg-sky-600 hover:bg-sky-500"
              @click="emits('cancel')">
              Annuler
            </button>
        
            <button type="submit" class="rounded-sm px-3 py-2 text-sm font-medium text-white shadow-sm"
              :class="{
                'bg-sky-600': !saving,
                'hover:bg-sky-500': !saving,
                'bg-sky-100': saving,
                'hover:bg-sky-100': saving,
                'text-black': saving,
                                                                                                                                                                                                                                                                                                                                                                                                                                                      }"
              :disabled="saving">
              {{ saving ? 'Enregistrement en cours...' : 'Enregistrer réservation' }}
            </button>
          </div>
          <span v-if="Object.keys(errors).length === 1" class="text-red-500">
            Une erreur est présente dans le formulaire (champ {{ Object.keys(errors)[0] }}).
            Merci de la corriger avant de soumettre à nouveau le formulaire
          </span>
          <span v-if="Object.keys(errors).length > 1" class="text-red-500">
            Plusieurs erreurs sont présentes dans le formulaire.
            Merci de les corriger avant de soumettre à nouveau le formulaire
          </span>
        </div>
        </vv-form>
        <Toast :position="toastPosition">
          <template #message="slotProps">
            <span :class="iconClass"></span>
            <div class="p-toast-message-text">
              <span class="p-toast-summary">{{ slotProps.message.summary }}</span>
              <div class="p-toast-detail" v-html="slotProps.message.detail" />
              <div> <small>N'hésitez pas à prendre contact avec le parc si l'erreur persiste. Veuillez nous excuser pour la gêne
                  occasionnée.</small></div>
            </div>
          </template>
        </Toast>
</template>

<script setup lang="ts">
import { Form as VvForm, Field as VvField, ErrorMessage as VvErrorMessage } from 'vee-validate'
import * as yup from 'yup'
import { watch } from 'vue';
import { useToast } from "primevue/usetoast";
import Toast from "primevue/toast";
const toast = useToast();


const emits = defineEmits(['submit', 'cancel'])
const props = defineProps({
  saving: {
    type: Boolean,
    required: true
  },
  saveError: {
    type: String,
    required: false,
    default: ''
  },
  displayCancel: {
    type: Boolean,
    required: false,
    default: false
  },
  originalValues: {
    type: Object,
    required: false,
    default: () => ({})
  },
  displayAdminFields: {
    type: Boolean,
    required: false,
    default: false
  }
})
const origins = CONFIGURATION.ORIGINS




watch(
  () => props.saveError, (prev, next) => {
    console.log(props.saveError)
    if (props.saveError.name == "Error") {
      toast.add({ severity: 'error', summary: 'Sauvegarde impossible', detail: props.saveError.message, life: 10000 });
    }

  },
  { deep: true });


const formSchema = yup.object().shape({
  email: yup.string().email().required().label('Email'),
  tel: yup.string().required().label('Téléphone'),
  nom: yup.string().required().label('Nom'),
  prenom: yup.string().required().label('Prénom'),
  num_departement: yup.string().required().oneOf(CONFIGURATION.ORIGINS.map(x => String(x.value))).label('Lieu d\'origine'),
  commentaire: yup.string().nullable().label('Commentaire'),
  nb_adultes: yup.number().min(0).default(0).label('Adulte(s)'),
  nb_moins_6_ans: yup.number().min(0).default(0).label('Moins de 6 ans'),
  nb_6_8_ans: yup.number().min(0).default(0).label('6 - 8 ans'),
  nb_9_12_ans: yup.number().min(0).default(0).label('9 - 12 ans'),
  nb_plus_12_ans: yup.number().min(0).default(0).label('Plus de 12 ans'),
  liste_attente: yup.bool().label('En liste d\'attente'),
  confirmed: yup.bool().label('Confirmée par le créateur'),
  nb_total: yup
    .number()
    .test("nb_total_notnull", "Au moins un participant doit être inscrit", function (code) {
      const { nb_adultes, nb_moins_6_ans, nb_6_8_ans, nb_9_12_ans, nb_plus_12_ans } = this.parent;
      return nb_adultes + nb_moins_6_ans + nb_6_8_ans + nb_9_12_ans + nb_plus_12_ans >= 1;
    })
})


const formValues = {
  email: props.originalValues.email,
  tel: props.originalValues.tel,
  nom: props.originalValues.nom,
  prenom: props.originalValues.prenom,
  num_departement: props.originalValues.num_departement,
  commentaire: props.originalValues.commentaire,
  nb_adultes: props.originalValues.nb_adultes || 0,
  nb_moins_6_ans: props.originalValues.nb_moins_6_ans || 0,
  nb_6_8_ans: props.originalValues.nb_6_8_ans || 0,
  nb_9_12_ans: props.originalValues.nb_9_12_ans || 0,
  nb_plus_12_ans: props.originalValues.nb_plus_12_ans || 0,
  liste_attente: props.originalValues.liste_attente,
  confirmed: props.originalValues.confirmed,
}

</script>

<style scoped>
span[role='alert'] {
  color: var(--red-500);
}
</style>