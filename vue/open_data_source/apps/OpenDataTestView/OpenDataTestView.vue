<template>

    <div id="app">

        <ul class="nav nav-tabs mb-3">
           <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_HOME.name}" @click="selected_model = OpenDataModels.OPEN_DATA_HOME">Info</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_FOOD.name}" @click="selected_model = OpenDataModels.OPEN_DATA_FOOD">Food</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_UNIT.name}" @click="selected_model = OpenDataModels.OPEN_DATA_UNIT">Unit</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_CATEGORY.name}" @click="selected_model = OpenDataModels.OPEN_DATA_CATEGORY">Category</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_STORE.name}" @click="selected_model = OpenDataModels.OPEN_DATA_STORE">Store</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_PROPERTY.name}" @click="selected_model = OpenDataModels.OPEN_DATA_PROPERTY">Property</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_VERSION.name}" @click="selected_model = OpenDataModels.OPEN_DATA_VERSION">Version</a></li>
        </ul>

        <div v-if="selected_model === OpenDataModels.OPEN_DATA_HOME">
            <h3>Tandoor Open Data</h3>
            The Tandoor Open Data project aims to get you started with tandoor faster and easier by providing a vast dataset
            of community contributed objects ranging from foods to units, stores and conversions.<br/>

            Find out more on <a href="https://github.com/TandoorRecipes/open-tandoor-data">GitHub</a><br/>
            Join our <a href="https://discord.gg/RhzBrfWgtp">Discord</a><br/>
            Or get right started creating some data for everyone to use.<br/><br/><br/>

            <h5>Quickstart</h5>
            <ul>
                <li>Create and Edit data as you are used to with tandoor</li>
                <li>You can only edit data you created yourself, ask on discord to get verified so you can edit everything</li>
                <li>Each object has a <i>version</i> attribute, use base for everything universal and the specific versions for certain countries or regions. When using anything other than base make sure to use the version specific language</li>
            </ul>
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
            selected_model: OpenDataModels.OPEN_DATA_HOME,
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
