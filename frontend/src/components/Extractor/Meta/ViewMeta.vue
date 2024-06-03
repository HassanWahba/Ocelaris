<template>
  <div>
    <div class="tabnav">
      <nav class="tabnav-tabs">
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'meta'"
          :aria-selected="tab === 'meta' ? 'true' : 'false'">Meta Data</button>
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'preview'"
          :aria-selected="tab === 'preview' ? 'true' : 'false'">Preview</button>
      </nav>
    </div>
    <div v-if="metaInfo && previewInfo">
      <table-meta v-if="tab === 'meta'" :info="metaInfo" :deletable="true" @delete="handleDelete"></table-meta>
      <table-preview v-else-if="tab === 'preview'" :headers="previewInfo.headers"
        :items="previewInfo.items"></table-preview>
    </div>
    <h2 v-else-if="id >= 0"><span>Loading</span><span class="AnimatedEllipsis"></span></h2>
  </div>
</template>

<script>
import { mapState, mapGetters } from "vuex";

export default {
  name: "ViewMeta",
  props: ['id'],
  data() {
    return {
      tab: 'meta',
      metas: [],
    };
  },
  computed: {
    ...mapGetters("meta", ['metaNames']),
    ...mapState("meta", ['metaTables', 'error']),
    metaInfo() {
      let metaTable = this.metaTables.find(t => t.id === this.id)
      return metaTable && metaTable.meta ? this.extractProps(metaTable.meta) : null;
    },
    previewInfo() {
      let metaTable = this.metaTables.find(t => t.id === this.id);
      if (!metaTable) {
        this.$notify.error('Meta table Not Found: ' + this.errorMessage)
      } else if (!metaTable.preview) {
        this.$notify.error('Meta table Preview Not Found: ' + this.errorMessage)
      } else if (!metaTable.preview.headers) {
        this.$notify.error('Meta table Preview Not Available: ' + metaTable.preview.message)
      }
      return metaTable && metaTable.preview ? metaTable.preview : null;
    }
  },
  methods: {
    handleDelete() {
      this.$store.dispatch('meta/removeMetaTable', { id: this.id })
        .then(res => {
          this.$notify.success("Meta table was deleted successfully.");
          this.$emit('deleted', this.id)
        })
        .catch(e => {
          this.$notify.error("The deletion failed: " + e);
        });
    },
    extractProps(tableMeta) {
      return [
        { name: 'Name', value: tableMeta.name },
        { name: 'Meta Table', value: tableMeta.source_table },
        { name: 'Tables\' Names', value: tableMeta.tables_column },
        { name: 'Tables\' Owners', value: tableMeta.owner_column },
        { name: 'Other Attributes', value: tableMeta.attributes },
        { name: 'Condition', value: tableMeta.condition },
      ]
    }
  }
}
</script>
<style scoped></style>