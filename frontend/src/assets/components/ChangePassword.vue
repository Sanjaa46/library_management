<template>

<div class="pl-[30px]">
    <Card title="Login to your FrappeUI App!" class=" z-10  rounded-xl">
    <h2 class="text-[30px] font-bold mb-8">Change Password</h2>
    <form class=" space-y-5 " @submit.prevent="submit">
        <Input
        required
        v-model="current_password"
        name="current"
        type="password"
        placeholder="Current password"
        class="w-[300px]"
        />
        <Input
        required
        v-model="new_password"
        name="password"
        type="password"
        class="w-[300px]"
        placeholder="New password"
        />
        <Input
        required
        v-model="re_enter_new_password"
        name="password"
        type="password"
        class="w-[300px]"
        placeholder="Re-enter new password"
        />
        <Button @click="handleChangePassword" variant="solid" class="bg-[#1290b9] text-white py-2 rounded hover:bg-[#016475] transition">
        Chnage Password
        </Button>
    </form>
    </Card>
</div>

</template>


<script setup>
import { ref } from 'vue'

const current_password = ref("");
const new_password = ref("");
const re_enter_new_password = ref("");

async function handleChangePassword() {
    if (current_password.value === new_password.value) {
        alert("New password must be different!")
        return
    }
    
    if (new_password.value !== re_enter_new_password.value) {
        alert("Password did not match!")
        return
    }

    try {
        const url = `/api/method/library_management.api.change_password`

        const response = await fetch(url, {
            credentials: 'include',
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                old_password: current_password.value,
                new_password: new_password.value,
            })
        })
        const data = await response.json()

        if (data.message.Success) {
            alert("Password changed succesfully!")
        } else {
            console.log(data)
            alert("Old password is incorrect!")
        }

    } catch (error) {
        console.log("Change password failed: ", error)
        console.error('Error details:', {
            name: error.name,
            message: error.message,
            stack: error.stack
        })
        alert('Change password failed. Please check console for details.')
    }
}

</script>