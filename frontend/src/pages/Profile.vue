<template>
    <Header></Header>
    <div class="w-[1120px] my-8 mx-auto text-[24px] font-bold relative">
        <div class="absolute w-1 h-12 bg-gradient-to-b from-blue-500 to-purple-500 left-0"></div>
        <h1 class="text-4xl font-bold pl-5">Profile</h1>
    </div>
    <section class="flex max-w-[1120px] h-[550px] mx-auto my-15">
        <!-- Pro Image, Fullname and three buttons -->
        <div class=" w-[30%]">
            <div class="w-[250px] h-[250px] mx-auto my-5 p-[7px] border-[3px] border-[#118ab2] rounded-full">
                <img class="m-auto w-[235px] h-[235px] object-fill rounded-[50%]" src="../assets/images/testpro.jpeg" alt="profile image">
            </div>
            <p class="w-[50%] m-auto text-center text-[20px] font-bold">John Doe</p>
            <div class="w-[30%] m-auto bg-green-500 rounded-full italic text-[10px]">
                <p class=" text-center"><b>Status:</b> membership</p>
            </div>

            <!-- Buttons -->
            <div class="flex flex-col items-center space-y-3 mt-5">
                <button class=" w-[215px] h-[35px] mt-5 bg-[#118ab2] text-white-overlay-900 rounded-[10px]">Buy Membership</button>
                <button>
                    Change Password >
                </button>
                <button>
                    My Books >
                </button>
            </div>
        </div>

        <!-- Line -->
        <div class="relative h-[475px] w-1 bg-[#118ab2] left-[-1px] top-[20px]"></div>
        
        <!-- Info, Chnage Password and My Books -->
        <div class="w-[70%]">
            <ProfileInfo />
        </div>

    </section>
    <Footer></Footer>
</template>

<script setup>
import Header from '../assets/components/Header.vue';
import Footer from '../assets/components/Footer.vue';
import ProfileInfo from '../assets/components/ProfileInfo.vue';


</script>