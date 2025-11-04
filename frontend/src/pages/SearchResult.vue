<template>
<Header></Header>
<section class="max-w-[1120px] mx-auto px-4 py-12">
    <div class="w-[1120px] my-8 mx-auto text-[24px] font-bold relative">
        <div class="absolute w-1 h-12 bg-[#118ab2] left-0"></div>
        <h1 class="text-4xl font-bold pl-5 pt-2">Search result for <i>'{{ searchQuery }}'</i></h1>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="text-center py-12">
        <p class="text-gray-600 text-[24px]">Loading...</p>
    </div>

    <!-- Result Container -->
    <div v-else>
        <!-- Book grid -->
        <div v-if="books.length > 0" class="mx-auto mt-0 mb-[50px] grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-[20px]">
            <Article v-for="book in books" :key="book.article_name" :book="book" />
        </div>

        <div v-else class="text-center py-12">
            <p class="text-gray-600 text-[24px]">No books found matching your search.</p>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="flex items-center justify-center gap-2 mt-8 mb-12">
            <!-- Previous Button -->
            <button 
                @click="goToPage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-4 py-2 rounded-lg border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
                Previous
            </button>

            <!-- Page Numbers -->
            <div class="flex gap-2">
                <!-- First Page -->
                <button 
                    v-if="showFirstPage"
                    @click="goToPage(1)"
                    class="px-4 py-2 rounded-lg border transition-colors"
                    :class="currentPage === 1 ? 'bg-[#118ab2] text-white border-[#118ab2]' : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'"
                >
                    1
                </button>

                <!-- Left Ellipsis -->
                <span v-if="showLeftEllipsis" class="px-2 py-2 text-gray-500">...</span>

                <!-- Middle Pages -->
                <button 
                    v-for="page in middlePages"
                    :key="page"
                    @click="goToPage(page)"
                    class="px-4 py-2 rounded-lg border transition-colors"
                    :class="currentPage === page ? 'bg-[#118ab2] text-white border-[#118ab2]' : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'"
                >
                    {{ page }}
                </button>

                <!-- Right Ellipsis -->
                <span v-if="showRightEllipsis" class="px-2 py-2 text-gray-500">...</span>

                <!-- Last Page -->
                <button 
                    v-if="showLastPage"
                    @click="goToPage(totalPages)"
                    class="px-4 py-2 rounded-lg border transition-colors"
                    :class="currentPage === totalPages ? 'bg-[#118ab2] text-white border-[#118ab2]' : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'"
                >
                    {{ totalPages }}
                </button>
            </div>

            <!-- Next Button -->
            <button 
                @click="goToPage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="px-4 py-2 rounded-lg border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
                Next
            </button>
        </div>

    </div>
</section>
<Footer></Footer>
</template>

<script setup>
import Article from '../assets/components/Article.vue';
import Header from '../assets/components/Header.vue';
import Footer from '../assets/components/Footer.vue';
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const books = ref([]);
const loading = ref(false);
const searchQuery = ref('');
const currentPage = ref(1)
const pageSize = ref(10);
const total = ref(0);
const totalPages = ref(0);

// Paginition computed properties
const showFirstPage = computed(() => {
    return currentPage.value > 3
});

const showLastPage = computed(() => {
    return currentPage.value < totalPages.value - 2
});

const showLeftEllipsis = computed(() => {
    return currentPage.value > 4
});

const showRightEllipsis = computed(() => {
    return currentPage.value < totalPages - 3
});

const middlePages = computed(() => {
    const pages = [];
    let start = Math.max(2, currentPage.value - 2);
    let end = Math.min(totalPages.value - 1, currentPage.value + 2);

    // near start
    if (currentPage.value <= 3) {
        start = 2;
        end = Math.min(5, totalPages.value - 1);
    }

    // near end
    if (currentPage.value >= totalPages.value - 2) {
        start = Math.max(2, totalPages.value - 4);
        end = totalPages.value - 1;
    }

    for (let i = start; i <= end; i++) {
        pages.push(i);
    }

    return pages;
});

// Fetch books 
const fetchBooks = async () => {
    loading.value = true;

    const url = `/api/method/library_management.api.search?query=${searchQuery.value}&page=${currentPage.value}&page_size=${pageSize.value}`

    try {
        const response = await fetch(url, {
            credentials: 'include',
            method: 'GET',
        });
        const data = await response.json()

        books.value = data.message.results;
        total.value = data.message.total;
        totalPages.value = data.message.total_pages;
    }
    catch (error) {
        console.error("Failed to fetch books: ", error);
        books.value = [];
        total.value = 0;
        totalPages.value = 0;
    } finally {
        loading.value = false;
    }
}

// Go to specific page
const goToPage = (page) => {
    if (page < 1 || page > totalPages.value) return;

    currentPage.value = page;
    // Update URL query params
    router.push({
        query: {
            ...route.query,
            page: page
        }
    });

    window.scrollTo({ top: 0, behavior: 'smooth' })

    fetchBooks();
}

onMounted(async () => {
    // Get query from URL params
    searchQuery.value = route.query.q || route.query.query || 'a';
    currentPage.value = parseInt(route.query.page) || 1;

    watch(() => route.query, (newQuery) => {
       searchQuery.value = newQuery.q || newQuery.query || 'a';
       currentPage.value = parseInt(newQuery.page) || 1;
       fetchBooks();
   }, { deep: true });
    
    await fetchBooks();
});

</script>