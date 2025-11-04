<template>
<section class="max-w-[1120px] mx-auto px-4 py-12">
    <div class="w-[1120px] my-8 mx-auto text-[24px] font-bold relative">
        <div class="absolute w-1 h-12 bg-[#118ab2] left-0"></div>
        <h1 class="text-4xl font-bold pl-5 pt-2">Featured Books</h1>
    </div>
    
    <Carousel v-bind="carouselConfig">
      <Slide v-for="book in books" :key="book.article_name">
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
import { ref, onMounted } from 'vue';

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

const books = ref([])
const loading = ref(false)

onMounted(async () => {
  try {
    const response = await fetch('/api/method/library_management.api.get_books', {
      credentials: 'include'
    });
    const data = await response.json();
    books.value = data.message.data;
  } catch (error) {
    console.error('Failed to fetch books:', error);
    books.value = [];
  } finally {
    loading.value = false;
  }
  console.log(books.value);
});

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