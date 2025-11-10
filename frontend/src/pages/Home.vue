<template>
    <Header></Header>
    <div class="relative w-full h-[420px] my-10 overflow-hidden">
        <!-- Background image -->
        <img
            src="/src/assets/images/hero-section.png"
            alt="hero section image"
            class="absolute inset-0 w-full h-full object-cover"
        />

        <!-- Overlay content -->
        <div class="absolute inset-0 flex flex-col items-center justify-center bg-black/40 text-center">
            <h1 class="text-3xl md:text-4xl font-bold text-cyan-400 mb-2">
            DISCOVER YOUR NEXT ADVENTURE
            </h1>
            <p class="text-blue-200 text-lg max-w-[600px]">
            Explore our Collection of Books, Resources & Community Events
            </p>
        </div>
    </div>
    <FeaturedBooks />
    <Contact></Contact>
    <Footer></Footer>
</template>

<script setup>
import Header from '../assets/components/Header.vue';
import Footer from '../assets/components/Footer.vue';
import FeaturedBooks from '../assets/components/FeaturedBooks.vue';
import Contact from '../assets/components/Contact.vue';

</script>
