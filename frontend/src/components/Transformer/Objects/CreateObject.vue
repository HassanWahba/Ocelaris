<template>
  <div>
    <div class="tabnav">
      <nav class="tabnav-tabs">
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'sql'"
          :aria-selected="tab === 'sql' ? 'true' : 'false'">Create with SQL</button>
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'graphical'"
          :aria-selected="tab === 'graphical' ? 'true' : 'false'">Graphical</button>
      </nav>
    </div>

    <create-sql v-if="tab === 'sql'" :id="-1" @created="handleCreated"></create-sql>
    <graphical-object v-if="tab === 'graphical'" @created="handleCreated"></graphical-object>

  </div>
</template>

<script>
export default {
  name: "CreateObject",
  props: ['id'],
  data() {
    return {
      tab: 'sql',
    };
  },
  methods: {
    handleCreated(id) {
      this.$emit('created', id);
    }
  }
}
</script>

<style scoped></style>
