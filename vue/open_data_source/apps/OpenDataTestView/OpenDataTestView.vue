<template>

    <div id="app">
        Test TExt

        {{ $t('Test')}}

        <button @click="show_create_modal = !show_create_modal">Toggle</button>

        <generic-modal-form :model="OPEN_DATA_UNIT" :action="Actions.CREATE" :show="show_create_modal"/>


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
Vue.use(VueI18n)

export default {
    name: "OpenDataTestView",
    computed: {
        Actions() {
            return Actions
        }
    },
    mixins: [],
    components: {GenericModalForm},
    data() {
        return {
            food: undefined,
            open_data_units: [],
            OPEN_DATA_UNIT: {
                name: "OpenDataUnit",
                apiName: "OpenDataUnit",
                apiClient:  new ApiApiFactory(),
                paginated: true,
                create: {
                    params: [["name", "plural_name", "comment", "slug",]],
                    form: {
                        show_help: true,
                        name: {
                            form_field: true,
                            type: "text",
                            field: "name",
                            label: "Name",
                            placeholder: "",
                        },
                        plural_name: {
                            form_field: true,
                            type: "text",
                            field: "plural_name",
                            label: "Plural name",
                            placeholder: "",
                        },
                        comment: {
                            form_field: true,
                            type: "text",
                            field: "comment",
                            label: "comment",
                            placeholder: "",
                        },
                        slug: {
                            form_field: true,
                            type: "text",
                            field: "slug",
                            label: "Slug",
                        },
                    },
                },
                merge: true,
            },
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
