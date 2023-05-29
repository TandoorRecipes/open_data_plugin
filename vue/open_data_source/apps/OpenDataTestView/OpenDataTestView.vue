<template>

    <div id="app">

        <ul class="nav nav-tabs mb-3">
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_HOME.name}" @click="selected_model = OpenDataModels.OPEN_DATA_HOME">Info</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_FOOD.name}" @click="selected_model = OpenDataModels.OPEN_DATA_FOOD">Food</a></li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_CONVERSION.name}" @click="selected_model = OpenDataModels.OPEN_DATA_CONVERSION">Conversion</a></li>
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

            <b-alert variant="success" show><b>BETA</b> This project is currently in beta, more descriptions and the integration with the GitHub repo will follow soon!</b-alert>

            <h5>Quickstart</h5>
            <ul>
                <li>Create and Edit data as you are used to with tandoor</li>
                <li>You can only edit foods, stores and conversions you created yourself, ask on discord to get <b>verified</b> so you can edit everything</li>
                <li>If unsure about something ask others for their opinion on discord</li>
                <li>Use the <code>comment</code> field in each object to add notes for other people reading or contributing</li>
            </ul>
            <h5>Versions</h5>
            <ul>
                <li>Each object has a version</li>
                <li>The <code>base</code> version contains data valid around the world and is always in english</li>
                <li>All objects of specific versions are in their respective language</li>
            </ul>
            <h5>Translations</h5>
            Translations are not yet available to be edited. Please focus on adding a good food and conversion base for now.
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
    computed: {},
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
