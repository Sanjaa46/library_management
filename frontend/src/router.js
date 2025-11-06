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
		name: "search",
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
	{
		name: "MembershipSuccess",
		path: "/frontend/membership-success",
		component: () => import("@/pages/MembershipSuccess.vue"),
	},
]

const router = createRouter({
	history: createWebHistory(),
	routes,
})

router.beforeEach(async (to, from, next) => {
  	// For development: allow all pages
	// next()

	let isLoggedIn = session.isLoggedIn
	try {
		await userResource.promise
	} catch (error) {
		isLoggedIn = false
	}
	
	
	// If user is not logged in and tries to visit a protected page
	if (!isLoggedIn && !["Login", "Signup"].includes(to.name)) {
		return next({ name: "Login" });
	}

	// If user is logged in and tries to visit Login or Signup
	if (isLoggedIn && ["Login", "Signup"].includes(to.name)) {
		return next({ name: "Home" });
	}

	// Otherwise, allow navigation
	next();
});

export default router
