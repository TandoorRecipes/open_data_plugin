<template>

    <div id="app">


        <ul class="nav nav-tabs mb-3">

            <li class="nav-item"><a
                class="nav-link"
                @click="selected_model = OpenDataModels.OPEN_DATA_FOOD">Food</a></li>
            <li class="nav-item"><a
                class="nav-link"
                @click="selected_model = OpenDataModels.OPEN_DATA_UNIT">Unit</a></li>
        </ul>

        <button @click="show_create_modal = !show_create_modal">Toggle</button>

        <generic-modal-form :model="selected_model" :models="OpenDataModels" :action="Actions.CREATE" :show="show_create_modal"/>


        <h1>List</h1>
        <open-data-list-component :model="selected_model"></open-data-list-component>
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
import {ModelMixin, OpenDataModels} from "../../utils/models";
import OpenDataListComponent from "../../components/OpenDataListComponent.vue";

Vue.use(VueI18n)

export default {
    name: "OpenDataTestView",
    computed: {
        Actions() {
            return Actions
        },
    },
    mixins: [ModelMixin],
    components: {GenericModalForm, OpenDataListComponent},
    data() {
        return {
            selected_model: OpenDataModels.OPEN_DATA_UNIT,
            show_create_modal: false,
        }
    },
    mounted() {
        this.$i18n.locale = window.CUSTOM_LOCALE
    },
    methods: {},
}
</script>

<style>

</style>
