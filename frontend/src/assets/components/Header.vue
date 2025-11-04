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

        <div>
            <router-link to="/frontend/profile">
                <img src="../images/profile.png" alt="profile icon" class="w-8 h-8 object-contain">
            </router-link>
        </div>
    </div>
  </header>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const query = ref("");

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