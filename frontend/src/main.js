import { createApp } from "vue"

import rate from 'vue-rate'
import 'vue-rate/dist/vue-rate.css'

import { io } from 'socket.io-client'

import App from "./App.vue"
import router from "./router"
import { initSocket } from "./socket"
import { FrappeUI } from "frappe-ui"

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
