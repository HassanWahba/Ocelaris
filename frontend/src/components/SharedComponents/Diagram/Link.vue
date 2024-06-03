<template>
  <g>
    <line :x1="calcSource().x" :y1="calcSource().y" :x2="calcDestination().x" :y2="calcDestination().y" stroke="#ffeaa7"
      stroke-width="3" fill="none"></line>
    <g v-if="editable">
      <line :x1="calcSource().x" :y1="calcSource().y" :x2="point.x" :y2="point.y" stroke="lightgray"></line>
      <line :x1="point.x" :y1="point.y" :x2="calcDestination().x" :y2="calcDestination().y" stroke="lightgray"></line>
      <ellipse :id="id" :cx="point.x" :cy="point.y" rx="10" ry="10" fill="#ff7675" stroke-width="2" class="grab"
        @click="select" @mousedown="mousedown" @touchstart="mousedown" @mousemove="mousemove" @touchmove="mousemove"
        @mouseup="mouseup" @touchend="mouseup"></ellipse>
    </g>
    <g v-if="selected">
      <text :x="point.x - 7" :y="point.y - 20" fill="#00b894" @click="edit" class="button">
        Edit
      </text>
      <text :x="point.x - 15" :y="point.y + 30" fill="#ff7675" @click="remove" class="button">
        Remove
      </text>
    </g>
  </g>
</template>
<script>
import mouseLocation from "./mouseLocation";
export default {
  mixins: [mouseLocation],
  props: {
    selected: Boolean,
    editable: Boolean,
    source: {
      id: Number,
      x: Number,
      y: Number
    },
    destination: {
      id: Number,
      x: Number,
      y: Number
    },
    link: {
      id: String,
      on: {
        type: String,
        default: ""
      },
      where: {
        type: String,
        default: ""
      },
    },
    rWidth: Number,
    rHeight: Number
  },
  computed: {},
  data() {
    return {
      startPosition: null,
      cursorOffset: {
        x: 0,
        y: 0
      },
      id: this.link.id,
      point: this.link.point
    };
  },
  methods: {
    mousedown(e) {
      this.$emit("click", this.link.id);
      const [x, y] = this.getLocation(e);
      this.cursorOffset.x = x;
      this.cursorOffset.y = y;
      this.startPosition = { x: this.point.x, y: this.point.y };
      document.addEventListener("mousemove", this.mousemove);
      document.addEventListener("mouseup", this.mouseup);
    },
    mousemove(e) {
      if (this.startPosition) {
        e.preventDefault();
        const [x, y] = this.getLocation(e);
        this.point.x =
          this.startPosition.x +
          (x - this.cursorOffset.x) / this.rWidth;
        this.point.y =
          this.startPosition.y +
          (y - this.cursorOffset.y) / this.rHeight;
        this.$emit("updateLocation", {
          id: this.id,
          x: this.point.x,
          y: this.point.y
        });
      }
    },
    mouseup() {
      this.startPosition = null;
      document.removeEventListener("mousemove", this.mousemove);
      document.removeEventListener("mouseup", this.mouseup);
    },
    remove() {
      this.$emit("remove", this.id);
    },
    select() {
      this.$emit("select", this.id);
    },
    edit() {
      this.$emit("editLink", {
        id: this.link.id,
        on: this.link.on,
        where: this.link.where
      });
    },
    calcSource() {
      let dx = this.point.x - this.source.point.x - this.source.width / 2;
      let dy = this.point.y - this.source.point.y - this.source.height / 2;
      if (dx === 0) {
        dx = 0.01;
      }
      if (Math.abs(dy / dx) <= 1) {
        if (dx >= 0) {
          return {
            x: this.source.point.x + this.source.width,
            y: this.source.point.y + this.source.height / 2
          };
        } else {
          return {
            x: this.source.point.x,
            y: this.source.point.y + this.source.height / 2
          };
        }
      } else {
        if (dy >= 0) {
          return {
            x: this.source.point.x + this.source.width / 2,
            y: this.source.point.y + this.source.height
          };
        } else {
          return {
            x: this.source.point.x + this.source.width / 2,
            y: this.source.point.y
          };
        }
      }
    },
    calcDestination() {
      let dx =
        this.point.x - this.destination.point.x - this.destination.width / 2;
      let dy =
        this.point.y - this.destination.point.y - this.destination.height / 2;
      if (dx === 0) {
        dx = 0.01;
      }
      if (Math.abs(dy / dx) <= 1) {
        if (dx >= 0) {
          return {
            x: this.destination.point.x + this.destination.width,
            y: this.destination.point.y + this.destination.height / 2
          };
        } else {
          return {
            x: this.destination.point.x,
            y: this.destination.point.y + this.destination.height / 2
          };
        }
      } else {
        if (dy >= 0) {
          return {
            x: this.destination.point.x + this.destination.width / 2,
            y: this.destination.point.y + this.destination.height
          };
        } else {
          return {
            x: this.destination.point.x + this.destination.width / 2,
            y: this.destination.point.y
          };
        }
      }
    }
  }
};
</script>
<style scoped></style>