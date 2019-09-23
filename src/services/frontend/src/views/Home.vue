<template>
  <div class="home">
    <img alt="GCP Logo" src="../assets/gcp_logo.png" height="25%" width="25%" />
    <Main msg="GCP Lab Keeper" />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Main from "@/components/Main.vue"; // @ is an alias to /src

@Component({
  components: {
    Main
  }
})
export default class Home extends Vue {}
</script>
