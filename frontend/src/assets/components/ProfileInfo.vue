<template>

<div>
    <h1 class=" pl-[20px] pb-[20px] text-[30px] font-bold">Info</h1>
    <ul class=" pl-[20px] space-y-4">
        <li>
            <p class=" text-black-overlay-500">ID</p>
            <p>{{ props.user.id }}</p>
        </li>
        <li>
            <p class=" text-black-overlay-500">Firstname</p>
            <p>{{ props.user.first_name }}</p>
        </li>
        <li>
            <p class=" text-black-overlay-500">Lastname</p>
            <p>{{ props.user.last_name }}</p>
        </li>
        <li>
            <p class=" text-black-overlay-500">Email</p>
            <p>{{ props.user.email }}</p>
        </li>
        <li>
            <p class=" text-black-overlay-500">Phone</p>
            <p>{{ props.user.phone }}</p>
        </li>
    </ul>
</div>

</template>


<script setup>
import { ref, onMounted } from 'vue';

const props = defineProps({
  user: {
    type: Object,
    required: true
  }
});

</script>