import { createMemoryHistory, createRouter } from "vue-router";
import Products from "./components/products/Products.vue"
import NotFound from "./components/NotFound.vue";
import Home from "./views/Home.vue"
import ProductDetail from "./views/ProductDetail.vue"
import Orders from "./views/Orders.vue"

export default createRouter( {
    history: createMemoryHistory(),
    routes: [
        { path: "/", component: Home},
        { path: "/products", component: Products},
        { path: "/product/:id", component: ProductDetail, props: true},
        { path: "/not_found", component: NotFound},
        { path: "/orders", component: Orders}
    ],
})
