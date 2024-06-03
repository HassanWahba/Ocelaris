<template>
  <div class="tree bg-white border-right ui-f7 no-select overflow-auto d-flex flex-column">
    <div class="flex-shrink-0">
      <nav class="UnderlineNav" style="display: block">
        <div class="tab-bar UnderlineNav-body flex-justify-center flex-items-center" role="tablist">
          <button class="UnderlineNav-item flex-1" role="tab" type="button" @click="$emit('updateTab', TYPE.TABLES)"
            :aria-selected="selectedTab === TYPE.TABLES ? 'true' : 'false'">Tables</button>
          <button class="UnderlineNav-item flex-1" role="tab" type="button" @click="$emit('updateTab', TYPE.OBJECTS)"
            :aria-selected="selectedTab === TYPE.OBJECTS ? 'true' : 'false'">Object Mappers</button>
          <button class="UnderlineNav-item flex-1" role="tab" type="button" @click="$emit('updateTab', TYPE.EVENTS)"
            :aria-selected="selectedTab === TYPE.EVENTS ? 'true' : 'false'">Event Mappers</button>
          <button class="UnderlineNav-item flex-1" role="tab" type="button" @click="$emit('updateTab', TYPE.PROCESS)"
            :aria-selected="selectedTab === TYPE.PROCESS ? 'true' : 'false'">Processes</button>
        </div>
      </nav>
      <div class="p-2 border-bottom">
        <input class="form-control input-sm width-full" placeholder="Search..." v-model="search" />
      </div>
      <div class="p-2 border-bottom">
        <button v-if="selectedTab !== TYPE.TABLES" class="btn btn-primary width-full" type="button"
          @click="$emit('updateData', { id: -1, selectedTab: selectedTab })">
          <i class="fas fa-plus mr-2"></i> New {{ selectedTab }}
        </button>
      </div>
    </div>

    <div class="overflow-auto flex-1">
      <a v-for="r in filtered" class="menu-item text-center" style="font-size: 20px; font-weight: bold"
        @click.prevent="$emit('updateData', { id: r.id, selectedTab: selectedTab })" :href="'#'"
        :draggable="isDraggable(selectedTab)" @dragstart="drag($event, r.id, r.meta.name, selectedTab)">{{ r.meta.name
        }}
      </a>
    </div>

  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "TransformerSidebar",
  props: ['selectedTab'],
  data() {
    return {
      TYPE: {
        TABLES: 'Table',
        EVENTS: 'Event',
        OBJECTS: 'Object',
        PROCESS: 'Process'
      },
      search: '',
    };
  },
  computed: {
    ...mapState("tables", ['tables']),
    ...mapState("objects", ['objects']),
    ...mapState("events", ['events']),
    ...mapState("processes", ['processes']),
    filtered() {
      let list = [];
      switch (this.selectedTab) {
        case this.TYPE.TABLES:
          if (this.search.length === 0)
            list = this.tables.slice(0, 50);
          else if (this.search.length > 1)
            list = this.tables.filter(e => {
              if (!e.meta || !e.meta.name) { console.log('Error: ', e); }
              return e.meta.name.toLowerCase().indexOf(this.search.toLowerCase()) == 0;
            }).slice(0, 50);
          break;
        case this.TYPE.EVENTS:
          list = this.events;
          break;
        case this.TYPE.OBJECTS:
          list = this.objects;
          break;
        case this.TYPE.PROCESS:
          list = this.processes;
          break;
      }
      return list;
    }
  },
  methods: {
    isDraggable(tab) {
      return tab !== this.TYPE.PROCESS;
    },
    drag(event, id, table, tab) {
      event.dataTransfer.setData("text/plain", JSON.stringify({ id, table, tab }));
    },
  }
};
</script>

<style scoped></style>