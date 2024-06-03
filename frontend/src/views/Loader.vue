<template>
	<div class="p-3 d-flex">
		<div class="sidebar mr-3 flex-shrink-0">
      <nav class="menu" aria-labelledby="menu-heading">
        <span class="menu-heading" id="menu-heading">Input/Output Options</span>
          <!-- <a class="menu-item" role="tab" type="button" @click="tab = 'Event'" :aria-selected="tab === 'Event' ? 'true' : 'false'"><i class="fa-solid fa-sitemap"></i> IO Events </a>
          <a class="menu-item" role="tab" type="button" @click="tab = 'Object'" :aria-selected="tab === 'Object' ? 'true' : 'false'"><i class="fa-solid fa-object-group"></i> IO Objects </a>
          <a class="menu-item" role="tab" type="button" @click="tab = 'Process'" :aria-selected="tab === 'Process' ? 'true' : 'false'"><i class="fa-solid fa-diagram-project"></i> IO Processes </a> -->
          <a class="menu-item" role="tab" type="button" @click="tab = 'Database'" :aria-selected="tab === 'Database' ? 'true' : 'false'"><i class="fa-solid fa-database"></i> IO OCDM Database</a>
          <a class="menu-item" role="tab" type="button" @click="tab = 'OCEL'" :aria-selected="tab === 'OCEL' ? 'true' : 'false'"><i class="fa-solid fa-database"></i> Extract OCEL 2.0 Database </a>
      </nav>
		</div>
		<div class="flex-1 p-3">
      <io-handler v-if="tab" :display="tab" @exported="" @imported=""></io-handler>
    </div>
	</div>
</template>

<script>
export default {
	name: 'Loader',
  data() {
    return {
      tab: '',
      counter: 0
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      await this.$store.dispatch("fetchLoaderData");
      this.counter += 1;
    }
  }
};
</script>

<style scoped lang="scss">
.sidebar {
	width: 250px;

	.fas {
		text-align: center;
		width: 20px;
		opacity: 0.8;
		margin-right: 5px;
	}
}
</style>
