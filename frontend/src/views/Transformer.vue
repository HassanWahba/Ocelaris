<template>
  <div class="editor bg-gray overflow-auto">
    <transformer-sidebar :selectedTab="sidebarTab" :key="counter" @updateData="handleSidebarChange" @updateTab="handleTabChange"></transformer-sidebar>
    <div class="selected overflow-auto flex-1 p-3">
      <div v-if="id === -1" class="create-action">
        <create-event v-if="viewTab === TYPE.EVENTS" @created="handleCreated"></create-event>
        <create-object v-else-if="viewTab === TYPE.OBJECTS" @created="handleCreated"></create-object>
        <create-process v-else-if="viewTab === TYPE.PROCESS" @created="handleCreated"></create-process>
      </div>
      <div v-else-if="id>=0" class="view-action">
        <view-table v-if="viewTab === TYPE.TABLES" :id="id" :key="`table-${counter}`" @updated="handleUpdated"></view-table>
        <view-event v-else-if="viewTab === TYPE.EVENTS" :id="id" :key="`event-${counter}`" @updated="handleUpdated" @created="handleCreated" @deleted="handleDelete"></view-event>
        <view-object v-else-if="viewTab === TYPE.OBJECTS" :id="id" :key="`object-${counter}`" @updated="handleUpdated" @created="handleCreated"  @deleted="handleDelete"></view-object>
        <view-process v-else-if="viewTab === TYPE.PROCESS" :id="id" :key="`process-${counter}`" @updated="handleUpdated" @created="handleCreated" @deleted="handleDelete"></view-process>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: "Transformer",
  data() {
    return {
      TYPE: {
        TABLES: 'Table',
        EVENTS: 'Event',
        OBJECTS: 'Object',
        PROCESS: 'Process'
      },
      search: '',
      viewTab: 'Table',
      sidebarTab: 'Table',
      id: -2,
      counter: 0
    }
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      await this.$store.dispatch("fetchTransformerData");
      this.counter += 1;
    },
    async handleSidebarChange(data) {
      let id = data.id;
      let viewTab = data.selectedTab;
      if (id >= 0 && viewTab === this.TYPE.TABLES) {
        await this.$store.dispatch("tables/fetchViewInfo", id);
      }
      this.viewTab = viewTab;
      this.id = id;
    },
    handleTabChange(sidebarTab) {
      if (this.id < -1) {
        this.id--;
      }
      this.sidebarTab = sidebarTab;
      this.counter += 1;
    },
    handleCreated(id){
      this.id = id;
      this.counter += 1;
    },
    handleDelete(){
      this.id = -2;
      this.counter += 1;
    },
    handleUpdated(){
      this.counter += 1;
    },
  }
};
</script>

<style scoped lang="scss">
.editor {
  height: 100%;
  display: flex;
}

.tree {
  width: 360px;
  height: 100%;
  flex-shrink: 0;

  .item {
    border-radius: 0;
    border-right: 0;
    border-top: 0;
    border-left: 0;
    cursor: pointer;
  }

  .item:focus {
    outline: 0;
    box-shadow: none;
    background-color: white;
  }
}

.selected {
  height: 100%;
  flex-grow: 1;
  border-radius: 2px;
}

.tab-bar {
  width: 100%;
}

.UnderlineNav-item {
  padding: 8px 8px;
}
</style>
