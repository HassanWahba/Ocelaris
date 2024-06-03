<template>
  <div>
    <div class="tabnav">
      <nav class="tabnav-tabs">
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'meta'"
          :aria-selected="tab === 'meta' ? 'true' : 'false'">Meta Data</button>
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'modify'"
          :aria-selected="tab === 'modify' ? 'true' : 'false'">Modify</button>
        <button class="tabnav-tab" role="tab" type="button" @click="tab = 'preview'"
          :aria-selected="tab === 'preview' ? 'true' : 'false'">Preview</button>
      </nav>
    </div>
    <table-meta v-if="tab === 'meta' && metaInfo" :info="metaInfo" :deletable="true"
      @delete="handleDelete"></table-meta>
    <create-event v-else-if="tab === 'modify'" @modify="handleModified" :id="event.id" :name="event.meta.name"
      :selectedLog="event.meta.logs[0].id || null" :selectedColumns="event.meta.selectedColumns"
      :condition="event.meta.condition" :object_id="event.meta.object_id" :p_objects="event.meta.objects"
      :key="counter"></create-event>
    <table-preview v-else-if="tab === 'preview' && previewInfo" :headers="previewInfo.headers"
      :items="previewInfo.items"></table-preview>
    <h2 v-else-if="id >= 0"><span>Loading</span><span class="AnimatedEllipsis"></span></h2>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "ViewEvent",
  props: ['id'],
  data() {
    return {
      tab: 'meta',
      counter: 0
    };
  },
  computed: {
    ...mapState("events", ['events']),
    event() {
      return this.events.find(t => t.id == this.id)
    },
    metaInfo() {
      return this.event && this.event.meta ? this.extractProps(this.event.meta) : null;
    },
    previewInfo() {
      if (!this.event) {
        this.$notify.error('Event Not Found: ' + this.errorMessage)
      } else if (!this.event.preview) {
        this.$notify.error('Event Preview Not Found: ' + this.errorMessage)
      } else if (!this.event.preview.headers) {
        this.$notify.error('Event Preview Not Available: ' + this.event.preview.message)
      }
      return this.event && this.event.preview ? this.event.preview : null;
    }
  },
  methods: {
    handleDelete() {
      this.$store.dispatch("events/removeEvent", { id: this.id })
        .then(res => {
          this.$notify.success("Event mapper was deleted successfully.");
          this.$emit('deleted', this.id)
        })
        .catch(e => {
          this.$notify.error("The deletion failed: " + e);
        });
    },
    handleModified() {
      this.$emit('updated')
      this.counter++
      this.$notify.success("Event mapper was modified successfully.");
    },
    extractProps(event) {
      let res = [
        { name: 'Name', value: event.name },
      ]
      console.log(event)
      if (event.logs) {
        for (let i = 0; i < event.logs.length; i++) {
          res.push({ name: 'Log Name', value: event.logs[i].name })
        }
      }
      if (event.objects) {
        for (let i = 0; i < event.objects.length; i++) {
          res.push({ name: 'Object Name', value: event.objects[i].name })
        }
      }
      return res
    }
  }
}
</script>
<style scoped></style>