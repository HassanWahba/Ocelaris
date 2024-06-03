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
    <table-meta v-if="tab === 'meta'" :info="metaInfo" :deletable="false" @delete="handleDelete"></table-meta>
    <table-preview v-else-if="tab === 'preview'" :headers="previewInfo.headers"
      :items="previewInfo.items"></table-preview>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: 'ViewTable',
  props: ['id'],
  data() {
    return {
      tab: 'meta',
    };
  },
  computed: {
    ...mapState("tables", ['tables']),
    metaInfo() {
      let table = this.tables.find(t => t.id === this.id)
      return table && table.meta ? this.extractProps(table.meta) : null;
    },
    previewInfo() {
      let table = this.tables.find(t => t.id === this.id);
      return table && table.preview ? table.preview : null;
    }
  },
  watch: {
    id() {
      if (!this.previewInfo) {
        this.fetchInfo(this.id);
      }
      this.tab = 'meta';
    }
  },
  methods: {
    fetchInfo(id) {
      let table = this.tables.find(t => t.id == id);
      if (!table || !table.preview) {
        this.$store.dispatch("tables/fetchViewInfo", { id: id });
        this.$emit('updated');
      }
    },
    handleDelete() {
      this.$emit('deleted', this.id)
    },
    extractProps(table) {
      let res = [
        { name: 'Name', value: table.name },
        { name: 'Owner', value: table.owner }
      ]
      if (table.metas) {
        for (let i = 0; i < table.metas.length; i++) {
          res.push({ name: 'Meta Table Name', value: table.metas[i].name })
        }
      }
      return res
    }
  }
}
</script>

<style scoped></style>