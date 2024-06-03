<template>
  <div>
    <h3>Meta Information</h3>
    <dl style="padding: 20px">
      <div v-for="(item, index) in info" :key="index">
        <dt>{{ item.name }}:</dt>
        <dd style="white-space: pre-wrap;">{{ item.value || "None" }}</dd>
      </div>
    </dl>
    <button v-if="deletable" @click="$emit('delete');" class="btn btn-danger">
      <i class="far fa-trash-alt"></i> Delete
    </button>
  </div>
</template>

<script>
export default {
  props: ["deletable", "info"],
};
</script>

<style scoped>
h3 {
  font-size: 1.2em;
  margin-bottom: 0.5em;
}

dl {
  margin-left: 1em;
}

dt {
  font-weight: bold;
}

dd {
  margin-bottom: 0.5em;
}
</style>
