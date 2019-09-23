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
export default {
  name: "ProjectSelector",
  props: {
    msg: String
  }
};
</script>
