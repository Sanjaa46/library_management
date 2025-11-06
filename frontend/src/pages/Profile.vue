<template>
    <Header></Header>
    <div class="w-[1120px] my-8 mx-auto text-[24px] font-bold relative">
        <div class="absolute w-1 h-12 bg-[#118ab2] left-0"></div>
        <h1 class="text-4xl font-bold pl-5 pt-2">Profile</h1>
    </div>
    <section class="flex max-w-[1120px] h-[550px] mx-auto my-15">
        <!-- Pro Image, Fullname and three buttons -->
        <div class=" w-[30%]">
            <a @click="current = 'ProfileInfo'">
                <div class="w-[250px] h-[250px] mx-auto my-5 p-[7px] border-[3px] border-[#118ab2] rounded-full">
                    <img class="m-auto w-[235px] h-[235px] object-fill rounded-[50%]" src="../assets/images/testpro.jpeg" alt="profile image">
                </div>
            </a>
            <p class="w-[50%] m-auto text-center text-[20px] font-bold">{{ first_name + " " + last_name }}</p>
            <div 
                :class='["w-[30%] m-auto rounded-full italic text-[10px]", statusClasses]'
            >
                <p class="text-center"><b>Status:</b> {{ statusText }}</p>
            </div>

            <!-- Buttons -->
            <div class="flex flex-col items-center space-y-3 mt-5">
                <button 
                    @click="createCheckoutSession"
                    :class='[" w-[215px] h-[35px] mt-5 bg-[#118ab2] hover:bg-[#016475] text-white-overlay-900 rounded-[10px]", buyButtonClasses]'
                >
                    Buy Membership
                </button>
                <button @click="current = 'ChangePassword'">
                    Change Password >
                </button>
                <button @click="current = 'MyBooks'">
                    My Books >
                </button>
            </div>
        </div>

        <!-- Line -->
        <div class="relative h-[475px] w-1 bg-[#118ab2] left-[-1px] top-[20px]"></div>
        
        <!-- Info, Change Password and My Books -->
        <div class="w-[70%]">
            <component :is="currentComponent" :user="user" />
        </div>

    </section>
    <Footer></Footer>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import Header from '../assets/components/Header.vue';
import Footer from '../assets/components/Footer.vue';
import ProfileInfo from '../assets/components/ProfileInfo.vue';
import MyBooks from '../assets/components/MyBooks.vue';
import ChangePassword from '../assets/components/ChangePassword.vue';

const componentsMap = {
    ProfileInfo,
    ChangePassword,
    MyBooks
}

const current = ref('ProfileInfo')

const currentComponent = computed(() => componentsMap[current.value])

const user = ref({})
const first_name = ref("John");
const last_name = ref("Doe");
const membership = ref(false)
const checkoutUrl = ref("")

const statusText = computed(() => {
    return membership.value ? "Membership" : "Nonmembership"
})

const statusClasses = computed(() => {
    return membership.value 
        ? "text-green-700 bg-green-300" 
        : "text-red-700 bg-red-300"
})

const buyButtonClasses = computed(() => {
    return membership.value
        ? "opacity-0"
        : "opacity-100"
})

onMounted(async () => {
    try {
        const response = await fetch('/api/method/library_management.api.profile', {
            credentials: 'include',
            method: 'GET',
            headers: { "Content-Type": "application/json" }
        });
        const data = await response.json();

        first_name.value = data.message.first_name;
        last_name.value = data.message.last_name;
        membership.value = data.message.membership;

        user.value = {
            id: data.message.id,
            first_name: data.message.first_name,
            last_name: data.message.last_name,
            phone: data.message.phone,
            email: data.message.email
        }
    } catch (error) {
        console.error('Failed to fetch user info:', error);
    }
});

async function createCheckoutSession() {

    const url = `/api/method/library_management.api.create_checkout_session`;

    const response = await fetch(url, {
        credentials: 'include',
        method: 'POST'
    })
    const data = await response.json();
    console.log(data)

    checkoutUrl.value = data.message.url
    window.location.href = checkoutUrl.value

}

</script>