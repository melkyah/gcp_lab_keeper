<template>
  <div>
    <b-button id="stopInstancesButton" variant="primary">{{ msg }}</b-button>
  </div>
</template>

<script>
export default {
  name: "StopInstancesButton",
  props: {
    msg: String,
    project: String
  },
  data: function() {
    return {};
  }
};
</script>
