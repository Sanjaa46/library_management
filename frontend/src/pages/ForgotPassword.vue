<template>
  <div class="max-w-[100%] m-3 grid grid-cols-1 h-screen">
    <Card title="Login to your FrappeUI App!" class="w-full max-w-md m-auto bg-[#f7f4f0] z-10 px-12 py-10 rounded-xl shadow-lg">
        <h2 class="text-3xl font-medium text-center">Forgot Password?</h2>
        <div class="text-sm text-center text-gray-500 my-3 hover:underline">
            No worries, we will send you reset link.
        </div>
        <form class="flex flex-col space-y-5 w-full" @submit.prevent="sendResetLink">
            <Input
            required
            v-model="email"
            name="email"
            type="text"
            placeholder="Email"
            />
            <a href="/frontend/account/login" class="text-sm text-center text-gray-500 cursor-pointer hover:underline">
                Back to log in
            </a>
            <Button variant="solid" class="bg-[#007C91] text-white py-2 rounded hover:bg-[#006273] transition">
                Reset Password
            </Button>
        </form>
    </Card>
</div>

</template>


<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

const email = ref("")

async function sendResetLink() {
    if (!email.value) {
        alert("Email is required!")
        return
    }

    try {
        const url = `/api/method/library_management.api.forgot_password?email=${email.value}`

        const response = await fetch(url, {
            method: 'POST'
        })
        const data = await response.json();
        if(data.message.success) {
            alert("Reset link sent!")
            router.replace("/frontend/account/login")
        }
    } catch(error) {
        alert("User not found!");
    }
}

</script>