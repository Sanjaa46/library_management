<template>
  <header class="flex bg-white w-full h-[60px] sticky top-0 z-50 place-content-center shadow-sm">
    <div class="flex py-3 px-[50px] h-94px w-[1120px] place-content-between items-center">
        <div>
            <router-link to="/frontend" class="flex items-center space-x-2">
                <img src="../images/logo.png" alt="logo" class="h-[150px] w-[150px] object-contain">
            </router-link>
        </div>
        
        <form @submit.prevent="handleSearch" class="relative max-w-md">
            <input
                v-model="query"
                type="text"
                placeholder="Search books..."
                @keyup.enter="handleSearch"
                class="relative bg-gray-300 placeholder:text-black w-[230px] h-[30px] left-[200px] pl-10 pr-4 py-2 rounded-[30px] border focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition"
            />
            <svg
                xmlns="http://www.w3.org/2000/svg"
                class="absolute left-[210px] top-[15px] -translate-y-1/2 h-5 w-5 text-gray-400 pointer-events-none"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
            >
                <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M21 21l-4.35-4.35M11 18a7 7 0 1 1 0-14 7 7 0 0 1 0 14z"
                />
            </svg>

            <button
                v-if="query"
                @click="clearSearch"
                type="button"
                class="absolute right-[-190px] top-[15px] -translate-y-1/2 text-gray-600 hover:text-gray-800 transition-colors"
            >
                ✕
            </button>
        </form>

        <div class="relative left-[150px] bottom-[-5px]">
            <!-- Bell icon -->
            <button @click="toggleDropdown" class="relative">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none"
                    viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14V11a6 6 0 10-12 0v3c0 .386-.146.737-.395 1.005L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <!-- Badge -->
                <span
                v-if="unreadCount > 0"
                class="absolute -top-1 -right-1 bg-red-600 text-xs rounded-full w-4 h-4 flex items-center justify-center">
                {{ unreadCount }}
                </span>
            </button>

            <!-- Dropdown -->
            <div v-if="dropdownOpen" class="absolute right-[-10px] mt-2 w-64 bg-white text-black rounded-lg shadow-lg z-10">
                <ul>
                    <li v-for="n in notifications" :key="n.name"
                        @click="markAsRead(n.name)"
                        class="px-3 py-2 border-b last:border-none cursor-pointer"
                        :class="{ 'opacity-50': n.is_read }">
                        <p class="font-semibold text-sm">{{ n.title }}</p>
                        <p class="text-xs text-gray-600">{{ n.message }}</p>
                    </li>
                </ul>
            </div>
        </div>

        <div>
            <router-link to="/frontend/profile">
                <img src="../images/profile.png" alt="profile icon" class="w-8 h-8 object-contain">
            </router-link>
        </div>
    </div>
  </header>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const query = ref("");

const dropdownOpen = ref(false)
const notifications = ref([])
const unreadCount = ref(0)

function toggleDropdown() {
  dropdownOpen.value = !dropdownOpen.value
  if (dropdownOpen.value) fetchNotifications()
}

// Notification API calls next.

async function fetchNotifications() {
  try {
    const res = await fetch("/api/method/library_management.api.get_notifications")
    const data = await res.json()
    notifications.value = data.message || []
    unreadCount.value = notifications.value.filter(n => !n.is_read).length
  } catch (err) {
    console.error("Failed to load notifications:", err)
  }
}

async function markAsRead(name) {
  try {
    await fetch("/api/method/library_management.api.mark_as_read", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name })
    })

    const n = notifications.value.find(i => i.name === name)
    if (n) n.is_read = true
    unreadCount.value = notifications.value.filter(n => !n.is_read).length
  } catch (err) {
    console.error("Failed to mark as read:", err)
  }
}

onMounted(() => {
  fetchNotifications()
})

// Initialize query from URL if on search page
if (route.name === 'frontend/search' || route.path.includes('frontend/search')) {
    query.value = route.query.q || route.query.query || '';
}

// Watch route changes to update search input
watch(() => route.query, (newQuery) => {
    if (route.name === 'frontend/search' || route.path.includes('frontend/search')) {
        query.value = newQuery.q || newQuery.query || '';
    }
}, { deep: true });

function clearSearch() {
    query.value = "";
}

function handleSearch() {
    if (!query.value.trim()) return;
    
    const trimmedQuery = query.value.trim();
    
    // If already on search page, just update the query params
    if (route.name === 'frontend/search' || route.path.includes('search')) {
        router.replace({
            path: '/frontend/search',
            query: {
                q: trimmedQuery,
                page: 1
            }
        });
    } else {
        router.push({
            path: '/frontend/search',
            query: {
                q: trimmedQuery,
                page: 1
            }
        });
    }
}
</script>