import {Actions, Models} from "@/utils/models";
import {ApiApiFactory} from "./openapi/api";

export const ModelMixin = {
    data() {
        return {
            OpenDataModels: OpenDataModels,
        }
    },
}

export class OpenDataModels extends Models {

    static OPEN_DATA_HOME = {
        name: "OpenDataHome",
        // Helper model
    }

    static OPEN_DATA_VERSION = {
        name: "OpenDataVersion",
        apiName: "OpenDataVersion",
        apiClient: new ApiApiFactory(),
        table_fields: ["name", "code"],
        create: {
            params: [["name", "code", "comment",]],
            form: {
                show_help: true,
                name: {
                    form_field: true,
                    type: "text",
                    field: "name",
                    label: "Name",
                },
                code: {
                    form_field: true,
                    type: "text",
                    field: "code",
                    label: "Code",
                    placeholder: "en, de, de-DE, de-AT",
                },
                comment: {
                    form_field: true,
                    type: "text",
                    field: "comment",
                    label: "comment",
                    placeholder: "",
                },
            },
        },
        merge: true,
    }

    static OPEN_DATA_UNIT = {
        name: "OpenDataUnit",
        apiName: "OpenDataUnit",
        apiClient: new ApiApiFactory(),
        table_fields: ["slug", "name"],
        create: {
            params: [["version", "slug", "name", "plural_name", "base_unit", "type", "comment",]],
            form: {
                show_help: true,
                version: {
                    form_field: true,
                    type: "lookup",
                    field: "version",
                    list: "OPEN_DATA_VERSION",
                    label: "Version",
                    allow_create: false,
                },
                slug: {
                    form_field: true,
                    type: "text",
                    field: "slug",
                    label: "Slug",
                },
                name: {
                    form_field: true,
                    type: "text",
                    field: "name",
                    label: "Name",
                    placeholder: "",
                },
                plural_name: {
                    form_field: true,
                    type: "text",
                    field: "plural_name",
                    label: "Plural name",
                    placeholder: "",
                },
                base_unit: {
                    form_field: true,
                    type: "choice",
                    options: [
                        {value: "G", text: "g"},
                        {value: "KG", text: "kg"},
                        {value: "ML", text: "ml"},
                        {value: "L", text: "l"},
                        {value: "OUNCE", text: "Ounce"},
                        {value: "POUND", text: "Pound"},
                        {value: "FLUID_OUNCE", text: "Fluid Ounce"},
                        {value: "TSP", text: "Tsp"},
                        {value: "TBSP", text: "Tbsp"},
                        {value: "CUP", text: "Cup"},
                        {value: "PINT", text: "Pint (US)"},
                        {value: "QUART", text: "Quart (US)"},
                        {value: "GALLON", text: "Gallon (US)"},
                        {value: "IMPERIAL_FLUID_OUNCE", text: "Imperial Fluid Ounce (GB)"},
                        {value: "IMPERIAL_PINT", text: "Imperial Pint (GB)"},
                        {value: "IMPERIAL_QUART", text: "Imperial Quart (GB)"},
                        {value: "IMPERIAL_GALLON", text: "Imperial Gallon (GB)"},
                    ],
                    field: "base_unit",
                    label: "Base Unit",
                    placeholder: "",
                },
                type: {
                    form_field: true,
                    type: "choice",
                    options: [
                        {value: "WEIGHT", text: "Weight"},
                        {value: "VOLUME", text: "Volume"},
                        {value: "OTHER", text: "Other"},
                    ],
                    field: "type",
                    label: "Type",
                    placeholder: "",
                },
                comment: {
                    form_field: true,
                    type: "text",
                    field: "comment",
                    label: "comment",
                    placeholder: "",
                },

            },
        },
        merge: true,
    }

    static OPEN_DATA_CATEGORY = {
        name: "OpenDataCategory",
        apiName: "OpenDataCategory",
        apiClient: new ApiApiFactory(),
        table_fields: ["slug", "name"],
        create: {
            params: [["version", "slug", "name", "description","comment",]],
            form: {
                show_help: true,
                version: {
                    form_field: true,
                    type: "lookup",
                    field: "version",
                    list: "OPEN_DATA_VERSION",
                    label: "Version",
                    allow_create: false,
                },
                slug: {
                    form_field: true,
                    type: "text",
                    field: "slug",
                    label: "Slug",
                },
                name: {
                    form_field: true,
                    type: "text",
                    field: "name",
                    label: "Name",
                    placeholder: "",
                },
                description: {
                    form_field: true,
                    type: "text",
                    field: "description",
                    label: "Description",
                    placeholder: "",
                },
                comment: {
                    form_field: true,
                    type: "text",
                    field: "comment",
                    label: "comment",
                    placeholder: "",
                },
            },
        },
        merge: true,
    }

