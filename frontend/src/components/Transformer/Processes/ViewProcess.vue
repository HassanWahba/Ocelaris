<template>
  <div>
    <div class="tabnav">
      <nav class="tabnav-tabs">
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'meta'"
          :aria-selected="tab === 'meta' ? 'true' : 'false'">Meta Data</button>
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'modify'"
          :aria-selected="tab === 'modify' ? 'true' : 'false'">Modify</button>
      </nav>
    </div>
    <table-meta v-if="tab === 'meta'" :info="metaInfo" :deletable="true" @delete="handleDelete"></table-meta>
    <create-process v-else-if="tab === 'modify'" @modify="handleModified" :id="process.id" :name="process.meta.name"
      :p_objects="process.meta.objects"></create-process>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "ViewProcess",
  props: ['id'],
  data() {
    return {
      tab: 'meta'
    };
  },
  computed: {
    ...mapState("processes", ['processes']),
    process() {
      return this.processes.find(t => t.id == this.id)
    },
    metaInfo() {
      let table = this.processes.find(t => t.id == this.id)
      return table && table.meta ? this.extractProps(table.meta) : null;
    },
    previewInfo() {
      let table = this.processes.find(t => t.id == this.id);
      return table && table.preview ? table.preview : null;
    }
  },
  methods: {
    handleDelete() {
      this.$store.dispatch("processes/removeProcess", { id: this.id })
        .then(() => {
          this.$emit('deleted');
        })
        .catch(e => {
          this.$notify.error("The deletion failed: " + e);
        });
    },
    handleModified() {
      this.$emit('updated')
    },
    extractProps(object) {
      let objs = []
      if (object.objects) {
        for (let i = 0; i < object.objects.length; i++) {
          objs.push({ name: 'Object_' + i, value: object.objects[i].name })
        }
      }
      return [
        { name: 'Name', value: object.name },
        ...objs
      ]
    }
  }
}
</script>

<style scoped></style>
