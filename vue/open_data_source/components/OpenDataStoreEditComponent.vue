<template>
    <div>
        <b-modal id="open_data_store_edit_modal" size="xl" @hidden="cancelAction">

            <template v-slot:modal-title>
                <div class="row" v-if="store">
                    <div class="col-12">
                        <h2>{{ store.name }}
                        </h2>
                    </div>
                </div>
            </template>

            <div class="row">
                <div class="col-12">
                    <b-form v-if="store">
                        <b-form-group :label="$t('Version')" description="">
                            <generic-multiselect
                                @change="store.version = $event.val"
                                :initial_single_selection="store.version"
                                label="name" :model="OpenDataModels.OPEN_DATA_VERSION"
                                :multiple="false"/>
                        </b-form-group>

                        <b-form-group :label="$t('Slug')" description="">
                            <b-form-input v-model="store.slug"></b-form-input>
                        </b-form-group>
                        <b-form-group :label="$t('Name')" description="">
                            <b-form-input v-model="store.name"></b-form-input>
                        </b-form-group>

                        <b-form-group :label="$t('Add Category')" description="">
                            <generic-multiselect
                                @change="adding_category = $event.val; addCategory()"
                                label="name" :model="OpenDataModels.OPEN_DATA_CATEGORY"
                                :multiple="false"/>
                        </b-form-group>

                        <draggable :list="store.category_to_store" group="supermarket_categories"
                                   :empty-insert-threshold="10" @sort="sortCategories()">
                            <div v-for="c in store.category_to_store" :key="c.id">
                                <b-button-group>
                                    <b-button class="btn btn-block btn-sm btn-primary" style="margin-top: 0.5vh">
                                        <i class="fas fa-grip-vertical"></i> {{ c.category.name }}
                                    </b-button>
                                    <b-button variant="danger" @click="deleteCategory(c)"><i class="fas fa-trash"></i>
                                    </b-button>
                                </b-button-group>

                            </div>
                        </draggable>

                        <b-form-group :label="$t('Comment')" description="">
                            <b-form-textarea rows="3" v-model="store.comment"></b-form-textarea>
                        </b-form-group>


                    </b-form>

                </div>
            </div>
            <template v-slot:modal-footer>
                <b-button class="mx-1" variant="secondary" v-on:click="cancelAction">{{ $t("Cancel") }}</b-button>
                <b-button variant="primary" @click="updateData">{{ $t('Save') }}</b-button>
                <b-button variant="danger" @click="deleteData" v-if="store.id !== undefined">{{ $t('Delete') }}
                </b-button>
            </template>
        </b-modal>
    </div>
</template>

<script>

import {ApiMixin, StandardToasts} from "@/utils/utils";
import {ApiApiFactory} from "../utils/openapi/api";
import {ModelMixin} from "../utils/models";

import draggable from "vuedraggable"
import GenericMultiselect from "../../../../../../vue/src/components/GenericMultiselect.vue";

export default {
    name: "OpenDataStoreEditComponent",
    components: {GenericMultiselect, draggable},
    mixins: [ApiMixin, ModelMixin],
    props: {
        object: {type: Object, default: undefined},
        show: {required: true, type: Boolean, default: false},
    },
    data() {
        return {
            store: undefined,
            adding_category: undefined,
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
                this.$bvModal.show('open_data_store_edit_modal')
            } else {
                this.$bvModal.hide('open_data_store_edit_modal')
            }
        },
    },
    methods: {
        loadData: function () {
            if (this.object !== undefined) {
                let apiClient = new ApiApiFactory()
                apiClient.retrieveOpenDataStore(this.object.id).then(r => {
                    this.store = r.data
                })
            } else {
                this.store = {
                    version: {'id': 1, 'name': 'base', 'code': 'base'},
                    slug: '',
                    name: '',
                    category_to_store: [],
                    comment: '',
                }
            }
        },
        updateData: function () {
            let apiClient = new ApiApiFactory()
            if (this.object !== undefined) {
                apiClient.updateOpenDataStore(this.store.id, this.store).then(r => {
                    this.cancelAction()
                    StandardToasts.makeStandardToast(this, StandardToasts.SUCCESS_UPDATE)
                }).catch((err) => {
                    StandardToasts.makeStandardToast(this, StandardToasts.FAIL_CREATE, err, true)
                })
            } else {
                let properties = JSON.parse(JSON.stringify(this.store.category_to_store));
                this.store.category_to_store = []

                apiClient.createOpenDataStore(this.store).then(r => {
                    this.store = r.data
                    properties.forEach(p => p.store = r.data.id)
                    this.store.category_to_store = properties

                    apiClient.updateOpenDataStore(this.store.id, this.store).then(r => {
                        this.cancelAction()
                        StandardToasts.makeStandardToast(this, StandardToasts.SUCCESS_CREATE)
                    }).catch((err) => {
                        console.log(err)
                        StandardToasts.makeStandardToast(this, StandardToasts.FAIL_UPDATE, err, true)
                    })
                }).catch((err) => {
                    StandardToasts.makeStandardToast(this, StandardToasts.FAIL_CREATE, err, true)
                })
            }
        },
        deleteData: function () {
            let apiClient = new ApiApiFactory()
            apiClient.destroyOpenDataStore(this.store.id).then(r => {
                this.cancelAction()
                StandardToasts.makeStandardToast(this, StandardToasts.SUCCESS_DELETE)
            }).catch((err) => {
                StandardToasts.makeStandardToast(this, StandardToasts.FAIL_DELETE, err, true)
            })
        },
        addCategory() {
            if (this.store.category_to_store.filter(x => x.category.id === this.adding_category.id).length === 0) {
                this.store.category_to_store.push(
                    {
                        category: this.adding_category,
                        store: this.store.id,
                        order: 0
                    }
                )
            }
        },
        deleteCategory: function (c) {
            this.store.category_to_store = this.store.category_to_store.filter(x => x !== c)
        },
        sortCategories: function () {
            this.store.category_to_store.forEach(function (element, index) {
                element.order = index
            })
        },
        cancelAction: function () {
            this.$emit("hidden")
        },
    },
}
</script>
