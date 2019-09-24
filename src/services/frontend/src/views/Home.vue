<template>
  <div class="home">
    <img
      alt="GCP Logo"
      src="../assets/Google-Cloud-Logo.png"
      width="250px"
      height="250px"
    />
    <lab-keeper msg="GCP Lab Keeper" />
  </div>
</template>

<script>
// @ is an alias to /src
import LabKeeper from "@/components/LabKeeper/LabKeeper.vue";

export default {
  name: "home",
  components: {
    LabKeeper
  }
};
</script>
