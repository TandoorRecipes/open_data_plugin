<template>
    <div>
        <b-btn @click="show_modal = true; modal_action=Actions.CREATE" class="mb-2">New</b-btn>

        <template v-if="model.name === OpenDataModels.OPEN_DATA_FOOD.name">
            <open-data-food-edit-component :show="show_modal" :object="selected_object"
                                           @hidden="finishAction"></open-data-food-edit-component>
        </template>
        <template v-else>
            <generic-modal-form :model="model" :models="OpenDataModels" :action="modal_action" :show="show_modal"
                                :item1="selected_object"
                                @finish-action="finishAction"/>
        </template>


        <table class="table table-bordered table-striped">
            <thead>
            <tr>
                <th v-for="f in model.table_fields" v-bind:key="f">{{ f }}</th>
                <th>Actions</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="o in objects" v-bind:key="o.id">
                <td v-for="f in model.table_fields" v-bind:key="`${o.id}_${f}`">{{ o[f] }}</td>
                <td>
                    <b-button-group>
                        <b-button variant="success"
                                  @click=" modal_action=Actions.UPDATE; selected_object=o; show_modal = true;"><i
                            class="fas fa-edit"></i></b-button>
                        <b-button variant="info"
                                  @click="copyObject(o)"><i class="fas fa-copy"></i></b-button>
                        <b-button variant="danger"
                                  @click=" modal_action=Actions.DELETE; selected_object=o; show_modal = true;"><i
                            class="fas fa-trash"></i></b-button>
                    </b-button-group>
                </td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>


import {StandardToasts} from "../../../../../../vue/src/utils/utils";
import {ApiMixin} from "@/utils/utils";
import OpenDataFoodEditComponent from "./OpenDataFoodEditComponent.vue";
import GenericModalForm from "../../../../../../vue/src/components/Modals/GenericModalForm.vue";
import {ModelMixin} from "../utils/models";
import {Actions} from "../../../../../../vue/src/utils/models";

export default {
    name: "OpenDataListComponent",
    components: {GenericModalForm, OpenDataFoodEditComponent},
    mixins: [ApiMixin, ModelMixin],
    props: {
        model: {type: Object},
        refresh: {type: Number},
    },
    data() {
        return {
            objects: [],
            selected_object: undefined,
            show_modal: false,
            modal_action: Actions.CREATE,
        }
    },
    mounted() {
        this.loadData();
    },
    computed: {},
    watch: {
        model: function () {
            this.loadData()
        },
    },
    methods: {
        loadData: function () {
            this.genericAPI(this.model, this.Actions.LIST).then((result) => {
                this.objects = result.data
            }).catch((err) => {
                StandardToasts.makeStandardToast(this, StandardToasts.FAIL_CREATE, err)
            })
        },
        copyObject: function (o) {
            let o_copy = JSON.parse(JSON.stringify(o));
            delete o_copy.id
            o_copy.slug += '-copy'
            o_copy.name += '-copy'
            o_copy.plural_name += '-copy'
            this.genericAPI(this.model, this.Actions.CREATE, o_copy).then((result) => {
                this.loadData()
            }).catch((err) => {
                StandardToasts.makeStandardToast(this, StandardToasts.FAIL_CREATE, err)
            })
        },
        finishAction: function (e) {
            if (e !== "cancel") {
                this.loadData();
                this.show_modal = false
                this.selected_object = undefined
            }
        }
    },
}
</script>
