<template>
  <div class="d-flex">
    <div class="sidebar mr-3 flex-shrink-0">
      <nav class="menu" aria-labelledby="menu-heading">
        <span class="menu-heading" id="menu-heading">Supported ERP Systems</span>
        <a class="menu-item" role="tab" type="button" @click="tab = 'oracle'"
          :aria-selected="tab === 'oracle' ? 'true' : 'false'"><i class="fa-solid fa-database"></i> Oracle EBS</a>
        <a class="menu-item" role="tab" type="button" @click="tab = 'custom'"
          :aria-selected="tab === 'custom' ? 'true' : 'false'"><i class="fa-solid fa-database"></i> Custom ERP System
        </a>
      </nav>
    </div>
    <div class="flex-1 p-3">
      <connection-info v-if="tab === ''" @disconnected="refresh" :key="componentKey"></connection-info>
      <oracle v-if="tab === 'oracle'" @created="handleCreated"></oracle>
      <custom v-if="tab === 'custom'" @created="handleCreated"></custom>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: 'DatabaseConnection',
  data() {
    return {
      tab: '',
      componentKey: 0
    };
  },
  mounted() {
    this.componentKey += 1;
  },
  created() {
    this.fetchSupportedDatabases();
    this.validate();
  },
  methods: {
    ...mapActions('connection', ['fetchSupportedDatabases', 'validateConnection']),
    refresh() {
      this.componentKey += 1;
    },
    async validate() {
      const isValid = await this.validateConnection()
      if (isValid) {
        this.$notify.success('Connection Validated Successfully');
        this.componentKey += 1;
        let isFetched = await this.$store.dispatch('fetchAllData');
        if (isFetched) {
          this.$notify.success('Data Fetched Successfully');
        } else {
          this.$notify.error('Data Fetch Failed');
        }
      } else {
        this.$notify.error('Connection Validation Failed');
      }
    },
    async handleCreated() {
      await this.validate();
      let isFetched = await this.$store.dispatch('fetchAllData');
      if (isFetched) {
        this.$notify.success('Data Fetched Successfully');
      } else {
        this.$notify.error('Data Fetch Failed');
      }
      this.componentKey += 1;
      this.tab = '';
    }
  }
};
</script>

<style scoped lang="scss"></style>
