<template>
    <Header></Header>
    <div class="">
        <div class="w-[1120px] my-8 mx-auto text-[24px] font-bold relative">
            <div class="absolute w-1 h-12 bg-[#118ab2] left-0"></div>
            <h1 class="text-4xl font-bold pl-5 pt-2">Book Info</h1>
        </div>

        <section  class="flex w-[1120px] p-[30px] mx-auto my-10">
            <!-- Book image and Author -->
            <div class="flex flex-col w-[20%] items-center justify-center">
                <img :src="book.image" class="w-[200px] h-[300px] object-contain rounded-[5px]" alt="book image">
                <p class="text-center mt-5">{{ book.author }}</p>
                <rate :length="5" v-model="articleRating" :disabled="true" :readonly="true" :showcount="true" class="color-black text-center  opacity-[100%]" />
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
                <Button 
                v-if="!issueSuccess"
                @click="issueBook" 
                variant="solid" 
                :class='["bg-[#1290b9] w-[90px] text-white my-10 rounded hover:bg-[#016475] transition", issueButtonClasses]'
                >
                Issue
                </Button>
                <!-- Write review -->
                <Button 
                @click="writeReview" 
                variant="solid" 
                class="bg-[#1290b9] text-white my-10 rounded hover:bg-[#016475] transition"
                >
                Write Review
                </Button>
            </div>
        </section>
    </div>
    <section class="w-[1120px] h-[250px] flex m-auto">
        <Reviews v-if="reviews.length > 0" v-for="review in reviews" :review="review"/>
    </section>
        
    <Footer></Footer>
        
    <div v-if="popup" class="absolute w-screen top-0 h-full bg-black-overlay-300">
        <div class="flex w-full h-full justify-center items-center">
            <Card title="Write Review!" class="w-[50%]  bg-[#f7f4f0] z-10 px-12 py-10 rounded-xl shadow-lg">
                <h2 class="text-xl font-medium text-center mb-8">Write Review</h2>
                <form class="flex flex-col space-y-5 w-full " @submit.prevent="">
                    <rate :length="5" v-model="customerRating" :showcount="true" class="text-center" />
                    <textarea
                        required
                        v-model="customerReview"
                        name="review"
                        placeholder="Review..."
                        class="h-[200px]"
                    ></textarea>
                    <div class="w-full space-x-5 m-auto ">
                        <Button variant="solid" @click="sendReview" class="bg-[#007C91] w-[45%] m-auto text-white py-2 rounded hover:bg-[#006273] transition">
                            Write Review
                        </Button>
                        <Button @click="cancelWriteReview" variant="solid" class="bg-[#007C91] w-[45%] m-auto text-white py-2 rounded hover:bg-[#006273] transition">
                            Cancel
                        </Button>
                    </div>
                </form>
            </Card>
      </div>
    </div>
</template>


<script setup>
import Header from '../assets/components/Header.vue';
import Footer from '../assets/components/Footer.vue';
import { inject, defineProps, ref, onMounted, computed, watch } from 'vue';
import { io } from 'socket.io-client'
import { useRoute } from 'vue-router';
import Reviews from '../assets/components/Reviews.vue';


const route = useRoute();

const book = ref({})
const articleName = ref("")
const issueSuccess = ref(false)
const articleRating = ref(0)
const reviews = ref([])
const popup = ref(false)

// Variables for write review popup
const customerReview = ref("");
const customerRating = ref(0)

onMounted(async () => {
    articleName.value = route.query.article_name;
    const socket = inject('socket')

    const url = `/api/method/library_management.api.book_info?article_name=${articleName.value}`

    // Fetch book info
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
        articleRating.value = parseInt(data.message.rating)
    }
    catch (error) {
        console.error("Failed to fetch books: ", error);
    }

    // Check user have an active issue
    try {
        const check_issue_url = `/api/method/library_management.api.has_active_issue?book=${articleName.value}`
        
        const response = await fetch(check_issue_url, {
            credentials: 'include'
        })
        const check_issue_data = await response.json();
        issueSuccess.value = check_issue_data.message
    } catch(error) {
        console.error("Failed to check the user have an active issue: ", error)
    }

    await fetchBookReviews()
    
    socket.on('new_review', (data) => {
        console.log('New review event received:', data);
        
        if (data.book === articleName.value) {
            console.log('New review for current book:', data);
            
            // Add the new review to the top of the list
            reviews.value.unshift({
                library_member: data.library_member,
                rating: data.rating,
                review: data.review,
                name: data.name
            });
        }
    });
})

const issueButtonClasses = computed(() => {
    return issueSuccess.value
        ? "opacity-0 cursor-not-allowed"
        : "opacity-100"
})

async function issueBook() {

    const url = `/api/method/library_management.api.issue_book?book=${articleName.value}`
    
    try {
        const response = await fetch(url, {
            credentials: 'include'
        })
        const data = await response.json();
        if (!data.message.success) {
            alert("You already requested this book!")
        }
    } catch(error) {
        console.error("Failed to issue the book: ", error)
        issueSuccess.value = false;
    }
}

function writeReview() {
    popup.value = !popup.value
}

function cancelWriteReview() {
    popup.value = !popup.value;
    customerRating.value = 0;
    customerReview.value = "";
}

async function sendReview() {
    
    try {
        const url = `/api/method/library_management.api.write_review?book=${articleName.value}&rating=${customerRating.value}&review=${customerReview.value}`

        const response = await fetch(url, {
            credentials: 'include',
            method: 'POST'
        })

        const data = await response.json();

        if(data.message.success) {
            popup.value = !popup.value
        } else {
            alert(data.message.message)
            popup.value = !popup.value
        }
    } catch(error) {
        console.error("Failed to write review. ", error)
        alert("Failed to write review!")
        popup.value = !popup.value
    }
}

async function fetchBookReviews() {
 // Get reviews
    try {
        const url = `/api/method/library_management.api.get_reviews?book=${articleName.value}`

        const response = await fetch(url, {
            credentials: 'include',
            method: 'POST'
        })
        const data = await response.json();

        reviews.value = data.message;
    } catch(error) {
        console.error("Failed to fetch book reviews: ", error)
    }
}

</script>