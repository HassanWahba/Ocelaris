<template>
	<div class="nav text-white">
		<div class="inner">
			<div class="title">Ocelaris</div>
			<div class="navigation-buttons">
				<router-link class="link" to="/load">IO</router-link>
				<router-link class="link" to="/transform">OCDM</router-link>
				<router-link class="link" to="/extract">Setup</router-link>
				<router-link class="link" to="/db-connect">DB Connection</router-link>
				<router-link class="link" to="/home">Home</router-link>
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'ocel-nav',
};
</script>

<style scoped>
.nav {
	height: 50px;
	width: 100%;
	background-color: #2A3990;
}

.nav .inner {
	height: 100%;
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding: 0 15px 0 15px;
}

.title {
	font-weight: 500;
	float: left;
	margin-left: 170px;
}

.link {
	font-weight: 500;
	margin-left: 25px;
	text-decoration: none;
	color: #a6a8a3;
	float: right;
}

.link:hover,
.router-link-active {
	color: white;
}

.navigation-buttons {
	margin-right: 150px;
}
</style>
