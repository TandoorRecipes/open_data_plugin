<template>

    <div id="app">
        Test TExt



    </div>
</template>


<script>
import Vue from "vue"
import {BootstrapVue} from "bootstrap-vue"

import "bootstrap-vue/dist/bootstrap-vue.css"
import {ApiApiFactory} from "../../utils/openapi";

Vue.use(BootstrapVue)


export default {
    name: "OpenDataTestView",
    mixins: [],
    components: {

    },
    data() {
        return {
            food: undefined,

        }
    },
    mounted() {
        let apiFactory = new ApiApiFactory()
        apiFactory.listOpenDataUnits()

    },
    methods: {

    },
}
</script>

<style>

</style>
