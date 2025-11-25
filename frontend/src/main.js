import { createApp } from "vue"

import rate from 'vue-rate'
import 'vue-rate/dist/vue-rate.css'

import App from "./App.vue"
import router from "./router"
import { initSocket } from "./socket"
import axios from 'axios'
import { useAuthStore } from "./data/auth"
import { createPinia } from "pinia"

const pinia = createPinia()
import {
	Alert,
	Badge,
	Button,
	Dialog,
	ErrorMessage,
	FormControl,
	Input,
	TextInput,
	frappeRequest,
	pageMetaPlugin,
	resourcesPlugin,
	setConfig,
} from "frappe-ui"

import "./index.css"

const globalComponents = {
	Button,
	TextInput,
	Input,
	FormControl,
	ErrorMessage,
	Dialog,
	Alert,
	Badge,
}
const app = createApp(App).use(rate)


setConfig("resourceFetcher", frappeRequest)

app.use(router)
app.use(resourcesPlugin)
app.use(pageMetaPlugin)
app.use(pinia)

axios.interceptors.request.use((config) => {
	const auth = useAuthStore()
	if (auth.accessToken) {
		config.headers.Authorization = `Bearer ${auth.accessToken}`;
		console.log(auth.accessToken);
	}
	return config;
})

const socket = initSocket()
// app.config.globalProperties.$socket = socket
app.provide('socket', socket)

socket.on("connect", () => {
	console.log("Connected!")
})


for (const key in globalComponents) {
	app.component(key, globalComponents[key])
}

app.mount("#app")
