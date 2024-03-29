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
          <p>GCP Lab Keeper helps you maintain all you lab projects in order.</p>
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
            <stop-instances-button msg="Stop VMs" @stopButtonClicked="stopVMs" />
          </b-col>
        </b-row>
      </b-card>
    </b-container>
  </div>
</template>

<script>
import ProjectSelector from "@/components/LabKeeper/ProjectSelector/ProjectSelector.vue";
import StopInstancesButton from "@/components/LabKeeper/StopInstancesButton/StopInstancesButton.vue";
import {
  StopInstanceRequest,
  Credentials,
  Project,
  ZonePrefixes
} from "./instance_manager_pb";
import { InstanceManagerClient } from "./instance_manager_grpc_web_pb";
import Account from "../../assets/credentials.json";

export default {
  name: "LabKeeper",
  components: {
    ProjectSelector,
    StopInstancesButton
  },
  data: function() {
    return {
      instanceManagerHost: "localhost",
      instanceManagerPort: "8090",
      selectedProject: "",
      stoppedVMs: []
    };
  },
  props: {
    msg: String
  },
  // Create client on component creation
  created: function() {
    this.client = new InstanceManagerClient(
      `http://${this.instanceManagerHost}:${this.instanceManagerPort}`,
      null,
      null
    );
  },
  methods: {
    /**
     * Updates selectedProject value when
     * projectSelector component triggers a
     * projectChanged event.
     */
    projectChanged: function(value) {
      this.selectedProject = value;
    },
    /**
     * Stop VMs running in the selected
     * GCP project.
     */
    stopVMs: function() {
      if (this.selectedProject) {
        let request = new StopInstanceRequest();
        let credentials = new Credentials();
        let project = new Project();
        let targetZones = new ZonePrefixes();
        credentials.setCredentials(JSON.stringify(Account));
        project.setProjectId(this.selectedProject);
        targetZones.setPrefixesList(["us"]);
        request.setCredentials(credentials);
        request.setProject(project);
        request.setZones(targetZones);
        this.client.stopInstances(request, {}, (err, response) => {
          this.stoppedVMs = response.toObject().instancesList;
        });
        console.log(this.selectedProject);
      } else {
        console.log("No project selected.");
      }
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
