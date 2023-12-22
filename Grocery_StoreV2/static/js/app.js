import router from "./router.js"
Vue.use(VueRouter)
new Vue({
    el: '#app',
    router : router,

    data: {
        message: "Hello World!!"
    },
    methods: {

    }
});
