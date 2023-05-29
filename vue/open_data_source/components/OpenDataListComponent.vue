<template>
    <div>
        <b-btn @click="show_modal = false;  modal_action=Actions.CREATE; show_modal = true;" class="mb-2">New</b-btn>

        <template v-if="model.name === OpenDataModels.OPEN_DATA_FOOD.name">
            <open-data-food-edit-component :show="show_modal" :object="selected_object"
                                           @hidden="finishAction"></open-data-food-edit-component>
        </template>
        <template v-else-if="model.name === OpenDataModels.OPEN_DATA_STORE.name">
            <open-data-store-edit-component :show="show_modal" :object="selected_object"
                                            @hidden="finishAction"></open-data-store-edit-component>
        </template>
        <template v-else>
            <generic-modal-form :model="model" :models="OpenDataModels" :action="modal_action" :show="show_modal"
                                :item1="selected_object"
                                @hidden="finishAction" @finish-action="finishAction"/>
        </template>

        <b-form-group label="Search Name">
            <b-input v-model="search_name"></b-input>
        </b-form-group>
        <b-form-group label="Search Slug">
            <b-input v-model="search_slug"></b-input>
        </b-form-group>


        <table class="table table-bordered table-striped">
            <thead>
            <tr>
                <th v-for="f in model.table_fields" v-bind:key="f">{{ f }}</th>
                <th v-if="model.name !== OpenDataModels.OPEN_DATA_VERSION.name">Created By</th>
                <th v-if="model.name !== OpenDataModels.OPEN_DATA_VERSION.name">Version</th>
                <th>Actions</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="o in filtered_objects" v-bind:key="o.id">
                <td v-for="f in model.table_fields" v-bind:key="`${o.id}_${f}`">{{ resolve(f,o) }}</td>
                <td v-if="model.name !== OpenDataModels.OPEN_DATA_VERSION.name">{{ o.created_by }}</td>
                <td v-if="model.name !== OpenDataModels.OPEN_DATA_VERSION.name">
                    <b-badge>{{ o.version.code }}</b-badge>
                </td>
                <td>
                    <b-button-group>
                        <b-button variant="success"
                                  @click="show_modal = false;  modal_action=Actions.UPDATE; selected_object=o; show_modal = true;"><i
                            class="fas fa-edit"></i></b-button>
                        <b-button variant="info"
                                  @click="copyObject(o)"><i class="fas fa-copy"></i></b-button>
                        <b-button variant="danger"
                                  @click="show_modal = false;  modal_action=Actions.DELETE; selected_object=o; show_modal = true;"><i
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
import OpenDataStoreEditComponent from "./OpenDataStoreEditComponent.vue";

export default {
    name: "OpenDataListComponent",
    components: {GenericModalForm, OpenDataFoodEditComponent, OpenDataStoreEditComponent},
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
            search_name: '',
            search_slug: '',
        }
    },
    mounted() {
        this.loadData();
    },
    computed: {
        filtered_objects: function () {
            let data = this.objects
            if (data.length > 0 && data[0].name !== undefined) {
                data = data.filter(x => x.name.toLowerCase().includes(this.search_name.toLowerCase()))
            }
            if (data.length > 0 && data[0].slug !== undefined) {
                data = data.filter(x => x.slug.toLowerCase().includes(this.search_slug.toLowerCase()))
            }
            return data
        },
    },
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
                this.objects = []
                StandardToasts.makeStandardToast(this, StandardToasts.FAIL_FETCH, err, true)
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
                StandardToasts.makeStandardToast(this, StandardToasts.FAIL_CREATE, err, true)
            })
        },
        finishAction: function (e) {
            if (e !== "cancel") {
                this.loadData();
                this.show_modal = false
                this.selected_object = undefined
            }
        },
        resolve: function (path, obj, separator = '.') {
            let properties = Array.isArray(path) ? path : path.split(separator)
            return properties.reduce((prev, curr) => prev?.[curr], obj)
        }
    },
}
</script>
