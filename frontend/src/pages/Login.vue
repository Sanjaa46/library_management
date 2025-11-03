<template>
  <div class="max-w-[100%] m-3 grid grid-cols-2 h-screen">
    <!-- LEFT SIDE -->
    <div class="flex items-center justify-center">
      <Card title="Login to your FrappeUI App!" class="w-full max-w-md bg-[#f7f4f0] z-10 px-12 py-10 rounded-xl shadow-lg">
        <h2 class="text-xl font-medium text-center mb-8">Sign In</h2>
        <form class="flex flex-col space-y-5 w-full" @submit.prevent="submit">
          <Input
            required
            name="email"
            type="text"
            placeholder="Email"
          />
          <Input
            required
            name="password"
            type="password"
            placeholder="Password"
          />
          <div class="text-sm text-right text-gray-500 cursor-pointer hover:underline">
            Forgot password?
          </div>
          <Button :loading="session.login.loading" variant="solid" class="bg-[#007C91] text-white py-2 rounded hover:bg-[#006273] transition">
            Login
          </Button>
        </form>
        <div class="text-center mt-6 text-sm">
          Don't have an account?
          <a href="/account/signup" class="text-blue-600 hover:underline">
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

<script lang="ts" setup>
import { session } from "../data/session"

function submit(e) {
	const formData = new FormData(e.target)
	session.login.submit({
		email: formData.get("email"),
		password: formData.get("password"),
	})
}
</script>
