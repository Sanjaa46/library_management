import router from "@/router"
import { createResource } from "frappe-ui"
import { computed, reactive } from "vue"

import { userResource } from "./user"

export function sessionUser() {
	const cookies = new URLSearchParams(document.cookie.split("; ").join("&"))
	let _sessionUser = cookies.get("user_id")
	if (_sessionUser === "Guest") {
		_sessionUser = null
	}
	return _sessionUser
}

export const session = reactive({
	login: createResource({
		url: "login",
		makeParams({ email, password }) {
			return {
				usr: email,
				pwd: password,
			}
		},
		onSuccess: async function(data) {
			userResource.reload()
			session.user = sessionUser()
			session.login.reset()
			
			const userName = await getUserRoles();

			if (userName === "Administrator" || userName === "librarian@example.com") {
				router.replace("/app"); // Frappe Desk
			} else {
				router.replace("/frontend"); // Library Member UI
			}
		},
	}),
	logout: createResource({
		url: "logout",
		onSuccess() {
			userResource.reset()
			session.user = sessionUser()
			router.replace({ name: "Login" })
		},
	}),
	user: sessionUser(),
	isLoggedIn: computed(() => !!session.user),
})

async function getUserRoles() {
  const user = await fetch("/api/method/frappe.auth.get_logged_user", {
    credentials: "include",
  }).then(r => r.json());

  return user.message;
}
