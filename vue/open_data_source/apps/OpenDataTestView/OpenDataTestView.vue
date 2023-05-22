<template>

    <div id="app">

        <ul class="nav nav-tabs mb-3">
<!--            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === undefined}" @click="selected_model = undefined">Info</a></li>-->
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_FOOD.name}" @click="selected_model = OpenDataModels.OPEN_DATA_FOOD">Food</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_UNIT.name}" @click="selected_model = OpenDataModels.OPEN_DATA_UNIT">Unit</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_CATEGORY.name}" @click="selected_model = OpenDataModels.OPEN_DATA_CATEGORY">Category</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_STORE.name}" @click="selected_model = OpenDataModels.OPEN_DATA_STORE">Store</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_PROPERTY.name}" @click="selected_model = OpenDataModels.OPEN_DATA_PROPERTY">Property</a></li>
        </ul>

        <div v-if="selected_model === undefined">

        </div>
        <div v-else>
             <open-data-list-component :model="selected_model"></open-data-list-component>
        </div>

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

    },
    mixins: [ModelMixin],
    components: {OpenDataListComponent},
    data() {
        return {
            selected_model: OpenDataModels.OPEN_DATA_FOOD,
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
