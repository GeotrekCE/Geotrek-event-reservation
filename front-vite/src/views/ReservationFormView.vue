<template>

  <header class="bg-white shadow">
    <div class="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">
      <h1 class="text-3xl font-bold tracking-tight text-gray-900">
        Réservation d'un événement
        <template v-if="event">
          ({{ event.name }})
        </template>
      </h1>
    </div>
  </header>

  <main
    class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 px-4 py-6"
    v-if="status !== STATUS.SUCCESS"
  >

    <section class="border-b border-gray-900/10 pb-12">

      <p>
        Vous vous apprêtez à effectuer une réservation pour l'animation
        <span class="font-medium" v-if="event">{{ event.name }}</span>
        proposé par le Parc National de Guadeloupe.
      </p>

      <h2 class="text-base font-medium leading-7 text-gray-900 mt-10" @click="isSummaryDisplayed = !isSummaryDisplayed">
        Résumé de l'animation
      </h2>

      <div class="grid grid-cols-1 sm:grid-cols-6 gap-x-2 gap-y-4 mt-4" v-if="event && isSummaryDisplayed">
        <div class="col-span-full sm:col-span-3">
          <label for="username" class="block text-sm font-medium leading-6 text-gray-900">
            Événement
          </label>
          <div class="mt-2">
            <div
              class="flex rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-md"
            >
              <span
                class="block flex-1 border-0 bg-transparent p-2 text-gray-600 sm:text-sm sm:leading-6"
              >
                {{ event.name }}
              </span>
            </div>
          </div>
        </div>

        <div class="col-span-1 sm:col-span-3">
          <label for="username" class="block text-sm font-medium leading-6 text-gray-900">
            Type
          </label>
          <div class="mt-2">
            <div
              class="flex rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-md"
            >
              <span
                class="block flex-1 border-0 bg-transparent p-2 text-gray-600 sm:text-sm sm:leading-6"
              >
                {{ ( event.type && event.type.type ) || 'Non renseigné' }}
              </span>
            </div>
          </div>
        </div>

        <div class="col-span-1 sm:col-span-3">
          <label for="username" class="block text-sm font-medium leading-6 text-gray-900">
            Date de début
          </label>
          <div class="mt-2">
            <div
              class="flex rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-md"
            >
              <span
                class="block flex-1 border-0 bg-transparent p-2 text-gray-600 sm:text-sm sm:leading-6"
              >
                {{ formatDate(event.begin_date) || 'Non renseigné' }}
              </span>
            </div>
          </div>
        </div>
        <div class="col-span-1 sm:col-span-3">
          <label for="username" class="block text-sm font-medium leading-6 text-gray-900">
            Date de fin
          </label>
          <div class="mt-2">
            <div
              class="flex rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-md"
            >
              <span
                class="block flex-1 border-0 bg-transparent p-2 text-gray-600 sm:text-sm sm:leading-6"
              >
                {{ formatDate(event.end_date) || 'Non renseigné' }}
              </span>
            </div>
          </div>
        </div>
        <div class="col-span-1 sm:col-span-3">
          <label for="username" class="block text-sm font-medium leading-6 text-gray-900">
            Capacité
          </label>
          <div class="mt-2">
            <div
              class="flex rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-md"
            >
              <span
                class="block flex-1 border-0 bg-transparent p-2 text-gray-600 sm:text-sm sm:leading-6"
              >
                {{ event.capacity || 'Non renseigné' }}
              </span>
            </div>
          </div>
        </div>

        <div class="col-span-1 sm:col-span-3">
          <label for="username" class="block text-sm font-medium leading-6 text-gray-900">
            Massif
          </label>
          <div class="mt-2">
            <div
              class="flex rounded-sm shadow-sm ring-1 ring-inset ring-gray-300 sm:max-w-md"
            >
              <span
                class="block flex-1 border-0 bg-transparent p-2 text-gray-600 sm:text-sm sm:leading-6"
              >
                {{ event.massif || 'Non renseigné' }}
              </span>
            </div>
          </div>
        </div>

        <div class="col-span-full">
          <label for="about" class="block text-sm font-medium leading-6 text-gray-900">Informations pratiques (fr)</label>
          <div class="mt-2">
            <textarea id="about" name="about" rows="3" class="block w-full rounded-sm border-0 p-2 text-gray-600 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6" :value="event.practical_info_fr" disabled />
          </div>
        </div>

        <div class="col-span-full">
          <label for="about" class="block text-sm font-medium leading-6 text-gray-900">Informations pratiques (en)</label>
          <div class="mt-2">
            <textarea id="about" name="about" rows="3" class="block w-full rounded-sm border-0 p-2 text-gray-600 shadow-sm ring-1 ring-inset ring-gray-300 sm:text-sm sm:leading-6" :value="event.practical_info_en" disabled />
          </div>
        </div>
      </div>

    </section>

    <section>

      <form @submit.prevent="saveReservation" class="mt-10">
        <div class="space-y-12">
          <div>
            <h1 class="text-xl font-medium leading-7 text-gray-900">Inscription</h1>
            <p class="mt-1 text-sm leading-6 text-gray-600">
              En remplissant ce formulaire, puis en le validant,
              vous recevrez un email de confirmation.
              <br/>
              <strong>Veillez bien à confirmer votre inscription via le lien contenu dans cet email.</strong>
            </p>

          </div>

          <div class="border-b border-gray-900/10 pb-12">
            <h2 class="text-base font-medium leading-7 text-gray-900">Informations personnelles</h2>
            <p class="mt-1 text-sm leading-6 text-gray-600">Utilisez une adresse mail sur laquelle vous pouvez vous connecter.</p>

            <div class="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
              <div class="col-span-1 sm:col-span-3">
                <label for="first-name" class="block text-sm font-medium leading-6 text-gray-900">Prénom</label>
                <div class="mt-2">
                  <input
                    type="text"
                    name="first-name"
                    id="first-name"
                    autocomplete="given-name"
                    class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" v-model="reservation.prenom" />
                </div>
              </div>

              <div class="col-span-1 sm:col-span-3">
                <label for="last-name" class="block text-sm font-medium leading-6 text-gray-900">Nom</label>
                <div class="mt-2">
                  <input type="text" name="last-name" id="last-name" autocomplete="family-name" class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" v-model="reservation.nom" />
                </div>
              </div>

              <div class="col-span-1 sm:col-span-2">
                <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email</label>
                <div class="mt-2">
                  <input id="email" name="email" type="email" autocomplete="email" class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" v-model="reservation.email" />
                </div>
              </div>

              <div class="col-span-1 sm:col-span-2">
                <label for="tel" class="block text-sm font-medium leading-6 text-gray-900">Téléphone</label>
                <div class="mt-2">
                  <input type="text" name="tel" id="tel" autocomplete="tel" class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" v-model="reservation.tel" />
                </div>
              </div>

              <div class="col-span-1 sm:col-span-2">
                <label for="dept" class="block text-sm font-medium leading-6 text-gray-900">Département</label>
                <div class="mt-2">
                  <select
                    id="dept"
                    name="dept"
                    autocomplete="dept"
                    class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6"
                    v-model="reservation.num_departement" 
                  >
                    <option value="09">Ariège</option>
                    <option>Canada</option>
                    <option>Mexico</option>
                  </select>
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
                  <input
                    type="number"
                    name="nb_adultes"
                    id="nb_adultes"
                    min="0" 
                    class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    v-model="reservation.nb_adultes" 
                  />
                </div>
              </div>
              <div class="sm:col-span-2">
                <label for="nb_moins_6_ans" class="block text-sm font-medium leading-6 text-gray-900">Moins de 6 ans</label>
                <div class="mt-2">
                  <input
                    type="number"
                    name="nb_moins_6_ans"
                    id="nb_moins_6_ans"
                    min="0" 
                    class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    v-model="reservation.nb_moins_6_ans"
                  />
                </div>
              </div>
              <div class="sm:col-span-2">
                <label for="nb_6_8_ans" class="block text-sm font-medium leading-6 text-gray-900">6 - 8 ans</label>
                <div class="mt-2">
                  <input
                    type="number"
                    name="nb_6_8_ans"
                    id="nb_6_8_ans"
                    min="0" 
                    class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    v-model="reservation.nb_6_8_ans" 
                  />
                </div>
              </div>
              <div class="sm:col-span-2">
                <label for="nb_9_12_ans" class="block text-sm font-medium leading-6 text-gray-900">9 - 12 ans</label>
                <div class="mt-2">
                  <input
                    type="number"
                    name="nb_9_12_ans"
                    id="nb_9_12_ans"
                    min="0" 
                    class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    v-model="reservation.nb_9_12_ans"
                  />
                </div>
              </div>
              <div class="sm:col-span-2">
                <label for="nb_plus_12_ans" class="block text-sm font-medium leading-6 text-gray-900">Plus de 12 ans</label>
                <div class="mt-2">
                  <input
                    type="number"
                    name="nb_plus_12_ans"
                    id="nb_plus_12_ans"
                    min="0" 
                    class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    v-model="reservation.nb_plus_12_ans"
                  />
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
                <textarea id="commentaire" name="commentaire" rows="3" class="block w-full rounded-sm border-0 p-2 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" v-model="reservation.commentaire" />
              </div>
            </div>
          </div>
        </div>



        <div class="my-6 flex flex-col items-end gap-x-6">
          <button
            type="submit"
            class="rounded-sm px-3 py-2 text-sm font-medium text-white shadow-sm  focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-600"
            :class="{
              'bg-sky-600': !saving,
              'hover:bg-sky-500': !saving,
              'bg-sky-100': saving,
              'hover:bg-sky-100': saving,
              'text-black': saving,
            }"
            :disabled="saving"
          >
            {{ saving ? 'Enregistrement en cours...' : 'Enregistrer réservation' }}
          </button>
          <span v-if="saveError" class="text-red-500">
           Une erreur est survenue : {{ saveError }} 
          </span>
          <span v-if="saveError" class="text-red-500">
            N'hésitez pas à prendre contact avec le parc si l'erreur persiste.
            Veuillez nous excuser pour la gêne occasionnée.
          </span>
        </div>
      </form>

    </section>

  </main>

  <main
    class="mx-auto max-w-7xl py-6 sm:px-6 lg:px-8 px-4 py-6"
    v-else
  >
    <h2 class="text-xl font-medium leading-7 text-gray-900 mt-10 mb-4">
      Merci pour votre inscription !
    </h2>
    <p class="mb-4">
      Vous allez recevoir un email dans votre boîte de réception
      attestant votre demande de réservation.
    </p>
    <h2 class="text-xl font-medium">
      Mais ce n'est pas fini !
    </h2>
    <p>
      Vous devez <strong>confirmer</strong> cette demande 
      en cliquant sur le lien présent dans l'email.
    </p>
  </main>
