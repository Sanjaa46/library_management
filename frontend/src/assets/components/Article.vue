<template>
  <article class="relative w-[210px] h-[300px] rounded-[10px] overflow-hidden shadow-[0_15px_35px_rgba(255,255,255,0.25)] group">
      <a :href="`/frontend/book?article_name=${book.article_name}`">
        <div class="poster relative overflow-hidden">
          <img :src="book.image" :alt="book.image"
            class="w-full transition-all duration-500 group-hover:-translate-y-[50px] group-hover:blur-[5px]" />

          <!-- Overlay -->
          <div class="absolute bottom-[-80px] left-0 w-full h-full bg-gradient-to-t from-[#0e0d0d] to-transparent transition-all duration-500 z-[1] group-hover:bottom-0"></div>
        </div>

        <div
          class="details absolute left-0 bottom-[-40px] p-5 w-full z-[2] transition-all duration-500 group-hover:bottom-10">
          <h3 class="text-white font-bold text-[19px]">{{ book.article_name }}</h3>

          <div class="info text-[12px] mt-2">
            <p class="text-white font-bold text-[14px]">{{ book.author }}</p>
          </div>
        </div>
      </a>
    </article>
</template>

<script setup>
defineProps({
  book: {
    type: Object,
    required: true
  }
});

</script>