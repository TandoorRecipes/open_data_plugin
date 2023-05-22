<template>
    <div>
        <b-modal id="open_data_food_edit_modal" size="xl" @hidden="cancelAction">

            <template v-slot:modal-title>
                <div class="row" v-if="food">
                    <div class="col-12">
                        <h2>{{ food.name }} <small class="text-muted" v-if="food.plural_name">{{
                                food.plural_name
                            }}</small>
                        </h2>
                    </div>
                </div>
            </template>

            <div class="row">
                <div class="col-12">
                    <b-form v-if="food">
                        <b-form-group :label="$t('FDC ID')" description="">
                            <b-input-group>
                                <b-form-input v-model="food.fdc_id"></b-form-input>

                                <b-input-group-append>
                                    <b-button variant="primary" @click="loadFDCData">LOAD FDC</b-button>
                                </b-input-group-append>
                            </b-input-group>
                        </b-form-group>

                        <b-form-group :label="$t('Slug')" description="">
                            <b-form-input v-model="food.slug"></b-form-input>
                        </b-form-group>
                        <b-form-group :label="$t('Name')" description="">
                            <b-form-input v-model="food.name"></b-form-input>
                        </b-form-group>
                        <b-form-group :label="$t('Plural')" description="">
                            <b-form-input v-model="food.plural_name"></b-form-input>
                        </b-form-group>

                        <b-form-group :label="$t('Store Category')" description="">
                            <generic-multiselect
                                @change="food.store_category = $event.val"
                                :initial_single_selection="food.store_category"
                                label="name" :model="OpenDataModels.OPEN_DATA_CATEGORY"
                                :multiple="false"/>
                        </b-form-group>

                        <b-form-group :label="$t('preferred_unit_metric')" description="">
                            <generic-multiselect
                                @change="food.preferred_unit_metric = $event.val"
                                :initial_single_selection="food.preferred_unit_metric"
                                label="name" :model="OpenDataModels.OPEN_DATA_UNIT"
                                :multiple="false"/>
                        </b-form-group>

                        <b-form-group :label="$t('preferred_shopping_unit_metric')" description="">
                            <generic-multiselect
                                @change="food.preferred_shopping_unit_metric = $event.val"
                                :initial_single_selection="food.preferred_shopping_unit_metric"
                                label="name" :model="OpenDataModels.OPEN_DATA_UNIT"
                                :multiple="false"/>
                        </b-form-group>
                        <b-form-group :label="$t('preferred_unit_imperial')" description="">
                            <generic-multiselect
                                @change="food.preferred_unit_imperial = $event.val"
                                :initial_single_selection="food.preferred_unit_imperial"
                                label="name" :model="OpenDataModels.OPEN_DATA_UNIT"
                                :multiple="false"/>
                        </b-form-group>
                        <b-form-group :label="$t('preferred_shopping_unit_imperial')" description="">
                            <generic-multiselect
                                @change="food.preferred_shopping_unit_imperial = $event.val"
                                :initial_single_selection="food.preferred_shopping_unit_imperial"
                                label="name" :model="OpenDataModels.OPEN_DATA_UNIT"
                                :multiple="false"/>
                        </b-form-group>

                        <b-form-group :label="$t('Properties Food Amount')" description="">
                            <b-form-input rows="3" v-model="food.properties_food_amount"></b-form-input>
                        </b-form-group>

                        <b-form-group :label="$t('Properties Food Unit')" description="">
                            <generic-multiselect
                                @change="food.properties_food_unit = $event.val"
                                :initial_single_selection="food.properties_food_unit"
                                label="name" :model="OpenDataModels.OPEN_DATA_UNIT"
                                :multiple="false"/>
                        </b-form-group>

                        <b-form-group :label="$t('Properties')" description="">
                            <table class="table">
                                <tr v-for="p in food.properties" v-bind:key="p.property">
                                    <td>
                                        <generic-multiselect
                                            @change="p.property = $event.val"
                                            :initial_single_selection="p.property"
                                            label="name" :model="OpenDataModels.OPEN_DATA_PROPERTY"
                                            :multiple="false"/>
                                    </td>
                                    <td>
                                        <b-form-input v-model="p.property_amount"></b-form-input>
                                    </td>
                                </tr>
                            </table>

                            <b-button @click="addProperty()">Add</b-button>
                        </b-form-group>

                        <b-form-group :label="$t('Properties Source')" description="">
                            <b-form-textarea rows="3" v-model="food.properties_source"></b-form-textarea>
                        </b-form-group>

                        <b-form-group :label="$t('Comment')" description="">
                            <b-form-textarea rows="3" v-model="food.comment"></b-form-textarea>
                        </b-form-group>


                    </b-form>

                </div>
            </div>
            <template v-slot:modal-footer>
                <b-button variant="primary" @click="updateData">{{ $t('Save') }}</b-button>
                <b-button variant="danger" @click="deleteData" v-if="food.id !== undefined">{{
                        $t('Delete')
                    }}
                </b-button>
            </template>
        </b-modal>
    </div>
