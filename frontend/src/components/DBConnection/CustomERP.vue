<template>
	<div class="Box">
		<div class="Box-header">
			<h3 class="Box-title">New Custom Connection</h3>
		</div>

		<div class="overflow-auto">
			<div class="Box-body overflow-auto">
				<form @submit.prevent="connect">
					<div class="form-group">
						<div class="form-group-header">
							<label for="hostname">Hostname</label>
						</div>
						<div class="form-group-body">
							<input class="form-control width-full" type="text" placeholder="erp.company.com"
								id="hostname" v-model="hostname" />
						</div>
					</div>

					<div class="form-group">
						<div class="form-group-header">
							<label for="hostname">Port</label>
						</div>
						<div class="form-group-body">
							<input class="form-control width-full" type="text" placeholder="8080" id="port"
								v-model="port" />
						</div>
					</div>

					<div class="form-group">
						<div class="form-group-header">
							<label for="database">Database</label>
						</div>
						<div class="form-group-body">
							<input class="form-control width-full" type="text" id="sid" v-model="sid" />
						</div>
					</div>

					<div class="form-group">
						<div class="form-group-header">
							<label for="username">Username</label>
						</div>
						<div class="form-group-body">
							<input class="form-control width-full" type="text" id="username" v-model="username" />
						</div>
					</div>

					<div class="form-group">
						<div class="form-group-header">
							<label for="password">Password</label>
						</div>
						<div class="form-group-body">
							<input class="form-control width-full" type="password" id="password" v-model="password" />
						</div>
					</div>
				</form>
			</div>
			<div class="Box-footer">
				<button class="btn btn-primary width-full mr-1" @click="connect"><i class="fas fa-check-circle"></i>
					Connect </button>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: "sap",
	data() {
		return {
			hostname: '',
			port: '',
			sid: '',
			username: '',
			password: '',
			error: null,
			system: 'sap',
		}
	},
	methods: {
		connect() {
			this.$store.dispatch('connection/connect', {
				hostname: this.hostname,
				port: this.port,
				sid: this.sid,
				username: this.username,
				password: this.password,
				system: this.system,
			})
				.then(() => {
					this.$emit('created');
				})
				.catch(e => {
					this.error = e.message;
				});
		},
	},
};
</script>

<style scoped></style>
