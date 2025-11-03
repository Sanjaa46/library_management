<template>
<Header></Header>
<section class="max-w-[1120px] mx-auto px-4 py-12">
    <div class="w-[1120px] my-8 mx-auto text-[24px] font-bold relative">
        <div class="absolute w-1 h-12 bg-[#118ab2] left-0"></div>
        <h1 class="text-4xl font-bold pl-5 pt-2">Search result for 'query'</h1>
    </div>

    <!-- 12 Articles Container -->
    <div class="mx-auto mt-0 mb-[50px] grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-[20px]">
        <Article v-for="book in books" :key="book.id" :book="book" />
    </div>
</section>
<Footer></Footer>
</template>

<script setup>
import Article from '../assets/components/Article.vue';
import Header from '../assets/components/Header.vue';
import Footer from '../assets/components/Footer.vue';

const books = [
  { id: 1, title: 'Rich Dad Poor Dad', author: 'Robert Kiyosaki', image: '/src/assets/images/richpoor.jpeg' },
  { id: 2, title: 'Rich Dad Poor Dad', author: 'Robert Kiyosaki', image: '/src/assets/images/richpoor.jpeg' },
  { id: 3, title: 'Rich Dad Poor Dad', author: 'Robert Kiyosaki', image: '/src/assets/images/richpoor.jpeg' },
  { id: 4, title: 'Rich Dad Poor Dad', author: 'Robert Kiyosaki', image: '/src/assets/images/richpoor.jpeg' },
  { id: 5, title: 'Rich Dad Poor Dad', author: 'Robert Kiyosaki', image: '/src/assets/images/richpoor.jpeg' },
  { id: 6, title: 'Rich Dad Poor Dad', author: 'Robert Kiyosaki', image: '/src/assets/images/richpoor.jpeg' },
  { id: 7, title: 'Rich Dad Poor Dad', author: 'Robert Kiyosaki', image: '/src/assets/images/richpoor.jpeg' },
  { id: 8, title: 'Rich Dad Poor Dad', author: 'Robert Kiyosaki', image: '/src/assets/images/richpoor.jpeg' },
  { id: 9, title: 'Rich Dad Poor Dad', author: 'Robert Kiyosaki', image: '/src/assets/images/richpoor.jpeg' },
  { id: 10, title: 'Rich Dad Poor Dad', author: 'Robert Kiyosaki', image: '/src/assets/images/richpoor.jpeg' },
];
</script>