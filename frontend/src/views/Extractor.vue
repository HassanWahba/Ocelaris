<template>
  <div class="editor bg-gray overflow-auto">
    <extractor-sidebar :selectedTab="sidebarTab" :key="counter" @updateData="handleSidebarChange"
      @updateTab="handleTabChange"></extractor-sidebar>
    <div class="selected overflow-auto flex-1 p-3">
      <div v-if="id === -1" class="create-action">
        <create-meta v-if="viewTab === TYPE.META" @created="handleCreated"></create-meta>
        <create-change-log v-else-if="viewTab === TYPE.LOGS" :id="-1" @created="handleCreated"></create-change-log>
      </div>
      <div v-else-if="id >= 0" class="view-action">
        <view-meta v-if="viewTab === TYPE.META" :id="id" :key="`meta-${counter}`" @deleted="handleDelete"></view-meta>
        <view-change-log v-else-if="viewTab === TYPE.LOGS" :key="`change-log-${counter}`" :id="id"
          @created="handleCreated" @deleted="handleDelete"></view-change-log>
      </div>
      <div v-else class="view-action">
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Extractor',
  data() {
    return {
      TYPE: {
        META: 'Meta',
        LOGS: 'Log',
        PROCESS: 'Process'
      },
      search: '',
      viewTab: 'Meta',
      sidebarTab: 'Meta',
      id: -2,
      counter: 0
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      await this.$store.dispatch("fetchExtractorData");
      this.counter += 1;
    },
    handleSidebarChange(data) {
      this.viewTab = data.selectedTab;
      this.id = data.id;
    },
    handleTabChange(sidebarTab) {
      if (this.id < -1) {
        this.id--;
      }
      this.sidebarTab = sidebarTab;
      this.counter += 1;
    },
    handleCreated(id) {
      this.id = id;
      this.counter += 1;
    },
    handleDelete() {
      this.id = -2;
      this.counter += 1;
    },
    handleUpdated() {
      this.counter += 1;
    },
  }

};
</script>
