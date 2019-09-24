<template>
  <div id="project-selector">
    <form>
      <div class="form-row">
        <label for="projectSelector" class="col-sm-4 col-form-label"
          >Project:</label
        >
        <select
          v-model="selectedProject"
          class="form-control col-sm-6"
          id="projectSelector"
        >
          <option value selected disabled>Select project...</option>
          <option v-for="(item, index) in projectList" :key="index">{{
            item.name
          }}</option>
        </select>
      </div>
    </form>
  </div>
</template>

<script>
import { Credentials, GetProjectRequest } from "./project_manager_pb";
import { ProjectManagerClient } from "./project_manager_grpc_web_pb";
import Account from "../../assets/credentials.json";

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
      projectList: null,
      client: null,
      request: null,
      credentials: null,
      selectedProject: ""
    };
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
    }
  }
};
</script>