    static OPEN_DATA_STORE = {
        name: "OpenDataStore",
        apiName: "OpenDataStore",
        apiClient: new ApiApiFactory(),
        table_fields: ["slug", "name"],
        create: {

            params: [["slug", "name", "comment",]],
            form: {
                component: "OpenDataStoreEditComponent",
            },
        },
        merge: true,
    }

    static OPEN_DATA_PROPERTY = {
        name: "OpenDataProperty",
        apiName: "OpenDataProperty",
        apiClient: new ApiApiFactory(),
        table_fields: ["slug", "name"],
        create: {
            params: [["version", "slug", "name", "unit", "comment",]],
            form: {
                show_help: true,
                version: {
                    form_field: true,
                    type: "lookup",
                    field: "version",
                    list: "OPEN_DATA_VERSION",
                    label: "Version",
                    allow_create: false,
                },
                slug: {
                    form_field: true,
                    type: "text",
                    field: "slug",
                    label: "Slug",
                },
                name: {
                    form_field: true,
                    type: "text",
                    field: "name",
                    label: "Name",
                    placeholder: "",
                },
                unit: {
                    form_field: true,
                    type: "text",
                    field: "unit",
                    label: "Unit",
                    placeholder: "",
                },
                fdc_id: {
                    form_field: true,
                    type: "text",
                    field: "fdc_id",
                    label: "fdc_id",
                    placeholder: "",
                },
                comment: {
                    form_field: true,
                    type: "text",
                    field: "comment",
                    label: "comment",
                    placeholder: "",
                },
            },
        },
        merge: true,
    }

    static OPEN_DATA_FOOD = {
        name: "OpenDataFood",
        apiName: "OpenDataFood",
        apiClient: new ApiApiFactory(),
        table_fields: ["slug", "name"],
        create: {
            params: [["slug", "name", "plural_name", "preferred_unit_metric", "comment",]],
            form: {
                component: "OpenDataFoodEditComponent",
            },
        },
        merge: true,
    }

    static OPEN_DATA_CONVERSION = {
        name: "OpenDataConversion",
        apiName: "OpenDataConversion",
        apiClient: new ApiApiFactory(),
        table_fields: ["slug", "food.name", "base_unit.name", "converted_unit.name"],
        create: {
            params: [["version", "slug", "food", "base_amount", "base_unit", "converted_amount", "converted_unit", "source", "comment"]],
            form: {
                show_help: true,
                version: {
                    form_field: true,
                    type: "lookup",
                    field: "version",
                    list: "OPEN_DATA_VERSION",
                    label: "Version",
                    allow_create: false,
                },
                slug: {
                    form_field: true,
                    type: "text",
                    field: "slug",
                    label: "Slug",
                },
                food: {
                    form_field: true,
                    type: "lookup",
                    field: "food",
                    list: "OPEN_DATA_FOOD",
                    label: "Food",
                    allow_create: false,
                },
                base_amount: {
                    form_field: true,
                    type: "number",
                    field: "base_amount",
                    label: "Base Amount",
                    placeholder: "",
                },
                base_unit: {
                    form_field: true,
                    type: "lookup",
                    field: "base_unit",
                    list: "OPEN_DATA_UNIT",
                    label: "Base Unit",
                    allow_create: false,
                },
                converted_amount: {
                    form_field: true,
                    type: "number",
                    field: "converted_amount",
                    label: "Converted Amount",
                    placeholder: "",
                },
                converted_unit: {
                    form_field: true,
                    type: "lookup",
                    field: "converted_unit",
                    list: "OPEN_DATA_UNIT",
                    label: "Converted Unit",
                    allow_create: false,
                },
                source: {
                    form_field: true,
                    type: "text",
                    field: "source",
                    label: "Source",
                    placeholder: "",
                },
                comment: {
                    form_field: true,
                    type: "text",
                    field: "comment",
                    label: "comment",
                    placeholder: "",
                },
            },
        },
        merge: true,
    }
}