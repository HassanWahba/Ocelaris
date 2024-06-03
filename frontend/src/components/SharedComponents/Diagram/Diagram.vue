<template>
  <div id="svg-diagram-show-area" class="scrollXY border" ref="field">
    <svg ref="svgElement" @dragover.prevent @drop="drop($event)" :width="'100%'" :height="'100%'"
      :viewBox="viewBoxDiagram" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <pattern id="smallGrid" width="10" height="10" patternUnits="userSpaceOnUse">
          <path d="M 10 0 L 0 0 0 10" fill="none" stroke="gray" stroke-width="0.5" />
        </pattern>
        <pattern id="grid" width="100" height="100" patternUnits="userSpaceOnUse">
          <rect width="100" height="100" fill="url(#smallGrid)" />
          <path d="M 100 0 L 0 0 0 100" fill="none" stroke="gray" stroke-width="1" />
        </pattern>
      </defs>
      <g :transform="scaleStr">
        <rect x="0" y="0" :width="width" :height="height" :fill="showGrid ? 'url(#grid)' : background" @click="reset" />
        <graph-node :node="item" :selected="item.id === selectedNode" v-for="item in nodeList" :key="item.id"
          :createLinkMode="createLinkMode" :editable="editable" :labels="labels" :rWidth="rect().rWidth"
          :rHeight="rect().rHeight" @editNode="editNode" @click="clickNode" @select="selectNode" @copy="copyNode"
          @updateLocation="updateNodeLocation" @toggleSelect="toggleSrcSelect" @commitDest="commitDest"
          @remove="removeNode" />
        <graph-link v-for="item in linkList" :link="item" :selected="item.id === selectedLink" :key="item.id"
          :source="findNode(item.source)" :destination="findNode(item.destination)" :editable="editable"
          :rWidth="rect().rWidth" :rHeight="rect().rHeight" @editLink="editLink" @click="clickLink" @select="selectLink"
          @updateLocation="updateLinkLocation" @remove="removeLink" />
      </g>
    </svg>
  </div>
</template>
<script>
export default {
  name: "Diagram",
  props: {
    width: Number,
    height: Number,
    background: String,
    showGrid: Boolean,
    nodes: Array,
    links: Array,
    editable: Boolean,
    labels: Object,
    fluid: {
      type: Boolean,
      default: false
    },
    admissibleTypes: Array
  },
  computed: {
    viewBoxDiagram() {
      return this.fluid
        ? `0 0 ${this.width / this.scale} ${this.height / this.scale}`
        : `0 0 ${this.width} ${this.height}`;
    },
    scaleStr() {
      return (
        "scale(" +
        (this.fluid ? 1.0 : this.scale || 1.0) +
        ")" +
        "translate(" +
        0 +
        "," +
        0 +
        ")"
      );
    },
    nodeList: {
      get() {
        return this.nodes;
      },
      set(val) {
        this.$emit("nodeChanged", {
          nodes: val
        });
      }
    },
    linkList: {
      get() {
        return this.links;
      },
      set(val) {
        this.$emit("linkChanged", {
          links: val
        });
      }
    }
  },
  watch: {
    editable() {
      this.reset()
    }
  },
  data() {
    return {
      name: "",
      url: "",
      color: "",
      selectedNode: -1,
      selectedLink: -1,
      createLinkMode: false
    };
  },
  methods: {
    drop(event) {
      if (!this.editable) {
        this.$notify.error('The graph is not in edit modus.')
        return;
      }
      let data = event.dataTransfer.getData("text/plain");

      let { id, table, tab } = JSON.parse(data);
      if (!this.isAdmissible(tab)) {
        this.$notify.error('The item is not an admissible type. Expected ' + JSON.stringify(this.admissibleTypes) + '. Got: ' + tab)
        return;
      } else if (this.findNode(id)) {
        this.$notify.error('The selected ' + tab.toLowerCase() + ' already exists.')
        return;
      }
      let svg = this.$refs.svgElement;
      let pt = svg.createSVGPoint();
      pt.x = event.clientX;
      pt.y = event.clientY;

      let svgP = pt.matrixTransform(svg.getScreenCTM().inverse());

      this.nodeList.push({
        id: id,
        content: { text: table, color: '#fab1a0' },
        width: 150,
        height: 100,
        shape: "ellipse",
        point: {
          x: svgP.x - 75,
          y: svgP.y - 50,
        },
      });
    },
    editNode(item) {
      this.$emit("editNode", item);
    },
    editLink(item) {
      this.$emit("editLink", item);
    },
    generateID() {
      return (
        new Date().getTime().toString(16) +
        Math.floor(Math.random() * 1000000).toString(16)
      );
    },
    reset() {
      if (!this.createLinkMode) {
        this.selectedNode = -1;
        this.selectedLink = -1;
      }
    },
    updateLinkLocation(obj) {
      let item = this.nodeList.find(x => x.id === obj.id);
      item.point.x = obj.x;
      item.point.y = obj.y;
    },
    findNode(id) {
      return this.nodes.find(x => x.id === id);
    },
    removeLink(id) {
      this.$emit("linkRemoved", id);
      this.linkList = this.linkList.filter(x => x.id !== id);
    },
    rect() {
      if (this.fluid) {
        const rect = this.$refs.field.getBoundingClientRect();
        return {
          rWidth: rect.width / this.width,
          rHeight: rect.height / this.height
        };
      } else {
        return {
          rWidth: 1,
          rHeight: 1
        };
      }
    },
    updateNodeLocation(obj) {
      let item = this.nodeList.find(x => x.id === obj.id);
      item.point.x = obj.x;
      item.point.y = obj.y;
    },
    clickNode(id) {
      this.$emit("nodeClicked", id);
    },
    clickLink(id) {
      this.$emit("linkClicked", id);
    },
    selectNode(id) {
      this.selectedNode = id;
    },
    selectLink(id) {
      this.selectedLink = id;
    },
    toggleSrcSelect() {
      this.createLinkMode = !this.createLinkMode;
    },
    commitDest(id) {
      let src = this.nodeList.find(x => x.id === this.selectedNode);
      let dest = this.nodeList.find(x => x.id === id);
      let newId = this.generateID()
      this.linkList.push({
        id: newId,
        source: this.selectedNode,
        destination: id,
        point: {
          x: (src.point.x + dest.point.x) * 0.5,
          y: (src.point.y + dest.point.y) * 0.5
        }
      });
      this.createLinkMode = false;
      this.selectedNode = -1;
      this.$emit("linkCreated", newId)
    },
    removeNode(id) {
      this.$emit("nodeRemoved", id)
      this.nodeList = this.nodeList.filter(x => x.id !== id);
      this.linkList = this.linkList.filter(x => {
        return x.source !== id && x.destination !== id;
      });
      this.createLinkMode = false;
    },
    copyNode(node) {
      if (!this.editable) return;
      this.nodeList.push({
        id: this.generateID(),
        content: {
          text: node.content.text,
          color: node.content.color,
          url: node.content.url
        },
        width: node.width,
        height: node.height,
        point: {
          x: node.point.x + 30,
          y: node.point.y + 30
        },
        shape: node.shape,
        stroke: node.stroke,
        strokeWeight: node.strokeWeight
      });
    },
    isAdmissible(tab) {
      return this.admissibleTypes.includes(tab)
    }
  }
};
</script>
<style>
.button {
  cursor: pointer;
}

.grab {
  cursor: grab;
}
</style>
