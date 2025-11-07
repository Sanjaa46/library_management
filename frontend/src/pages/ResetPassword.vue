<template>
  <div class="max-w-[100%] m-3 grid grid-cols-1 h-screen">
    <Card title="Login to your FrappeUI App!" class="w-full max-w-md m-auto bg-[#f7f4f0] z-10 px-12 py-10 rounded-xl shadow-lg">
        <h2 class="text-3xl font-medium text-center ">Reset Password</h2>
        <form class="flex flex-col space-y-5 w-full" @submit.prevent="resetPassword">
            <Input
            required
            v-model="newPassword"
            name="password"
            type="password"
            placeholder="New password"
            class="h-10 my-3"
            />
            <Button variant="solid" class="bg-[#007C91] text-white py-2 rounded hover:bg-[#006273] transition">
                Reset Password
            </Button>
        </form>
    </Card>
</div>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();

const newPassword = ref("")
const resetToken = ref("")

onMounted(async () => {
    resetToken.value = route.query.token;

    if(!resetToken.value){
        alert("Reset password token not found!")
        router.replace("/frontend/account/login")
    }
})

async function resetPassword() {
    try {
        const url = `/api/method/library_management.api.reset_password?token=${resetToken.value}&new_password=${newPassword.value}`

        const response = await fetch(url, {
            method: 'POST'
        })
        const data = await response.json();
        console.log(data.message.message)
        if(data.message.success) {
            alert(data.message.message)
            router.replace("/frontend/account/login")
        } else {
            alert(data.message.message)
            router.replace("/frontend/account/login")
        }

    } catch(error) {
        alert("Failed to reset password!")
        router.replace("/frontend/account/login")
    }
}



</script>