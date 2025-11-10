<template>
    <footer class=" flex flex-col bg-[#2c3e50] w-full justify-center mt-10 bottom-0">
        <div class="flex justify-between w-[1120px] mx-auto py-8 relative">
            <div class="w-[30%]"> <!-- Logo and description -->
                <img src="../images/logo.png" class="m-5" alt="footer logo">
                <p class="w-[400px]">Энэхүү систем нь энгийн номын сангийн удирдлагын систем бөгөөд номын санч болон уншигчдад (Library Member) зориулсан.</p>
                <div class="w-[150px] py-5 flex place-content-between">
                    <a href=""><img src="../images/email.png" alt="email icon"></a>
                    <img src="../images/facebook.png" alt="facebook icon">
                    <img src="../images/twitter.png" alt="twitter icon">
                </div>
            </div>
            <div> <!-- Sitemap -->
                <div class="relative w-full h-full flex items-center justify-center bottom-5">
                    <ul class="text-center">
                        <h1 class="font-bold text-[20px] mb-2">Site Map</h1>
                        <router-link to="/frontend">
                            <li>Home Page</li>
                        </router-link>
                        <router-link to="/frontend/profile">
                            <li>Profile</li>
                        </router-link>
                        <router-link to="/frontend/search">
                            <li>Books</li>
                        </router-link>
                    </ul>
                </div>
            </div>
            <button @click="scrollTop" class="absolute bottom-5 z-[999] right-[-100px] "><img src="../images/arrow.png" alt="arrow"></button>
        </div>
        
        <div class=" w-full bg-[#118ab2] flex justify-center bottom-0">
            <p class="text-sm">Copyright © 2025, library-example.com, All Rights Reserved</p>
        </div>
    </footer>
</template>

<script setup>
function scrollTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>