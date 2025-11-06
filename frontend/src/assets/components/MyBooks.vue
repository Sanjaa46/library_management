<template>

<h1 class=" pl-[20px] pb-[20px] text-[30px] font-bold">My Books</h1>



<div class=" w-[90%] relative mx-auto overflow-x-auto shadow-md sm:rounded-lg">
    <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400 ">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
                <th scope="col" class="px-6 py-3">
                    Article name
                </th>
                <th scope="col" class="px-6 py-3">
                    Issued Date
                </th>
                <th scope="col" class="px-6 py-3">
                    Due Date
                </th>
            </tr>
        </thead>
        <tbody>
            <ArticleListItem v-for="book in books" :key="book.article_name" :book="book" />
        </tbody>
    </table>
</div>


</template>


<script setup>
import ArticleListItem from './ArticleListItem.vue';
import { onMounted, ref } from 'vue';

const books = ref([])

onMounted(async () => {
    try {
        const response = await fetch('/api/method/library_management.api.my_books', {
            credentials: 'include'
        })
        const data = await response.json();
        books.value = data.message

    } catch (error) {
        console.error("Failed to fetch books: ", error)
        books.value = []
    }
})


</script>