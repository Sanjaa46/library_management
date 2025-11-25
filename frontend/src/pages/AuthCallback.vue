<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const router = useRouter();

onMounted(async () => {
    const params = new URLSearchParams(window.location.search);
    const code = params.get("code");
    const state = params.get("state");
    console.log("Authorization code:", code);

    if (!code) {
        console.error("No authorization code found");
        return;
    }

    // try {
    //     // Exchange code for tokens
    //     const res = await axios.post("http://localhost:8001/token", {
    //         grant_type: "authorization_code",
    //         code,
    //         redirect_uri: "http://localhost:8080/callback",
    //         client_id: "vue_app",
    //     });

    //     const { access_token, refresh_token } = res.data;

    //     // Save tokens
    //     localStorage.setItem("access_token", access_token);
    //     localStorage.setItem("refresh_token", refresh_token);

    //     // Redirect to home page after login
    //     router.push("/");
    // } catch (err) {
    //     console.error("Token exchange failed", err);
    // }
});
</script>

<template>
  <div class="p-6 text-center text-lg">Logging you in...</div>
</template>
