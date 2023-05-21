const BundleTracker = require("webpack-bundle-tracker")

const plugin_pages = {
    open_data_test_view: {
        entry: "./open_data_source/apps/OpenDataTestView/main.js",
        chunks: ["open-data-plugin-chunk-vendors","open-data-plugin-locales-chunk","open-data-plugin-api-chunk"],
    }
}

module.exports = {
    pages: plugin_pages,
    filenameHashing: false,
    productionSourceMap: false,
    publicPath: process.env.NODE_ENV === "production" ? "" : "http://localhost:8080/",
    outputDir: "../static/vue/",
    runtimeCompiler: true,
    pwa: {
        name: "OpenDataPlugin",
        themeColor: "#4DBA87",
        msTileColor: "#000000",
        appleMobileWebAppCapable: "yes",
        appleMobileWebAppStatusBarStyle: "black",

        // workboxPluginMode: "InjectManifest",
        // workboxOptions: {
        //     swSrc: "./src/sw.js",
        //     swDest: "../../templates/sw.js",
        //     manifestTransforms: [
        //         (originalManifest) => {
        //             const result = originalManifest.map((entry) => new Object({url: "static/vue/" + entry.url}))
        //             return {manifest: result, warnings: []}
        //         },
        //     ],
        // },
    },
    pluginOptions: {
        i18n: {
            locale: "en",
            fallbackLocale: "en",
            localeDir: "locales",
            enableInSFC: true,
        },
    },
    chainWebpack: (config) => {
        config.optimization.splitChunks(
            {
                cacheGroups: {
                    locale: {
                        test: /[\\/]src[\\/]locales[\\/]/,
                        name: "open-data-plugin-locales-chunk",
                        chunks: "all",
                        priority: 3,
                    },
                    api: {
                        test: /[\\/]src[\\/]utils[\\/]openapi[\\/]/,
                        name: "open-data-plugin-api-chunk",
                        chunks: "all",
                        priority: 3,
                    },
                    vendor: {
                        test: /[\\/]node_modules[\\/]/,
                        name: "open-data-plugin-chunk-vendors",
                        chunks: "all",
                        priority: 1,
                    },
                },
            },
        )

        config.optimization.minimize(true)

        //TODO somehow remov them as they are also added to the manifest config of the service worker
        /*
        Object.keys(pages).forEach(page => {
            config.plugins.delete(`html-${page}`);
            config.plugins.delete(`preload-${page}`);
            config.plugins.delete(`prefetch-${page}`);
        })
        */

        config.plugin("BundleTracker").use(BundleTracker, [{relativePath: true, path: "../vue/"}])

        config.resolve.alias.set("__STATIC__", "static")

        //config.resolve.alias.set("@", "../../../recipes_src")

        config.devServer
            .host("localhost")
            .port(8080)
            .set('hot', 'only')
            .set('static', {watch: true})
            // old webpack dev server v3 settings
            //  .hotOnly(true)
            //   .watchOptions({ poll: 500 })
            //  .public("http://localhost:8080")
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["*"]})
    },
}
