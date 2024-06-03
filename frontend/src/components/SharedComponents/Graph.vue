<template>
  <div ref="graph"></div>
</template>

<script>
import * as d3 from 'd3';
import { mapState } from "vuex";

export default {
  data() {
    return {
      nodes: [],
      links: [],
    };
  },
  computed: {
    ...mapState("processes", ['processes']),
  },
  mounted() {
    this.tables.forEach(table => {
      this.nodes.push(table);
    });
    this.joins.forEach(join => {
      const sourceNode = this.nodes.find(node => node.id === join.sourceTable);
      const targetNode = this.nodes.find(node => node.id === join.targetTable);
      this.links.push({ source: sourceNode, target: targetNode });
    });

    console.log("Nodes: ", this.nodes);
    console.log("Links: ", this.links);

    this.renderGraph();
  },
  methods: {
    renderGraph() {
      const svg = d3.select(this.$refs.graph)
        .append("svg")
        .attr("width", 800)
        .attr("height", 600);

      const simulation = d3.forceSimulation(this.nodes)
        .force("link", d3.forceLink(this.links).distance(200))
        .force("charge", d3.forceManyBody().strength(-500))
        .force("center", d3.forceCenter(800 / 2, 600 / 2));

      const link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(this.links)
        .enter().append("line");

      const node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(this.nodes)
        .enter().append("circle")
        .attr("r", 20)
        .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

      node.append("title")
        .text(d => d.id);

      simulation.nodes(this.nodes)
        .on("tick", ticked);

      simulation.force("link")
        .links(this.links);

      function ticked() {
        link
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

        node
          .attr("cx", d => d.x)
          .attr("cy", d => d.y);
      }

      function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
      }

      function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
    },
  },
};
</script>

<style scoped>
.links line {
  stroke: #999;
  stroke-opacity: 0.6;
}

.nodes circle {
  stroke: #fff;
  stroke-width: 1.5px;
}
</style>
