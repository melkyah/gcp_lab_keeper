<template>
  <div class="home">
    <img
      alt="GCP Logo"
      src="../assets/Google-Cloud-Logo.png"
      height="50%"
      width="50%"
    />
    <main-view msg="GCP Lab Keeper" />
  </div>
</template>

<script>
// @ is an alias to /src
import MainView from "@/components/MainView.vue";

export default {
  name: "home",
  components: {
    MainView
  }
};
</script>
