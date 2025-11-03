<template>
    <footer class=" flex bg-[#2c3e50] w-full justify-center">
        <div class="flex justify-between w-[1120px] mx-auto py-8 relative">
            <div class="w-[30%]"> <!-- Logo and description -->
                <img src="../images/logo.png" class="m-5" alt="footer logo">
                <p class="w-[400px]">Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.</p>
                <div class="w-[150px] py-5 flex place-content-between">
                    <a href=""><img src="../images/email.png" alt="email icon"></a>
                    <img src="../images/facebook.png" alt="facebook icon">
                    <img src="../images/twitter.png" alt="twitter icon">
                </div>
            </div>
            <div> <!-- Sitemap -->
                <div class="w-full h-full flex items-center justify-center">
                    <ul class="text-center">
                        <h1 class="font-bold text-[20px] mb-2">Site Map</h1>
                        <li><a href="#">Home Page</a></li>
                        <li><a href="#">Profile</a></li>
                        <li><a href="#">Books</a></li>
                    </ul>
                </div>
            </div>
            <a href="#" class="absolute bottom-5 z-[999] right-10"><img src="../images/arrow.png" alt="arrow"></a>
        </div>
        
    </footer>
    <div class=" w-100% bg-[#118ab2] flex justify-center">
        <p class="text-sm">Copyright © 2025, library-example.com, All Rights Reserved</p>
    </div>
</template>

<script setup></script>