import Vue from 'vue';
import Vuex from 'vuex';
import connection from './modules/connection';
import tables from './modules/tables';
import events from './modules/events';
import objects from './modules/objects';
import processes from './modules/processes';
import meta from './modules/meta';
import log from './modules/log';
import io from './modules/io';;

Vue.use(Vuex);
const store = new Vuex.Store({
  modules: {
    connection,
    tables,
    events,
    objects,
    processes,
    meta,
    log,
    io,
  },
  actions: {
    async fetchAllData({ dispatch }) {
      try {
        await dispatch('meta/fetchAll');
        await dispatch('log/fetchAll');
        await dispatch('tables/fetchAll');
        await dispatch('events/fetchAll');
        await dispatch('objects/fetchAll');
        await dispatch('processes/fetchAll');
        console.log('All data has been fetched!');
        return true;
      } catch (e) {
        console.error(e.message);
        return false;
      }
    },
    async fetchExtractorData({ dispatch }) {
      try {
        await dispatch("meta/fetchAll");
        await dispatch("log/fetchAll");
        console.log('Extractor data has been fetched!');
      } catch (e) {
        console.error(e.message);
      }
    },
    async fetchTransformerData({ dispatch }) {
      try {
        await dispatch("tables/fetchAll");
        await dispatch("log/fetchAll");
        await dispatch("events/fetchAll");
        await dispatch("objects/fetchAll");
        await dispatch("processes/fetchAll");
        console.log('Transformer data has been fetched!');
      } catch (e) {
        console.error(e.message);
      }
    },
    async fetchLoaderData({ dispatch }) {
      try {
        await dispatch("events/fetchAll");
        await dispatch("objects/fetchAll");
        await dispatch("processes/fetchAll");
        console.log('Loader data has been fetched!');
      } catch (e) {
        console.error(e.message);
      }
    },
  },
});

export default store;
