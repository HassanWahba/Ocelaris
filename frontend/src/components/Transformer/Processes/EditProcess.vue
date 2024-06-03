<template>
	<div class="Box">
		<div class="Box-header">
			<h3 class="Box-title">Neues Projekt</h3>
		</div>

		<div class="overflow-auto">
			<div class="Box-body overflow-auto">
				<form @submit.prevent="saveProject">
					<div class="form-group">
						<div class="form-group-header">
							<label for="project-name">Name</label>
						</div>
						<div class="form-group-body">
							<input class="form-control" type="text" placeholder="Projektname" value="" id="project-name"
								v-model="name" />
						</div>
					</div>

					<div class="form-group">
						<div class="form-group-header">
							<label for="project-routes">Fahrstraßen</label>
						</div>
						<div class="form-group-body">
							<select class="form-select route-drop" id="project-routes" v-model="selectedOption">
								<option disbaled value="">Fahrstraßen für dieses Projekt auswählen...</option>
								<option v-for="item in $store.compact.routes" :value="item.id">{{ item.name }}</option>
							</select>
							<button class="btn" @click.prevent="addID"><i class="fas fa-plus-circle"></i></button>
						</div>
					</div>

					<button class="btn btn-sm mr-2" @click.prevent="deleteID(route)" v-for="route in routesArr">
						{{ $store.compact.routes.filter(r => r.id === route)[0].name }}
						<i class="far fa-trash-alt" style="margin-left: 10px"></i>
					</button>
				</form>
			</div>
			<div class="Box-footer">
				<button class="btn btn-primary width-full mr-1" @click="saveProject"><i class="fas fa-check-circle"></i>
					Projekt erstellen</button>
			</div>
		</div>
	</div>
</template>

<script>
import { mapState } from "vuex";


export default {
	name: 'EditProcess',
	data() {
		return {
			name: '',
			selectedOption: '',
			routesArr: []
		};
	},
	computed: {
		...mapState('objects', ['objects']),
		...mapState('events', ['events'])
	},
	methods: {
		addID: function () {
			if (this.selectedOption === '') {
				this.$notify.error('Keine Fahrstraße wurde ausgewählen...');
			} else if (this.routesArr.includes(this.selectedOption)) {
				this.$notify.error('Fahrstraße existiert im Projekt schon');
			} else {
				this.routesArr.push(this.selectedOption);
			}
		},
		deleteID: function (routeId) {
			this.routesArr.splice(this.routesArr.indexOf(routeId), 1);
		},
		saveProject: function () {
			for (let i = 0; i < this.routesArr.length; i++) {
				this.routesArr[i] = parseInt(this.routesArr[i]);
			}
			if (this.name !== '') {
				this.$api
					.post('projects/', {
						name: this.name,
						routes_IDs: this.routesArr
					})
					.then(resp => {
						this.$notify.success('Projekt wurde erstellt.');
						this.$emit('created', resp.data.id);
						this.$store.fetchCompactListings();
					})
					.catch(err => {
						this.$notify.error('Fehler beim Erstellen: ' + err);
					});
			} else {
				this.$notify.error('Projektname fehlt');
			}
		},
		handleModified() {
			this.$store.dispatch("processes/fetchViewInfo", this.id)
				.then(id => {
					this.$emit('updated', id);
					this.$notify.success("Process info have been fetched successfully.");
				})
				.catch(e => {
					this.$notify.error("The fetch process of object info failed: " + e);
				});
		},
	}
};
</script>

<style scoped>
.route-drop {
	width: calc(100% - 52px);
}
</style>
