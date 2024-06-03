<template>
  <div>
    <div class="tabnav">
      <nav class="tabnav-tabs">
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'meta'"
          :aria-selected="tab === 'meta' ? 'true' : 'false'">Meta Data</button>
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'mod'"
          :aria-selected="tab === 'mod' ? 'true' : 'false'">Modify</button>
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'preview'"
          :aria-selected="tab === 'preview' ? 'true' : 'false'">Preview</button>
      </nav>
    </div>
    <div v-if="metaInfo">
      <table-meta v-if="tab === 'meta'" :info="metaInfo" :deletable="true" @delete="handleDelete"></table-meta>
      <create-change-log v-else-if="tab === 'mod'" @change="handleCreated" :id="id" :name="log_meta.name"
        :owner="log_meta.owner" :table="log_meta.table" :condition="log_meta.condition"
        :timestamp="log_meta.event_timestamp" :targetTable="log_meta.event_target"
        :attributes="log_meta.attributes"></create-change-log>
      <table-preview v-else-if="tab === 'preview'" :headers="previewInfo.headers"
        :items="previewInfo.items"></table-preview>
    </div>
    <h2 v-else-if="id >= 0"><span>Loading</span><span class="AnimatedEllipsis"></span></h2>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "ViewChangeLog",
  props: ['id'],
  data() {
    return {
      tab: 'meta',
    };
  },
  computed: {
    ...mapState("log", ['logs', 'error']),
    metaInfo() {
      let table = this.logs.find(t => t.id === this.id)
      console.log(table)
      return table && table.meta ? this.extractProps(table.meta) : null;
    },
    log_meta() {
      return this.logs.find(t => t.id === this.id).meta
    },
    previewInfo() {
      let log = this.logs.find(t => t.id === this.id);
      if (!log) {
        this.$notify.error('Change log Not Found: ' + this.errorMessage)
      } else if (!log.preview) {
        this.$notify.error('Change log Preview Not Found: ' + this.errorMessage)
      } else if (!log.preview.headers) {
        this.$notify.error('Change log Preview Not Available: ' + log.preview.message)
      }
      return log && log.preview ? log.preview : null;
    }
  },
  watch: {
    error(newError) {
      if (newError) {
        this.errorMessage = newError.message;
        this.$notify.error('Error Occurred While Creating: ' + this.errorMessage)
      }
    }
  },
  methods: {
    async fetchInfo(id) {
      console.log("fetching info for " + id)
      let log = this.logs.find(t => t.id === id);
      if (!log) {
        this.$notify.error('Change log Not Found: ' + this.errorMessage)
      } else if (!log.preview) {
        this.$notify.error('Change log Preview Not Found: ' + this.errorMessage)
      } else if (!log.preview.headers) {
        this.$notify.error('Change log Preview Not Available: ' + this.errorMessage)
      }
    },
    handleCreated(id) {
      this.$emit('created', id);
      this.tab = 'meta'
    },
    handleDelete() {
      this.$store.dispatch('log/removeLog', { id: this.id })
        .then(res => {
          this.$notify.success("Change log was deleted successfully.");
          this.$emit('deleted', this.id)
        })
        .catch(e => {
          this.$notify.error("The deletion failed: " + e);
        });
    },
    extractProps(tableMeta) {
      return [
        { name: 'Name', value: tableMeta.name },
        { name: 'Owner', value: tableMeta.owner },
        { name: 'Table', value: tableMeta.table },
        { name: 'Timestamp Column', value: tableMeta.event_timestamp },
        { name: 'Document ID', value: tableMeta.event_target },
        { name: 'Other Attributes', value: tableMeta.attributes },
        { name: 'Condition', value: tableMeta.condition },
      ]
    }
  }
}
</script>
<style scoped></style>