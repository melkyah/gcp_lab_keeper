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
import {grpc, BrowserHeaders} from "grpc-web-client";

export default {
  name: "ProjectSelector",
  props: {
    msg: String
  },
  data: function(){
      return {
          projectManagerHost: "localhost",
          projectManagerPort: "8090",
          credPath: "../../assets/credentials.json",
          projectList: [],
          client: null
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
      getProjects: function(credFile){
          let credentials = new Credentials();
          let request = new GetProjectRequest();
          credentials.setCredentials(credFile);
          request.setCredentials = credentials;
        
          this.client.getProjects(request, function(error, result) {
            if (error) console.log('Error: ', error);
            else console.log(result.toObject());
          });
      },
  }
}
</script>