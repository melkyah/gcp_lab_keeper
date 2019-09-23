<template>
  <dir>
    <form>
      <div class="form-group row">
        <label for="projectSelector" class="col-sm-2 col-form-label"
          >Project</label
        >
        <div class="col-sm-10">
          <select
            class="form-control"
            type="text"
            placeholder="Project ID"
            id="projectSelector"
          >
            <option>1</option>
            <option>2</option>
            <option>3</option>
            <option>4</option>
            <option>5</option>
          </select>
        </div>
      </div>
    </form>
  </dir>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class ProjectSelector extends Vue {
  @Prop() private msg!: string;
}
</script>
