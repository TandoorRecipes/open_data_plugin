<template>

    <div id="app">

        <ul class="nav nav-tabs mb-3">
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_HOME.name}" @click="selected_model = OpenDataModels.OPEN_DATA_HOME">Info</a>
            </li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_FOOD.name}" @click="selected_model = OpenDataModels.OPEN_DATA_FOOD">Food <span class="badge badge-pill badge-primary" v-if="stats !== null">{{stats.object_counts.food}}</span></a>
            </li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_CONVERSION.name}" @click="selected_model = OpenDataModels.OPEN_DATA_CONVERSION">Conversion <span class="badge badge-pill badge-primary" v-if="stats !== null">{{stats.object_counts.conversion}}</span></a>
            </li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_UNIT.name}" @click="selected_model = OpenDataModels.OPEN_DATA_UNIT">Unit <span class="badge badge-pill badge-primary" v-if="stats !== null">{{stats.object_counts.unit}}</span></a>
            </li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_CATEGORY.name}" @click="selected_model = OpenDataModels.OPEN_DATA_CATEGORY">Category <span class="badge badge-pill badge-primary" v-if="stats !== null">{{stats.object_counts.category}}</span></a>
            </li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_STORE.name}" @click="selected_model = OpenDataModels.OPEN_DATA_STORE">Store <span class="badge badge-pill badge-primary" v-if="stats !== null">{{stats.object_counts.store}}</span></a>
            </li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_PROPERTY.name}" @click="selected_model = OpenDataModels.OPEN_DATA_PROPERTY">Property <span class="badge badge-pill badge-primary" v-if="stats !== null">{{stats.object_counts.property}}</span></a>
            </li>
            <li class="nav-item"><a class="nav-link" :class="{'active':selected_model.name === OpenDataModels.OPEN_DATA_VERSION.name}" @click="selected_model = OpenDataModels.OPEN_DATA_VERSION">Version <span class="badge badge-pill badge-primary" v-if="stats !== null">{{stats.object_counts.version}}</span></a>
            </li>
        </ul>



        <div v-if="selected_model === OpenDataModels.OPEN_DATA_HOME">
            <h3>Tandoor Open Data</h3>
            The Tandoor Open Data project aims to get you started with tandoor faster and easier by providing a vast dataset
            of community contributed objects ranging from foods to units, stores and conversions.<br/>

            Find out more on <a href="https://github.com/TandoorRecipes/open-tandoor-data">GitHub</a><br/>
            Join our <a href="https://discord.gg/RhzBrfWgtp">Discord</a><br/>
            Or get right started creating some data for everyone to use.

            <h5 class="mt-4">Leaderboards</h5>

            <div class="row" v-if="stats !== null">
                <div class="col">

                    <div class="card-deck">
                        <div class="card" style="width: 18rem;">
                            <div class="card-header">
                                Foods - All Time
                            </div>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item" v-for="o in stats.food_stats_total" v-bind:key="`food_stats_total_${o.username}`">{{ o.username }} <span
                                    class="text-right float-right"><span class="badge badge-pill badge-primary">{{ o.count }}</span></span></li>
                            </ul>
                        </div>

                        <div class="card" style="width: 18rem;">
                            <div class="card-header">
                                Foods - last 30 days
                            </div>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item" v-for="o in stats.food_stats_last_30" v-bind:key="`food_stats_last_30_${o.username}`">{{ o.username }} <span
                                    class="text-right float-right"><span class="badge badge-pill badge-primary">{{ o.count }}</span></span></li>
                            </ul>
                        </div>


                        <div class="card" style="width: 18rem;">
                            <div class="card-header">
                                Conversions - All Time
                            </div>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item" v-for="o in stats.conversion_stats_total" v-bind:key="`conversion_stats_total_${o.username}`">{{ o.username }} <span
                                    class="text-right float-right"><span class="badge badge-pill badge-primary">{{ o.count }}</span></span></li>
                            </ul>
                        </div>

                        <div class="card" style="width: 18rem;">
                            <div class="card-header">
                                Conversions - last 30 days
                            </div>
                            <ul class="list-group list-group-flush">
                                <li class="list-group-item" v-for="o in stats.conversion_stats_last_30" v-bind:key="`conversion_stats_last_30_${o.username}`">{{ o.username }} <span
                                    class="text-right float-right"><span class="badge badge-pill badge-primary">{{ o.count }}</span></span></li>
                            </ul>
                        </div>
                    </div>
                </div>

            </div>

            <h5 class="mt-4">Quickstart</h5>
            <ul>
                <li>Create and Edit data as you are used to with tandoor</li>
                <li>Many foods can be found in the <a href="https://fdc.nal.usda.gov/index.html" target="_blank" rel="noreferrer nofollow">FDC Database</a>. Copy the FDC ID to quickly import it in the
                    food editor. If appropriate for the food create a conversion (some foods will come with a measurement comment).
                </li>
                <li>You can only edit foods, stores and conversions you created yourself, ask on discord to get <b>verified</b> so you can edit everything.</li>
                <li>If unsure about something ask others for their opinion on discord. Also take a look at this <a
                    href="https://github.com/TandoorRecipes/open-tandoor-data/wiki/Data-Considerations-and-Standards" target="_blank"> collection of examples</a>.</li>
                <li>Use the <code>comment</code> field in each object to add notes for other people reading or contributing.</li>
            </ul>
            <h5>Versions</h5>
            <ul>
                <li>Each object has a version</li>
                <li>The <code>base</code> version contains data valid around the world and is always in english</li>
                <li>All objects of specific versions are in their respective language</li>
            </ul>
            <h5>Translations</h5>
            Data for a select language is only available for translated entries.
            To help translate head over to the Tandoor Translation Page <a href="https://translate.tandoor.dev/projects/tandoor-open-data/" target="_blank">here</a>.
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
            stats: null,
        }
    },
    mounted() {
        this.$i18n.locale = window.CUSTOM_LOCALE

        let apiClient = new ApiApiFactory()
        apiClient.listOpenDataStatisticsViewSets().then(r => {
            this.stats = r.data
        })
    },
    methods: {},
}
</script>

<style>

</style>
