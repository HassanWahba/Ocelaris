<template>
  <div class="home-container">
    <div class="card">
      <h1 class="title">{{ message }}</h1>
      <p class="description">This tool allows you to extract data from your ERP system and interactively generate object-centric event logs. It provides options for data import, export, and a feature-rich editor.</p>
      <router-link to="/db-connect">
			  <button class="btn btn-primary width-full mr-1"><i class="fas fa-check-circle"></i> Connect to a database </button>
			</router-link>
        <a href="https://github.com/HassanWahba/Ocelaris" target="_blank">
          <button class="btn width-full"> See Repository </button>
        </a>
    </div>
  </div>
</template>

<script>
export default {
	name: 'Home',
	data: () => {
		return {
			message: 'The OCEL Interactive Modeller & Extractor Tool'
		};
	},
};
</script>

<style scoped>
.home-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 60px);
}

.card {
  max-width: 500px;
  padding: 20px;
  background: #fff;
  box-shadow: 0 0 15px rgba(0,0,0,0.1);
  border-radius: 5px;
  text-align: center;
  animation: fadeIn 1s ease-in-out;
}

.title {
  margin: 0;
  margin-bottom: 15px;
  font-size: 28px;
  color: #333;
}

.description {
  margin-bottom: 30px;
  font-size: 16px;
  color: #666;
  line-height: 1.5;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
