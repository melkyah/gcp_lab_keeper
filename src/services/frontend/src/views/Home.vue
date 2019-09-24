<template>
  <div class="home">
    <img alt="GCP Logo" src="../assets/Google-Cloud-Logo.png" height="250px" width="250px" />
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
