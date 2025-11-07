<template>
    <Header></Header>

    <div class="w-[1120px] my-8 mx-auto text-[24px] font-bold relative">
        <div class="absolute w-1 h-12 bg-[#118ab2] left-0"></div>
        <h1 class="text-4xl font-bold pl-5 pt-2">Membership Success</h1>
    </div>

    <section class="flex flex-col items-center justify-center max-w-[1120px] h-[600px] mx-auto my-15 ">
        <img src="../assets/images/success.png" class="w-[400px] h-[400px]" alt="Membership Success">
        <h2 class="text-2xl font-bold mt-[30px]">Thank you for your membership!</h2>
        <p class="text-lg">You can now access library resources.</p>
        <Button variant="solid" class="bg-[#118ab2] hover:bg-[#016475] text-white-overlay-900 rounded-[10px] w-[200px] h-[40px] mt-[30px]" @click="goToLibrary">
            Go to Library
        </Button>
    </section>

    <Footer></Footer>
</template>

<script setup>
import Header from '../assets/components/Header.vue';
import Footer from '../assets/components/Footer.vue';
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();

const sessionId = ref("");
const isVerifying = ref(false);
const verificationError = ref("");

onMounted(() => {
    // Extract sessionId from url
    sessionId.value = route.query.session_id;

    if (sessionId.value) {
        verifyPaymentSession(sessionId.value);
    } else {
        console.error("No session ID found");
    }
})

async function verifyPaymentSession(sessionId) {
    isVerifying.value = true;

    try {
        const response = await fetch(`/api/method/library_management.api.verify_checkout_session?session_id=${sessionId.value}`, {
            credentials: 'include',
            method: 'GET'
        });
        const data = await response.json();

        if (data.message && data.message.verified) {
            console.log("Payment verified");
        }
    } catch (error) {
        verificationError.value = 'Could not verify payment. Please contact support.';
        console.error('verification error: ', error);
    } finally {
        isVerifying.value = false;
    }
}

function goToLibrary() {
    router.push('/frontend');
}

</script>