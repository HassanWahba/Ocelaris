<template>
  <div>
    <div class="tabnav">
      <nav class="tabnav-tabs">
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'meta'"
          :aria-selected="tab === 'meta' ? 'true' : 'false'">Meta Data</button>
        <button v-if="isGraph" class="tabnav-tab" role="tab" type="button" @click="tab = 'graphical'"
          :aria-selected="tab === 'graphical' ? 'true' : 'false'">Graphical</button>
        <button v-else class="tabnav-tab" role="tab" type="button" @click="tab = 'sql'"
          :aria-selected="tab === 'sql' ? 'true' : 'false'">SQL</button>
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'preview'"
          :aria-selected="tab === 'preview' ? 'true' : 'false'">Preview</button>
      </nav>
    </div>
    <table-meta v-if="tab === 'meta'" :info="metaInfo" :deletable="true" @delete="handleDelete"></table-meta>
    <graphical-object v-if="tab === 'graphical'" :graph="obj" @submit="updateGraph"></graphical-object>
    <create-sql v-else-if="tab === 'sql'" :attributes="obj.attributes || []" :object_id="String(obj.object_id || '')"
      :from="obj.from_tables || ''" :condition="obj.condition || ''" :name="obj.name || ''" :p_objects="obj.objects"
      :id="id || -1" :key="counter" @created="handleCreated" @updated="handleUpdated"
      @modified="handleModified"></create-sql>
    <table-preview v-else-if="tab === 'preview'" :headers="previewInfo.headers"
      :items="previewInfo.items"></table-preview>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "viewObject",
  props: ['id'],
  data() {
    return {
      tab: 'meta',
      counter: 0
    };
  },
  computed: {
    ...mapState("objects", ['error']),
    ...mapState("objects", ['objects']),
    metaInfo() {
      let table = this.objects.find(t => t.id === this.id)
      return table && table.meta ? this.extractProps(table.meta) : null;
    },
    previewInfo() {
      let table = this.objects.find(t => t.id === this.id);
      console.log(table)
      return table && table.preview ? table.preview : null;
    },
    obj() {
      let obj = this.objects.find(t => t.id === this.id);
      if (!obj) {
        this.$notify.error('Object mapper Not Found: ' + this.errorMessage)
      } else if (!obj.meta) {
        this.$notify.error('Object mapper\'s Meta Not Found: ' + this.errorMessage)
      } else if (!obj.meta.graph && !obj.meta.attributes) {
        this.$notify.error('Object mapper\'s Meta Not Available: ' + this.errorMessage)
      }
      if (obj.meta.graph)
        return obj.meta.graph
      return obj.meta
    },
    isGraph() {
      let obj = this.objects.find(t => t.id === this.id);
      return obj && obj.meta.graph ? true : false;
    }
  },
  methods: {
    fetchInfo(id) {
      let table = this.objects.find(t => t.id === id);
      if (!table || !table.preview) {
        this.$store.dispatch("objects/fetchViewInfo", id)
          .then(id => {
            this.$emit('updated', id);
            this.$notify.success("Object mapper info have been fetched successfully.");
          })
          .catch(e => {
            this.$notify.error("The fetch process of object info failed: " + e);
          });
      }
    },
    handleDelete() {
      this.$emit('deleted', this.id)
      this.$store.dispatch("objects/removeObjectTest", this.id)
        .then(id => {
          this.$emit('deleted', id);
          this.$notify.success("Object mapper was deleted successfully.");
        })
        .catch(e => {
          this.$notify.error("The deletion failed: " + e);
        });
    },
    handleCreated(id) {
      this.$emit('created', id);
      this.counter++
      this.$notify.success("Object mapper was created successfully.");
    },
    handleModified(id) {
      this.$emit('updated', id);
      this.counter++
      this.$notify.success("Object mapper was modified successfully.");
    },
    handleUpdated() {
      this.counter++
    },
    extractProps(object) {
      let attributes = ''
      for (let att in object.attributes) {
        attributes += object.attributes[att].attribute_column
        if (object.attributes[att].timestamp_column)
          attributes += '+' + object.attributes[att].timestamp_column
        attributes += '\n'
      }

      let res = [
        { name: 'Name', value: object.name },
        { name: 'Object ID', value: object.object_id },
        { name: 'Attribute (+ Timestamp) Columns', value: attributes },
        { name: 'From', value: object.from_tables },
        { name: 'Condition', value: object.condition },
      ]

      if (object.objects) {
        for (let i = 0; i < object.objects.length; i++) {
          res.push({ name: 'Object Name', value: object.objects[i].name })
        }
      }
      return res
    },
  }
}
</script>

<style scoped></style>
