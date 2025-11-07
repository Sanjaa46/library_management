<template>
  <div class="max-w-[100%] m-3 grid grid-cols-2 h-screen">
    <!-- LEFT SIDE -->
    <div class="flex items-center justify-center">
      <Card title="Login to your FrappeUI App!" class="w-full max-w-md bg-[#f7f4f0] z-10 px-12 py-10 rounded-xl shadow-lg">
        <h2 class="text-xl font-medium text-center mb-8">Sign In</h2>
        <form class="flex flex-col space-y-5 w-full" @submit.prevent="submit">
          <Input
            required
            v-model="email"
            name="email"
            type="text"
            placeholder="Email"
          />
          <Input
            required
            v-model="password"
            name="password"
            type="password"
            placeholder="Password"
          />
          <a href="/frontend/forgot-password" class="text-sm text-right text-gray-500 cursor-pointer hover:underline">
            Forgot password?
          </a>
          <Button :locading="session.login.loading" variant="solid" class="bg-[#007C91] text-white py-2 rounded hover:bg-[#006273] transition">
            Login
          </Button>
        </form>
        <div class="text-center mt-6 text-sm">
          Don't have an account?
          <a href="/frontend/account/signup" class="text-blue-600 hover:underline">
            Sign up
          </a>
        </div>
      </Card>
    </div>

    <!-- RIGHT SIDE: Shapes -->
    <div class="relative overflow-hidden -m-10">
      <div class="bg-[#2C3E50] w-[100%] h-[120%] absolute -top-20 right-[-100px] -rotate-12 origin-top-right rounded-tl-[20px]"></div>

      <div class="bg-[#254B71] w-[150%] h-[150%] absolute bottom-[8px] right-[-400px] rotate-[60deg] origin-bottom-left"></div>

      <div class="bg-[#577592] w-[85%] h-[60%] absolute top-[-380px] right-[40px] rotate-12 rounded-bl-[20px] rounded-br-[20px]"></div>
    </div> 
  </div>


</template>

<script setup>
import { session } from '../data/session'

// Session-based Authentication
function submit(e) {
  const formData = new FormData(e.target)
	session.login.submit({
    email: formData.get("email"),
		password: formData.get("password"),
	})
}


// Toke-based Authentication
import { ref } from 'vue';

const email = ref('')
const password = ref('')
const userType = ref('member')



async function handleLogin() {
  if (userType.value === 'member') {
    await loginLibraryMember()
  } else {
    await loginStaff()
  }
}

async function loginLibraryMember() {
  console.log('Email:', email.value)
  console.log('Timestamp:', new Date().toISOString())
  
  try {
    const response = await fetch('http://localhost:8000/api/method/library_management.auth.login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', },
      body: JSON.stringify({
        email: email.value,
        password: password.value,
      })
    })
    
    console.log('Response loginLibraryMember Status:', response.status)
    console.log('Response OK:', response.ok)
    
    const data = await response.json()
    console.log('Response Data:', data)

    if (data.message && data.message.access_token) {
      localStorage.setItem('library_token', data.message.access_token)
      console.log('Token saved successfully to local storage')
      console.log('Token:', data.message.access_token.substring(0, 20) + '...')
      alert('Login successful!')
    } else {
      console.error('Login failed - No access token in response')
      console.error('Response structure:', JSON.stringify(data, null, 2))
      alert('Invalid Member login')
    }
  } catch (error) {
    console.error('Login error occurred:', error)
    console.error('Error details:', {
      name: error.name,
      message: error.message,
      stack: error.stack
    })
    alert('Login failed. Please check console for details.')
  }
  
}

async function loginStaff() {
  try {
    alert("Hello")
    const response = await fetch('/api/method/login', {
      method: 'POST',
      headers: { 'Content-type': 'application/json' },
      body: JSON.stringify({
        usr: email.value,
        pwd: password.value,
      })
    })
    const data = await response.json()
    if (data.message === 'Logged In') {
      window.location.href = '/app'
    } else {
      alert("Invalid staff login")
    }
  } catch (error) {
    console.error('Login error occurred:', error)
    console.error('Error details:', {
      name: error.name,
      message: error.message,
      stack: error.stack
    })
    alert('Login failed. Please check console for details.')
  }


}


</script>