</template>

<script>

import {ApiMixin, StandardToasts} from "@/utils/utils";
import {ApiApiFactory} from "../utils/openapi/api";
import GenericMultiselect from "../../../../../../vue/src/components/GenericMultiselect.vue";
import {ModelMixin} from "../utils/models";


export default {
    name: "OpenDataFoodEditComponent",
    components: {GenericMultiselect},
    mixins: [ApiMixin, ModelMixin],
    props: {
        object: {type: Object, default: undefined},
        show: {required: true, type: Boolean, default: false},
    },
    data() {
        return {
            food: undefined
        }
    },
    mounted() {
        this.loadData();
    },
    computed: {},
    watch: {
        show: function () {
            if (this.show) {
                this.loadData()
                this.$bvModal.show('open_data_food_edit_modal')
            } else {
                this.$bvModal.hide('open_data_food_edit_modal')
            }
        },
    },
    methods: {
        loadData: function () {
            if (this.object !== undefined) {
                console.log('loading food')
                let apiClient = new ApiApiFactory()
                apiClient.retrieveOpenDataFood(this.object.id).then(r => {
                    this.food = r.data
                })
            } else {
                this.food = {
                    slug: '',
                    name: '',
                    plural_name: '',
                    store_category: null,
                    preferred_unit_metric: null,
                    preferred_shopping_unit_metric: null,
                    preferred_unit_imperial: null,
                    preferred_shopping_unit_imperial: null,
                    properties: [],
                    fdc_id: '',
                    comment: '',
                }
            }
        },
        updateData: function () {
            let apiClient = new ApiApiFactory()
            if (this.object !== undefined) {
                apiClient.updateOpenDataFood(this.food.id, this.food).then(r => {
                    this.cancelAction()
                    StandardToasts.makeStandardToast(this, StandardToasts.SUCCESS_UPDATE)
                }).catch((err) => {
                    StandardToasts.makeStandardToast(this, StandardToasts.FAIL_CREATE, err)
                })
            } else {
                apiClient.createOpenDataFood(this.food).then(r => {
                    this.cancelAction()
                    StandardToasts.makeStandardToast(this, StandardToasts.SUCCESS_CREATE)
                }).catch((err) => {
                    StandardToasts.makeStandardToast(this, StandardToasts.FAIL_CREATE, err)
                })
            }
        },
        deleteData: function () {
            let apiClient = new ApiApiFactory()
            apiClient.destroyOpenDataFood(this.food.id).then(r => {
                this.cancelAction()
                StandardToasts.makeStandardToast(this, StandardToasts.SUCCESS_DELETE)
            }).catch((err) => {
                StandardToasts.makeStandardToast(this, StandardToasts.FAIL_DELETE, err)
            })
        },
        addProperty: function () {
            this.food.properties.push({property: null, property_amount: 0})
        },
        loadFDCData: function () {
            let apiClient = new ApiApiFactory()
            apiClient.retrieveFDCViewSet(this.food.fdc_id).then(r => {
                console.log(r.data)
                this.food = r.data
                StandardToasts.makeStandardToast(this, StandardToasts.SUCCESS_FETCH)
            }).catch((err) => {
                StandardToasts.makeStandardToast(this, StandardToasts.FAIL_FETCH, err)
            })
        },
        cancelAction: function () {
            this.$emit("hidden", "")
        },
    },
}
</script>
