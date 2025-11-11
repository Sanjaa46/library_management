<template>

<article class="w-full h-[70%] bg-black-overlay-30 rounded-[20px] mx-5 shadow-xl">
    <div class="flex p-3">
        <img src="../images/profile.png" alt="">
        <h1 class="my-auto ml-3">{{ review.library_member }}</h1>
    </div>
    <rate :length="5" v-model="review.rating" :disabled="true" :readonly="true" class="" />
    <p class="w-full h-[20px] p-1">{{ review.review }}</p>
</article>

</template>

<script setup>
import { ref, onMounted, defineProps } from 'vue';

defineProps({
  review: {
    type: Object,
    required: true
  }
});

</script>