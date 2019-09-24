<template>
  <div id="project-selector">
    <b-form-group label="Project:">
      <select v-model="selectedProject" class="form-control" id="projectSelector">
        <option value selected disabled>-- Select project --</option>
        <option v-for="(item, index) in projectList" :key="index">{{ item.name }}</option>
      </select>
    </b-form-group>
    <b-form-group label="Zones:">
      <b-form-radio-group
        id="zone-group"
        v-model="selectedZone"
        :options="zoneList"
        name="zone-options"
        @click.prevent="checkZone"
      ></b-form-radio-group>
    </b-form-group>
  </div>
</template>

<script>
import { Credentials, GetProjectRequest } from "./project_manager_pb";
import { ProjectManagerClient } from "./project_manager_grpc_web_pb";
import Account from "../../../assets/credentials.json";

export default {
  name: "ProjectSelector",
  props: {
    msg: String
  },
  // Component parameters
  data: function() {
    return {
      projectManagerHost: "localhost",
      projectManagerPort: "8080",
      zoneList: [
        "us",
        "europe",
        "asia",
        "southamerica",
        "northamerica",
        "australia"
      ],
      selectedZone: "us",
      projectList: null,
      client: null,
      request: null,
      credentials: null,
      selectedProject: ""
    };
  },
  watch: {
    /**
     * This returns the selected project ID
     * to its parent component so that it can
     * be used in the button request.
     */
    selectedProject: function(value) {
      let project = this.projectList.find(function(element) {
        return element.name == value;
      });
      this.$emit("projectChanged", project.projectId);
    }
  },
  // This runs on component creation
  created: function() {
    this.client = new ProjectManagerClient(
      `http://${this.projectManagerHost}:${this.projectManagerPort}`,
      null,
      null
    );
    this.getProjects();
  },
  // Start method definitions
  methods: {
    /**
     * This function gets called on component creation.
     * Contacts the Project Manager server and gets
     * a list of active project for the user in the
     * service account used.
     */
    getProjects: function() {
      console.log("Starting request Projects function.");

      this.credentials = new Credentials();
      this.request = new GetProjectRequest();

      this.credentials.setCredentials(JSON.stringify(Account));
      this.request.setCredentials(this.credentials);

      this.client.getProjects(this.request, {}, (err, response) => {
        if (err) {
          console.log(err.code);
          console.log(err.message);
        } else {
          this.projectList = response.toObject().projectsList;
        }
      });
    },
    /**
     * Updates checked zone and emits to parent.
     */
    checkZone: function() {
      console.log("test");
      this.$emit("zoneSelected", this.selectedZone);
    }
  }
};
</script>
