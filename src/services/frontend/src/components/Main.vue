<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      GCP Lab keeper helps you keep your lab projects in order.
    </p>
    <p>
      Below is the configuration set up for Lab Keeper.
    </p>
    <ProjectSelector />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";
import ProjectSelector from "@/components/ProjectSelector.vue";

@Component({
  components: {
    ProjectSelector
  }
})
export default class Main extends Vue {
  @Prop() private msg!: string;
}
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
