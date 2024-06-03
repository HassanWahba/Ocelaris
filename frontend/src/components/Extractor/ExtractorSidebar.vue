<template>
  <div class="tree bg-white border-right ui-f7 no-select overflow-auto d-flex flex-column">
    <div class="flex-shrink-0">
      <nav class="UnderlineNav" style="display: block">
        <div class="tab-bar UnderlineNav-body flex-justify-center flex-items-center" role="tablist">
          <button class="UnderlineNav-item flex-1" role="tab" type="button" @click="$emit('updateTab', TYPE.META)"
            :aria-selected="selectedTab === TYPE.META ? 'true' : 'false'">Meta Tables</button>
          <button class="UnderlineNav-item flex-1" role="tab" type="button" @click="$emit('updateTab', TYPE.LOGS)"
            :aria-selected="selectedTab === TYPE.LOGS ? 'true' : 'false'">Change Logs</button>
        </div>
      </nav>
      <div class="p-2 border-bottom">
        <input class="form-control input-sm width-full" placeholder="Search..." v-model="search" />
      </div>
      <div class="p-2 border-bottom">
        <button class="btn btn-primary width-full" type="button"
          @click="$emit('updateData', { id: -1, selectedTab: selectedTab })">
          <i class="fas fa-plus mr-2"></i> New {{ selectedTab }}
        </button>
      </div>
    </div>

    <div class="overflow-auto flex-1">
      <a v-for="e in filtered" class="menu-item text-center" style="font-size: 20px; font-weight: bold"
        @click.prevent="$emit('updateData', { id: e.id, selectedTab: selectedTab })">{{ e.meta.name }}
      </a>
    </div>

  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "ExtractorSidebar",
  props: ['selectedTab'],
  data() {
    return {
      TYPE: {
        META: 'Meta',
        LOGS: 'Log'
      },
      search: '',
    };
  },
  computed: {
    ...mapState("meta", ['metaTables']),
    ...mapState("log", ['logs']),
    filtered() {
      let list = [];
      switch (this.selectedTab) {
        case this.TYPE.META:
          list = this.metaTables;
          break;
        case this.TYPE.LOGS:
          list = this.logs;
          break;
      }
      if (this.search.length > 0) {
        list = list.filter(e => {
          return e.meta.name.toLowerCase().indexOf(this.search.toLowerCase()) >= 0;
        });
      }
      return list;
    }
  }
};
</script>

<style scoped></style>