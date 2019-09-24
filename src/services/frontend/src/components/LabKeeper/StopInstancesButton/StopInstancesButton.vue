<template>
  <div>
    <b-button id="stopInstancesButton" variant="primary" @click="clicked">{{
      msg
    }}</b-button>
  </div>
</template>

<script>
export default {
  name: "StopInstancesButton",
  props: {
    msg: String
  },
  data: function() {
    return {};
  },
  methods: {
    clicked: function() {
      this.$emit("stopButtonClicked");
    }
  }
};
</script>
