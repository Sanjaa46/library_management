<template>

<section class="w-[600px] mx-auto my-[40px]" id="contact-us">
    <Card title="Contac us!" class=" z-10  rounded-xl">
        <h2 class="text-[30px] font-bold mb-8">Contact Us</h2>
        <form class=" space-y-5 " @submit.prevent="submit">
            <div class="flex w-full space-x-3">
                <Input
                required
                v-model="firstName"
                name="firstName"
                type="text"
                class="w-[50%]"
                placeholder="First name"
                />
                <Input
                required
                v-model="lastName"
                autocomplete="off"
                name="lastName"
                type="text"
                class="w-[50%]"
                placeholder="Last name"
                />
            </div>
            <Input
            required
            v-model="email"
            name="email"
            type="email"
            class=""
            placeholder="Email"
            />
            <textarea
            required
            v-model="message"
            name="message"
            type="text"
            class="h-[100px] w-full rounded-[10px]"
            placeholder="Message..."
            ></textarea>
            <Button @click="handleSendMessage" variant="solid" class="bg-[#1290b9] text-white py-2 rounded hover:bg-[#016475] transition">
                Submit
            </Button>
        </form>
    </Card>
</section>

</template>

<script setup>
import { ref } from 'vue';

const firstName = ref("");
const lastName = ref("");
const email = ref("");
const message = ref("");

async function handleSendMessage() {
    if(!firstName.value || !lastName.value || !email.value || !message.value) {
        alert("All fields are required!")
        return
    }

    const url = `/api/method/library_management.api.send_message?first_name=${firstName.value}&last_name=${lastName.value}&email_address=${email.value}&message=${message.value}`;

    try {
        const response = await fetch(url, {
            credentials: 'include',
            method: 'POST'
        })
        const data = await response.json()

        if(data.message.success) {
            firstName.value = "";
            lastName.value = "";
            email.value = "";
            message.value = "";
            alert(data.message.message)
        } else {
            alert(data.message.message)
        }
    } catch(error) {
        console.error("Failed to send message", error);
        alert("Failed to send message!")
    }
}

</script>