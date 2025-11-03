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
            name="first_name"
            type="text"
            placeholder="First name"
          />
          <Input
            required
            name="last_name"
            type="text"
            placeholder="Last name"
          />
          <Input
            required
            name="username"
            type="text"
            placeholder="User name"
          />
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
          <Input
            required
            name="re-password"
            type="password"
            placeholder="Re-enter Password"
          />
          <Button variant="solid" class="bg-[#007C91] text-white py-2 rounded hover:bg-[#006273] transition">
            Login
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
</script>