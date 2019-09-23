<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      GCP Lab Keeper helps you maintain all you lab projects in order.
    </p>
    <project-selector />
  </div>
</template>

<script>
import ProjectSelector from "@/components/ProjectSelector/ProjectSelector.vue";

export default {
  name: "MainView",
  components: {
    ProjectSelector
  },
  props: {
    msg: String
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
