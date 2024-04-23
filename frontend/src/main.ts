import { createApp } from 'vue'
import router from "./router"
import App from './App.vue'
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap/dist/js/bootstrap.js"
import "bootstrap-icons/font/bootstrap-icons.min.css"

const app = createApp(App)
app.use(router).mount("#app")


