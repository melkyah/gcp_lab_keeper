<template>
  <div class="hello">
    <b-container fluid class="bv-example-row">
      <b-row>
        <b-col>
          <h1>{{ msg }}</h1>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <p>
            GCP Lab Keeper helps you maintain all you lab projects in order.
          </p>
        </b-col>
      </b-row>
    </b-container>
    <b-container>
      <b-card bg-variant="light" header="Try me" class="text-center">
        <b-row>
          <b-col>
            <project-selector @projectChanged="projectChanged" />
          </b-col>
        </b-row>
        <b-row class="mt-4">
          <b-col>
            <stop-instances-button
              msg="Stop VMs"
              v-bind:project="selectedProject"
            />
          </b-col>
        </b-row>
      </b-card>
    </b-container>
  </div>
</template>

<script>
import ProjectSelector from "@/components/ProjectSelector/ProjectSelector.vue";
import StopInstancesButton from "@/components/StopInstancesButton/StopInstancesButton.vue";

export default {
  name: "MainView",
  components: {
    ProjectSelector,
    StopInstancesButton
  },
  data: function() {
    return {
      selectedProject: ""
    };
  },
  props: {
    msg: String
  },
  methods: {
    /**
     * Updates selectedProject value when
     * projectSelector component triggers a
     * projectChanged event.
     */
    projectChanged: function(value) {
      this.selectedProject = value;
    }
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
