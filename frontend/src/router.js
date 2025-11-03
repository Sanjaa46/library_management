import { userResource } from "@/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"

const routes = [
	{
		path: "/",
		name: "Home",
		component: () => import("@/pages/Home.vue"),
	},
	{
		name: "Login",
		path: "/account/login",
		component: () => import("@/pages/Login.vue"),
	},
	{
		name: "Signup",
		path: "/account/signup",
		component: () => import("@/pages/Signup.vue"),
	},
	{
		name: "Search",
		path: "/search",
		component: () => import("@/pages/SearchResult.vue"),
	},
	{
		name: "Profile",
		path: "/profile",
		component: () => import("@/pages/Profile.vue"),
	},
	{
		name: "Bookinfo",
		path: "/book",
		component: () => import("@/pages/BookInfo.vue"),
	},
]

const router = createRouter({
	history: createWebHistory("/frontend"),
	routes,
})

router.beforeEach(async (to, from, next) => {
  // For development: allow all pages
  next();
});

export default router
