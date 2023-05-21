<template>
    <div>
        <table class="table table-bordered table-striped">
            <thead>
            <tr>
                <th v-for="f in model.table_fields" v-bind:key="f">{{ f }}</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="o in objects" v-bind:key="o.id">
                <td v-for="f in model.table_fields" v-bind:key="`${o.id}_${f}`">{{ o[f] }}</td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>


import {StandardToasts} from "../../../../../../vue/src/utils/utils";
import {ApiMixin} from "@/utils/utils";

export default {
    name: "OpenDataListComponent",
    components: {},
    mixins: [ApiMixin],
    props: {
        model: {type: Object},
    },
    data() {
        return {
            objects: []
        }
    },
    mounted() {
        this.loadData();
    },
    computed: {},
    watch: {
        model: function (){
            this.loadData()
        }
    },
    methods: {
        loadData: function () {
            this.genericAPI(this.model, this.Actions.LIST).then((result) => {
                this.objects = result.data
            }).catch((err) => {
                StandardToasts.makeStandardToast(this, StandardToasts.FAIL_CREATE, err)
            })
        }
    },
}
</script>