</template>

<script setup lang="ts">
import { ref, onBeforeMount } from 'vue'
import { useRoute } from 'vue-router'
import {getOneEvent, postReservation } from '@/utils/appli_api';
import { formatDate } from '@/utils/formatDate'

const currentRoute = useRoute()
const geotrekId = currentRoute.params.geotrekid

const STATUS = {
  PRISTINE: 'PRISTINE',
  VALID: 'VALID',
  INVALID: 'INVALID',
  SAVING: 'SAVING',
  ERROR: 'ERROR',
  SUCCESS: 'SUCCESS'
}

/**
 * State local
 */
const isSummaryDisplayed = ref(true)
/*const reservation = ref({
  nom: '',
  prenom: '',
  tel: '',
  email: '',
  commentaire: '',
  nb_adultes: 0,
  nb_moins_6_ans: 0,
  nb_6_8_ans: 0,
  nb_9_12_ans: 0,
  nb_plus_12_ans: 0,
  num_departement: '',
  id_event: geotrekId,
})
*/
const reservation = ref({
  nom: '',
  prenom: '',
  tel: '',
  email: '',
  commentaire: '',
  nb_adultes: 0,
  nb_moins_6_ans: 0,
  nb_6_8_ans: 0,
  nb_9_12_ans: 0,
  nb_plus_12_ans: 0,
  num_departement: '09',
  id_event: geotrekId,
})
const status = ref(STATUS.PRISTINE)

/**
 * Chargement de l'événement corrélé
 */
const event = ref<any>(null)
onBeforeMount(async () => {
  event.value = await getOneEvent(geotrekId)
})


/**
 * Fonctions d'enregistrement de la réservation
 */
const saving = ref(false)
const saveError = ref<any>(null)
async function saveReservation() {
  status.value = STATUS.SAVING
  saving.value = true
  try {
    await postReservation(reservation.value)
    status.value = STATUS.SUCCESS
  } catch (error) {
    saveError.value = error
    status.value = STATUS.ERROR
  }
  saving.value = false
}

</script>