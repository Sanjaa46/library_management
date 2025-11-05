<template>

<div class="pl-[30px]">
    <Card title="Login to your FrappeUI App!" class=" z-10  rounded-xl">
    <h2 class="text-[30px] font-bold mb-8">Change Password</h2>
    <form class=" space-y-5 " @submit.prevent="submit">
        <Input
        required
        name="current"
        type="password"
        placeholder="Current password"
        class="w-[300px]"
        />
        <Input
        required
        name="password"
        type="password"
        class="w-[300px]"
        placeholder="New password"
        />
        <Input
        required
        name="password"
        type="password"
        class="w-[300px]"
        placeholder="Re-enter new password"
        />
        <div class="text-sm text-gray-500 cursor-pointer hover:underline">
        Forgot password?
        </div>
        <Button variant="solid" class="bg-[#1290b9] text-white py-2 rounded hover:bg-[#016475] transition">
        Chnage Password
        </Button>
    </form>
    </Card>
</div>

</template>


<script setup></script>