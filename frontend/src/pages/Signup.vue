<template>
  <div class="m-3 grid grid-cols-2 h-screen">
    <!-- LEFT SIDE: Shapes -->
    <div class="relative overflow-hidden -m-10">
      <div class="bg-[#2C3E50] w-[100%] h-[120%] absolute top-[-200px] right-[-0px] rotate-[12deg] origin-top-right rounded-tl-[20px]"></div>

      <div class="bg-[#254B71] w-[105%] h-[50%] absolute bottom-[-150px] right-[100px] rotate-[15deg] origin-bottom-left rounded-[20px]"></div>

      <div class="bg-[#577592] w-[85%] h-[60%] absolute top-[-380px] right-[48px] rotate-[-12deg] rounded-[20px]"></div>
    </div> 

    <!-- RIGHT SIDE -->
    <div class="flex items-center justify-center">
      <Card title="Login to your FrappeUI App!" class="w-full max-w-md bg-[#f7f4f0] z-10 px-12 py-10 rounded-xl shadow-lg">
        <h2 class="text-xl font-medium text-center mb-8">Sign Up</h2>
        <form class="flex flex-col space-y-5 w-full" @submit.prevent="submit">
          <Input
            required
            v-model="first_name"
            name="first_name"
            type="text"
            placeholder="First name"
          />
          <Input
            required
            v-model="last_name"
            name="last_name"
            type="text"
            placeholder="Last name"
          />
          <Input
            required
            v-model="username"
            name="username"
            type="text"
            placeholder="User name"
          />
          <Input
            required
            v-model="email"
            name="email"
            type="text"
            placeholder="Email"
          />
          <Input
            required
            v-model="phone"
            name="phone"
            type="number"
            placeholder="Phone"
          />
          <Input
            required
            v-model="password"
            name="password"
            type="password"
            placeholder="Password"
          />
          <Input
            required
            v-model="re_password"
            name="re-password"
            type="password"
            placeholder="Re-enter Password"
          />
          <Button @click="handleSignup" variant="solid" class="bg-[#007C91] text-white py-2 rounded hover:bg-[#006273] transition">
            Sign up
          </Button>
        </form>
        <div class="text-center mt-6 text-sm">
          <a href="/account/login" class="text-blue-600 hover:underline">
            Sign in
          </a>
        </div>
      </Card>
    </div>
  </div>


</template>

<script setup>
import { ref } from 'vue';

const first_name = ref("")
const last_name = ref("")
const username = ref("")
const email = ref("")
const phone = ref("")
const password = ref("")
const re_password = ref("")



async function handleSignup() {
  if (password.value !== re_password.value) {
    alert('Passwords do not match!')
    return
  }

  if (!password.value || password.value.length < 8) {
    alert('Password must be at least 8 characters')
    return
  }

  console.log('Email:', email.value)
  console.log('Timestamp:', new Date().toISOString())
  
  try {
    const response = await fetch('http://localhost:8000/api/method/library_management.auth.signup_user', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', },
      body: JSON.stringify({
        first_name: first_name.value,
        last_name: last_name.value,
        email: email.value,
        phone: phone.value,
        password: password.value,
      })
    })
    
    console.log('Response Status:', response.status)
    console.log('Response OK:', response.ok)
    
    const data = await response.json()
    console.log('Response Data:', data)

    if (data.message && data.message.success === true) {
      alert('Signup successful!')
    } else {
      console.error('Signup failed')
      console.error('Response structure:', JSON.stringify(data, null, 2))
    }
  } catch (error) {
    console.error('Signup error occurred:', error)
    console.error('Error details:', {
      name: error.name,
      message: error.message,
      stack: error.stack
    })
    alert('Signup failed. Please check console for details.')
  }
}

</script>