<template>

    <div id="app">

        <ul class="nav nav-tabs mb-3">
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model === OpenDataModels.OPEN_DATA_FOOD}" @click="selected_model = OpenDataModels.OPEN_DATA_FOOD">Food</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model === OpenDataModels.OPEN_DATA_UNIT}" @click="selected_model = OpenDataModels.OPEN_DATA_UNIT">Unit</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model === OpenDataModels.OPEN_DATA_CATEGORY}" @click="selected_model = OpenDataModels.OPEN_DATA_CATEGORY">Category</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model === OpenDataModels.OPEN_DATA_STORE}" @click="selected_model = OpenDataModels.OPEN_DATA_STORE">Store</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model === OpenDataModels.OPEN_DATA_PROPERTY}" @click="selected_model = OpenDataModels.OPEN_DATA_PROPERTY">Property</a></li>
        </ul>

        <button @click="show_create_modal = !show_create_modal">Toggle</button>

        <template v-if="selected_model.name === OpenDataModels.OPEN_DATA_FOOD.name">
            <open-data-food-edit-component :show="show_create_modal" :object="selected_object" @hidden="refresh += 1; show_create_modal = false"></open-data-food-edit-component>
        </template>
        <template v-else>
            <generic-modal-form :model="selected_model" :models="OpenDataModels" :action="Actions.CREATE" :show="show_create_modal" @finish-action="refresh += 1; show_create_modal = false"/>
        </template>


        <h1>List</h1>
        <open-data-list-component :model="selected_model" :refresh="refresh"></open-data-list-component>
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
import OpenDataFoodEditComponent from "../../components/OpenDataFoodEditComponent.vue";

Vue.use(VueI18n)

export default {
    name: "OpenDataTestView",
    computed: {
        Actions() {
            return Actions
        },
    },
    mixins: [ModelMixin],
    components: {GenericModalForm, OpenDataListComponent, OpenDataFoodEditComponent},
    data() {
        return {
            selected_model: OpenDataModels.OPEN_DATA_UNIT,
            selected_object: undefined,
            show_create_modal: false,
            refresh: 0,
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
