<template>
<Header></Header>

<div class="w-[1120px] my-8 mx-auto text-[24px] font-bold relative">
    <div class="absolute w-1 h-12 bg-[#118ab2] left-0"></div>
    <h1 class="text-4xl font-bold pl-5 pt-2">Book Info</h1>
</div>

<section  class="flex w-[1120px] p-[30px] mx-auto my-10">
    <!-- Book image and Author -->
    <div class="flex flex-col w-[20%] items-center justify-center">
        <img :src="book.image" class="w-[200px] h-[300px] object-contain rounded-[5px]" alt="book image">
        <p class="text-center mt-5">{{ book.author }}</p>
    </div>

    <!-- Book information -->
    <div class="w-[80%] ml-10">
        <h1 class="text-[25px] font-medium">{{ book.article_name }}</h1>
        <div class="flex my-5 space-x-5 text-[15px]">
            <p><b>Author: </b>{{ book.author }}</p>
            <p><b>Publisher: </b>{{ book.publisher }}</p>
            <p><b>ISBN: </b>{{ book.isbn }}</p>
            <p><b>Status: </b>{{ book.status }}</p>
        </div>
        <h1 class="text-[18px] font-medium">Description</h1>
        <p>
            {{ book.description }}
        </p>
        <Button variant="solid" class="bg-[#1290b9] w-[90px] text-white my-10 rounded hover:bg-[#016475] transition">
        Issue
        </Button>
    </div>
</section>


<Footer></Footer>
</template>


<script setup>
import Header from '../assets/components/Header.vue';
import Footer from '../assets/components/Footer.vue';
import { defineProps, ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const book = ref({})
const articleName = ref("")

onMounted(async () => {
    articleName.value = route.query.article_name;
    console.log(articleName.value)

    const url = `/api/method/library_management.api.book_info?article_name=${articleName.value}`

    try {
        const response = await fetch(url, {
            credentials: 'include',
            method: 'POST',
            body: {
                article_name: articleName.value
            }
        });
        const data = await response.json()

        book.value = data.message
    }
    catch (error) {
        console.error("Failed to fetch books: ", error);
    }
})

</script>