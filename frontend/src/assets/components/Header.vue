<template>
  <header class="flex bg-white w-full h-[60px] sticky top-0 z-50 place-content-center">
    <div class="flex py-3 px-[50px] h-94px w-[1120px] place-content-between items-center">
        <div>
            <router-link to="/" class="flex items-center space-x-2 ">
                <img src="../images/logo.png" alt="logo" class="h-[150px] w-[150px] object-contain">
            </router-link>
        </div>
        <div class="relative max-w-md">
            <input
                v-model="query"
                type="text"
                placeholder="Search books..."
                class="relative bg-gray-300 placeholder:text-black w-[230px] h-[30px] left-[200px] pl-10 pr-4 py-2 rounded-[30px] border focus:border-blue-500 focus:ring-2 focus:ring-blue-200 outline-none transition"
                />
            <svg
                xmlns="http://www.w3.org/2000/svg"
                class="absolute left-[210px] top-[15px] -translate-y-1/2 h-5 w-5 text-gray-400"
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
                class="absolute right-[-190px] top-[15px] -translate-y-1/2 text-gray-600 hover:text-gray-600"
                >
                ✕
            </button>
        </div>
        <div>
            <router-link to="/profile">
                <img src="../images/profile.png" alt="profile icon">
            </router-link>
        </div>
    </div>
  </header>

</template>

<script setup>
import { ref } from 'vue';

const query = ref("")

function clearSearch() {
    query.value = ""
}

</script>
