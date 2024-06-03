<template>
  <div>
    <div class="modal" :class="{ 'is-open': isActive }" @click="cancel"></div>
    <div class="item" :class="{ 'is-open': isActive }">
      <transition name="item">
        <div class="form" v-if="isActive">
          <input v-model="newLink.on" placeholder="ON Clause" /><br />
          <input v-model="newLink.where" placeholder="WHERE Clause"><br />
          <button @click="ok">OK</button>
          <button class="danger" @click="cancel">Cancel</button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: "EditLinkModal",
  props: {
    isActive: Boolean,
    link: {
      type: Object,
      default() {
        return {
          id: "",
          on: "",
          where: ""
        };
      }
    }
  },
  data() {
    return {
      newLink: this.link,
      oldLink: Object.assign({}, this.link)
    };
  },
  methods: {
    ok() {
      this.$emit("ok", this.newLink);
    },
    cancel() {
      this.$emit("cancel", this.oldLink);
    }
  },
  watch: {
    link(newLink, oldLink) {
      if (newLink !== oldLink) {
        this.newLink = newLink;
      }
    }
  }
};
</script>

<style lang="scss" scoped>
input {
  width: 95%;
  margin-bottom: 5px;
}

select {
  margin-bottom: 5px;
}

.item-enter-active {
  transition: all 0.8s ease;
}

.item-leave-active {
  transition: all 0.3s ease;
}

.item-enter,
.item-leave-to {
  opacity: 0;
}
</style>
