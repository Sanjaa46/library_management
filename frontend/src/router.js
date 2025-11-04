import { userResource } from "@/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"

const routes = [
	{
		path: "/frontend",
		name: "Home",
		component: () => import("@/pages/Home.vue"),
	},
	{
		name: "Login",
		path: "/frontend/account/login",
		component: () => import("@/pages/Login.vue"),
	},
	{
		name: "Signup",
		path: "/frontend/account/signup",
		component: () => import("@/pages/Signup.vue"),
	},
	{
		name: "Search",
		path: "/frontend/search",
		component: () => import("@/pages/SearchResult.vue"),
	},
	{
		name: "Profile",
		path: "/frontend/profile",
		component: () => import("@/pages/Profile.vue"),
	},
	{
		name: "Bookinfo",
		path: "/frontend/book",
		component: () => import("@/pages/BookInfo.vue"),
	},
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

router.beforeEach(async (to, from, next) => {
  // For development: allow all pages
  next();
});

export default router
