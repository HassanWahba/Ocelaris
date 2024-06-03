import { Notyf } from 'notyf';
import 'notyf/notyf.min.css';

import Vue from 'vue/dist/vue.esm.browser';
import VueRouter from 'vue-router';

import API from '../src/api';
import Store from '../src/store';

Vue.prototype.$api = API;
Vue.prototype.$store = Store;

Vue.prototype.$notify = new Notyf({
	position: { x: 'center', y: 'top' }
});

Vue.use(VueRouter);


/*
	Generic Components
 */

import Nav from './components/SharedComponents/Nav.vue';

import ViewTable from './components/SharedComponents/ViewTable.vue';
import TableMeta from './components/SharedComponents/Tables/TableMeta.vue';

import TablePreview from './components/SharedComponents/Tables/TablePreview.vue';

Vue.component('ocel-nav', Nav);

Vue.component('view-table', ViewTable);

Vue.component('table-meta', TableMeta);
Vue.component('table-preview', TablePreview);



/*
	Diagram Components
 */

import Diagram from "./components/SharedComponents/Diagram/Diagram.vue";
import Node from "./components/SharedComponents/Diagram/Node.vue";

import Link from "./components/SharedComponents/Diagram/Link.vue";
import EditLinkModal from "./components/SharedComponents/Diagram/Modals/EditLinkModal.vue";
import EditNodeModal from "./components/SharedComponents/Diagram/Modals/EditNodeModal.vue";

Vue.component('diagram', Diagram);
Vue.component('graph-node', Node);
Vue.component('graph-link', Link);
Vue.component('edit-link-modal', EditLinkModal);
Vue.component('edit-node-modal', EditNodeModal);


/*
	Database Components
 */

import ConnectionInfo from './components/DBConnection/ConnectionInfo.vue';
import CustomERP from './components/DBConnection/CustomERP.vue';
import Oracle from './components/DBConnection/Oracle.vue';

Vue.component('connection-info', ConnectionInfo);
Vue.component('custom', CustomERP);
Vue.component('oracle', Oracle);


/*
	Extractor Components
 */

import ExtractorSidebar from './components/Extractor/ExtractorSidebar.vue';

import CreateMeta from './components/Extractor/Meta/CreateMeta.vue';
import ViewMeta from './components/Extractor/Meta/ViewMeta.vue';

import CreateChangeLog from './components/Extractor/ChangeLogs/CreateChangeLog.vue';
import ViewChangeLog from './components/Extractor/ChangeLogs/ViewChangeLog.vue';

Vue.component('extractor-sidebar', ExtractorSidebar);

Vue.component('create-meta', CreateMeta);
Vue.component('view-meta', ViewMeta);

Vue.component('create-change-log', CreateChangeLog);
Vue.component('view-change-log', ViewChangeLog);


/*
	Transformer Components
 */

import TransformerSidebar from './components/Transformer/TransformerSidebar.vue';

import CreateEvent from './components/Transformer/Events/CreateEvent.vue';
import ViewEvent from './components/Transformer/Events/ViewEvent.vue';

import CreateObject from './components/Transformer/Objects/CreateObject.vue';
import CreateSQL from './components/Transformer/Objects/CreateSQL.vue';
import GraphicalObject from './components/Transformer/Objects/GraphicalObject.vue';
import ViewObject from './components/Transformer/Objects/ViewObject.vue';

import ViewProcess from './components/Transformer/Processes/ViewProcess.vue';
import EditProcess from './components/Transformer/Processes/EditProcess.vue';
import CreateProcess from './components/Transformer/Processes/CreateProcess.vue';

Vue.component('transformer-sidebar', TransformerSidebar);

Vue.component('create-event', CreateEvent);
Vue.component('view-event', ViewEvent);

Vue.component('create-object', CreateObject);
Vue.component('create-sql', CreateSQL);
Vue.component('graphical-object', GraphicalObject);
Vue.component('view-object', ViewObject);

Vue.component('create-process', CreateProcess);
Vue.component('view-process', ViewProcess);
Vue.component('edit-process', EditProcess);

/*
	Loader Components
 */

import IOHandler from './components/Loader/IOHandler.vue'

Vue.component('io-handler', IOHandler);

/*
	import Views
 */

import Home from './views/Home.vue';
import DB from './views/DatabaseConnection.vue';
import Transformer from './views/Transformer.vue';
import Extractor from './views/Extractor.vue';
import Loader from './views/Loader.vue';

/*
	Routes
 */

const routes = [
	{ path: '/', redirect: '/home' },
	{ path: '/home', component: Home },
	{ path: '/db-connect', component: DB },
	{ path: '/load', component: Loader },
	{ path: '/extract', component: Extractor },
	{ path: '/transform', component: Transformer }
];
const router = new VueRouter({
	routes,
	mode: 'history'
});

/*
	Redirect, if not connected.
 */

const allowedRoutes = ['/home', '/db-connect'];
const allowedRoute = ['/'];

router.beforeEach((to, from, next) => {
	if (allowedRoute.some(route => to.path.startsWith(route))) {
		next();
	} else {
		if (Store.state.connection.status === 'connected') {
			next();
		} else {
			Vue.prototype.$notify.error('Please connect to a Database first. Current connection status is ' + Store.state.connection.error)
			next('/db-connect');
		}
	}
});
const app = new Vue({
	router
})

app.$mount('#app');
