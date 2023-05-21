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
    static OPEN_DATA_UNIT = {
        name: "OpenDataUnit",
        apiName: "OpenDataUnit",
        apiClient: new ApiApiFactory(),
        table_fields: ["slug", "name"],
        create: {
            params: [["name", "plural_name", "comment", "slug",]],
            form: {
                show_help: true,
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
                comment: {
                    form_field: true,
                    type: "text",
                    field: "comment",
                    label: "comment",
                    placeholder: "",
                },
                slug: {
                    form_field: true,
                    type: "text",
                    field: "slug",
                    label: "Slug",
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
            params: [["slug", "name", "comment",]],
            form: {
                show_help: true,
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
                show_help: true,
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

    static OPEN_DATA_PROPERTY = {
        name: "OpenDataProperty",
        apiName: "OpenDataProperty",
        apiClient: new ApiApiFactory(),
        table_fields: ["slug", "name"],
        create: {
            params: [["slug", "name", "unit", "comment",]],
            form: {
                show_help: true,
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
        table_fields: ["slug", "food", "base_unit", "converted_unit"],
        create: {
            params: [["slug", "food", "base_amount", "base_unit", "converted_amount", "converted_unit", "source", "comment"]],
            form: {
                show_help: true,
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