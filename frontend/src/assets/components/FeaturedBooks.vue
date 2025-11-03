<template>
<section class="max-w-[1120px] mx-auto px-4 py-12">
    <div class="w-[1120px] my-8 mx-auto text-[24px] font-bold relative">
        <div class="absolute w-1 h-12 bg-[#118ab2] left-0"></div>
        <h1 class="text-4xl font-bold pl-5 pt-2">Featured Books</h1>
    </div>
    
    <Carousel v-bind="carouselConfig">
      <Slide v-for="book in books" :key="book.id">
        <Article :book="book" />
      </Slide>

      <template #addons>
        <Navigation />
      </template>
    </Carousel>
</section>
</template>

<script setup>
import 'vue3-carousel/carousel.css';
import Article from '../components/Article.vue';
import { Carousel, Slide, Navigation } from 'vue3-carousel';

const carouselConfig = {
  itemsToShow: 4.5,
  snapAlign: 'start',
  wrapAround: false,
  transition: 500,
  breakpoints: {
    320: {
      itemsToShow: 1.5,
    },
    640: {
      itemsToShow: 2.5,
    },
    1024: {
      itemsToShow: 5,
    },
  }
};

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
];
</script>

<style>
/* Custom carousel navigation styling */
.carousel__prev,
.carousel__next {
  background-color: black;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  color: white;
}

.carousel__prev:hover,
.carousel__next:hover {
  background-color: rgb(31, 31, 31);
}

.carousel__prev {
    position: absolute;
    left: -60px;
}

.carousel__next {
    position: absolute;
    right: -60px;
}
</style>