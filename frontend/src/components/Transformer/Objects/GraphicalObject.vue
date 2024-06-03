<template>
  <section>
    <edit-node-modal :node="tmpNode" :isActive="isEditModalActive" @ok="openNodeEdit"
      @cancel="cancelNodeEdit"></edit-node-modal>

    <edit-link-modal :link="tmpLink" :isActive="isEditLinkModalActive" @ok="editLink"
      @cancel="cancelLinkEdit"></edit-link-modal>
    <diagram :width="2000" :height="1000" :fluid="false" background="#fafafa" :nodes="graphData.nodes"
      :links="graphData.links" :editable="editable" :admissibleTypes="admissibleTypes" :labels="{
      edit: 'Edit',
      remove: 'Remove',
      link: 'Link',
      select: 'Select'
    }" @editNode="openNodeEdit" @editLink="openLinkEdit" @nodeChanged="nodeChanged" @linkChanged="linkChanged"
      @linkCreated="linkCreated"></diagram>
    <div v-if="graph && graph.nodes" class="Box-footer">
      <button v-if="editable" class="btn mr-1" @click="submitChanges"><i class="fas fa-check-circle"></i> Lock</button>
      <button v-else class="btn mr-1" @click="editGraph">Edit</button>
    </div>
    <div v-else class="Box-footer">
      <textarea required placeholder="Object Name" class="form-control mr-1 p-1" style="height: 32px; resize: none;"
        id="obj-name" cols="40" v-model="graphData.name"></textarea>
      <button class="btn mr-1" @click="submit"><i class="fas fa-check-circle"></i> Create</button>
    </div>
  </section>
</template>

<script>
export default {
  name: "GraphicalObject",
  props: ['graph'],
  data() {
    return {
      isEditLinkModalActive: false,
      isEditModalActive: false,
      tmpNode: {
        id: "",
        select: "",
        where: ""
      },
      tmpLink: {
        id: "",
        source: "",
        destination: "",
        on: "",
        where: ""
      },
      editable: false,
      graphData: {
        name: '',
        nodes: [],
        links: []
      },
      admissibleTypes: ['Table']
    };
  },
  mounted() {
    if (this.graph) {
      this.graphData.nodes = this.graph.nodes || [];
      this.graphData.links = this.graph.links || [];
      this.graphData.name = this.graph.name || '';
      this.editable = false;
    } else
      this.editable = true;

    console.log(this.editable)
  },
  methods: {
    openNodeEdit(item) {
      this.tmpLink.id = item.id;
      this.tmpLink.source = item.source;
      this.tmpLink.destination = item.destination;
      this.tmpLink.select = item.select;
      this.tmpLink.where = item.where;
      this.isEditModalActive = true;
    },
    editNode(item) {
      if (item.select === undefined || item.select.trim() === '') {
        this.$notify.error('The SELECT field is mandatory.')
        return
      }
      let tmp = this.graphData.nodes.find(x => x.id === item.id);
      tmp.select = item.select;
      tmp.where = item.where;
      this.isEditModalActive = false;
    },
    cancelNodeEdit(item) {
      if (item.select && item.select.trim() === '')
        this.graphData.nodes.splice(this.graphData.nodes.findIndex(x => x.id === item.id), 1)
      this.isEditModalActive = false;
    },
    openLinkEdit(item) {
      this.tmpLink.id = item.id;
      this.tmpLink.on = item.on;
      this.tmpLink.where = item.where;
      this.isEditLinkModalActive = true;
    },
    editLink(item) {
      if (item.on === undefined || item.on.trim() === '') {
        this.$notify.error('The ON condition is mandatory.')
        return
      }
      let tmp = this.graphData.links.find(x => x.id === item.id);
      tmp.on = item.on;
      tmp.where = item.where;
      this.isEditLinkModalActive = false;
    },
    cancelLinkEdit(item) {
      if (item.on && item.on.trim() === '')
        this.graphData.links.splice(this.graphData.links.findIndex(x => x.id === item.id), 1)
      this.isEditLinkModalActive = false;
    },
    nodeChanged(obj) {
      this.graphData.nodes = obj.nodes;
    },
    linkChanged(obj) {
      this.graphData.links = obj.links;
    },
    linkCreated(id) {
      this.openLinkEdit({ id: id, on: '', where: '' })
    },
    isTree() {
      let visited = new Set();
      console.log(this.graphData)
      let nodes = this.graphData.nodes.map(node => node.id);

      // Use Depth-First Search to check for cycles and connectivity.
      const dfs = (node, parent) => {
        visited.add(node);
        for (let neighbor of this.graphData.links.filter(link => link.source === node || link.destination === node)) {
          let nextNode = (neighbor.source === node) ? neighbor.destination : neighbor.source;
          if (nextNode !== parent) {
            if (visited.has(nextNode)) {
              return true;
            } else if (dfs(nextNode, node)) {
              return true;
            }
          }
        }
        return false;
      };

      // Start DFS from the first node.
      if (dfs(nodes[0], null)) {
        return false; // Cycle detected.
      }

      // Check if all nodes were visited (i.e., the graph is connected).
      for (let node of nodes) {
        if (!visited.has(node)) {
          return false;
        }
      }
      return true;
    },
    validate() {
      if (this.graphData.nodes.length === 0) {
        this.$notify.error('At least one table should be included in the graph')
        return false
      } else if (!this.isTree()) {
        this.$notify.error('The graph should be a tree.')
        return false
      } else if (this.graphData.name === '') {
        this.$notify.error('Please insert a name for the new object.')
        return false
      } else {
        return true
      }
    },
    submitChanges() {
      if (this.validate()) {
        this.editable = false;
        this.$emit('change', this.graphData)
      }
    },
    submit() {
      if (this.validate())
        this.$emit('submit', this.graphData)
    },
    editGraph() {
      this.editable = true;
    }
  }
};
</script>