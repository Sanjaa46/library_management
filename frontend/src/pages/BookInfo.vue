<template>
<Header></Header>

<div class="w-[1120px] my-8 mx-auto text-[24px] font-bold relative">
    <div class="absolute w-1 h-12 bg-[#118ab2] left-0"></div>
    <h1 class="text-4xl font-bold pl-5 pt-2">Book Info</h1>
</div>

<section  class="flex w-[1120px] p-[30px] mx-auto my-10">
    <!-- Book image and Author -->
    <div class="flex flex-col w-[20%] items-center justify-center">
        <img src="../assets/images/richpoor.jpeg" class="w-[200px] h-[300px] object-contain rounded-[5px]" alt="book image">
        <p class="text-center mt-5">Rober T. Kiyosaki</p>
    </div>

    <!-- Book information -->
    <div class="w-[80%] ml-10">
        <h1 class="text-[25px] font-medium">Rich Dad Poor Dad</h1>
        <div class="flex my-5 space-x-5 text-[15px]">
            <p><b>Author: </b>Robert</p>
            <p><b>Publisher: </b>James Clear</p>
            <p><b>ISBN: </b>ISBN-01</p>
            <p><b>Status: </b>Available</p>
        </div>
        <h1 class="text-[18px] font-medium">Description</h1>
        <p>
            Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
        </p>
        <Button variant="solid" class="bg-[#1290b9] w-[90px] text-white my-10 rounded hover:bg-[#016475] transition">
        Issue
        </Button>
    </div>
</section>

<Footer></Footer>
</template>


<script setup>
import Header from '../assets/components/Header.vue';
import Footer from '../assets/components/Footer.vue';

</script>