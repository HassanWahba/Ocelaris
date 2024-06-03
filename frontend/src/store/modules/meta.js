// store/modules/meta.js

import API from '../../api';

export default {
    namespaced: true,
    state: {
        metaTables: [],
        error: null,
    },
    mutations: {
        addMetaTable(state, metaTable) {
            state.metaTables.push(metaTable);
        },
        saveMetaTableInfo(state, metaTable) {
            let i = state.metaTables.findIndex(meta => meta.id == metaTable.id);
            Vue.set(state.metaTables, i, metaTable);
        },
        removeMetaTable(state, id) {
            let i = state.metaTables.findIndex(meta => meta.id == id);
            state.metaTables.splice(i, 1);
        },
        setMetaTables(state, metaTables) {
            state.metaTables = metaTables;
        },
        setError(state, error) {
            state.error = error;
        }
    },
    getters: {
        metaNames(state) {
            return state.metaTables.map(meta => ({ id: meta.id, name: meta.meta.name }));
        },
        getMetaNameFromID(state) {
            return (id) => {
                let meta = state.metaTables.find(m => m.id == id);
                return meta.meta.name;
            }
        }
    },
    actions: {
        async fetchAll({ commit, dispatch }) {
            try {
                return API.get('/meta-tables/all')
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('setMetaTables', response.data);
                        } else {
                            commit('setError', `Request failed with status code: ${response.status}`);
                        }
                    }).catch(error => {
                        dispatch('handleError', error);
                    })
            } catch (error) {
                dispatch('handleError', error);
            }
        },
        async fetchViewInfo({ commit, dispatch }, id) {
            try {
                return API.post('/meta-tables/view-info', { id: id })
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('saveMetaTableInfo', response.data);
                        } else {
                            commit('setError', `Request failed with status code: ${response.status}`);
                        }
                    }).catch(error => {
                        dispatch('handleError', error);
                    })
            } catch (error) {
                dispatch('handleError', error);
            }
        },
        async addMetaTable({ commit, dispatch }, metaTable) {
            try {
                return API.post('/meta-tables/new', metaTable)
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            metaTable = response.data;
                            commit('addMetaTable', metaTable);
                        } else {
                            commit('setError', `Request failed with status code: ${response.status}`);
                        }
                        return response;
                    }).catch(error => {
                        dispatch('handleError', error);
                    })
            } catch (error) {
                dispatch('handleError', error);
            }
        },
        async removeMetaTable({ commit, dispatch }, id) {
            try {
                return API.post('/meta-tables/remove', { id: id })
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('removeMetaTable', id);
                        } else {
                            commit('setError', `Request failed with status code: ${response.status}`);
                        }
                        return response;
                    }).catch(error => {
                        dispatch('handleError', error);
                    })
            } catch (error) {
                dispatch('handleError', error);
            }
        },
        handleError({ commit }, error) {
            if (error.response) {
                commit('setError', `Error: ${error.response.data}`);
            } else if (error.request) {
                commit('setError', `No response from server. ${error.message}`);
            } else {
                commit('setError', `Error: ${error.message}`);
            }
        }
    },
};
