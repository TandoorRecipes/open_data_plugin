<template>

    <div id="app">
        Test TExt

        {{ $t('Test')}}

        <button @click="show_create_modal = !show_create_modal">Toggle</button>

        <generic-modal-form :model="OpenDataModels.OPEN_DATA_UNIT" :models="OpenDataModels" :action="Actions.CREATE" :show="show_create_modal"/>


        <h1>List</h1>
        <ul>
            <li v-for="x in open_data_units" v-bind:key="x.id">{{x}}</li>
        </ul>
    </div>
</template>


<script>
import Vue from "vue"
import {BootstrapVue} from "bootstrap-vue"

import "bootstrap-vue/dist/bootstrap-vue.css"
import {ApiApiFactory} from "../../utils/openapi/api";
import GenericModalForm from "../../../../../../../vue/src/components/Modals/GenericModalForm.vue";
import {Actions} from "@/utils/models";

Vue.use(BootstrapVue)
import VueI18n from 'vue-i18n'
import {ModelMixin} from "../../utils/models";
Vue.use(VueI18n)

export default {
    name: "OpenDataTestView",
    computed: {
        Actions() {
            return Actions
        }
    },
    mixins: [ModelMixin],
    components: {GenericModalForm},
    data() {
        return {
            food: undefined,
            open_data_units: [],

            show_create_modal: false,
        }
    },
    mounted() {
        this.$i18n.locale = window.CUSTOM_LOCALE

        let apiClient = new ApiApiFactory()
        console.log(apiClient)
        apiClient.listOpenDataUnits().then(r => {
            this.open_data_units = r.data
        })

    },
    methods: {

    },
}
</script>

<style>

</style>
