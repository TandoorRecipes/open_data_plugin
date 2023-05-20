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
        paginated: true,
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
}