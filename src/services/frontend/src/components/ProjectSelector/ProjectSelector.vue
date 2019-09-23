<template>
  <div id="project-selector">
    <form>
      <div class="form-row">
        <label for="projectSelector" class="col-sm-4 col-form-label">
          Project:
        </label>
        <select class="form-control col-sm-6" id="projectSelector">
          <option>1</option>
          <option>2</option>
          <option>3</option>
          <option>4</option>
          <option>5</option>
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
  data: function(){
      return {
          projectManagerHost: "localhost",
          projectManagerPort: "8080",
          credPath: "../../assets/credentials.json",
          projectList: [],
          client: null,
          request: null,
          credentials: null
      };
  },
  created: function(){
      this.client = new ProjectManagerClient(
          `http://${this.projectManagerHost}:${this.projectManagerPort}`, null, null
          );
      this.getProjects(this.credPath);
  },
  // Start method definitions
  methods: {
      getProjects: function(){

          console.log("Starting request Projects function.")
          console.log(Account)

          this.credentials = new Credentials();
          this.request = new GetProjectRequest();
          this.credentials.setCredentials(JSON.stringify(Account));
          this.request.setCredentials(this.credentials);

          console.log(this.request)
          console.log(this.credentials)
        
          this.client.getProjects(this.request, {}, function(err, response){
            console.log(response)
          })
      },
  }
}
</script>