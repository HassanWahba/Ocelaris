// store/modules/tables.js

import API from '../../api';

export default {
    namespaced: true,
    state: {
        tables: [],
        error: null,
    },
    mutations: {
        setTables(state, tables) {
            state.tables = tables;
        },
        setTable(state, table) {
            const index = state.tables.findIndex(t => t.id == table.id);
            if (index !== -1) {
                state.tables.splice(index, 1, table);
            } else {
                state.tables.push(table);
            }
        },
        setError(state, error) {
            state.error = error;
        }
    },
    actions: {
        async fetchAll({ commit, dispatch }) {
            try {
                return API.get('/db/table-names')
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('setTables', response.data);
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
        async fetchTablesWith({ commit, dispatch }, { filter }) {
            try {
                return API.post('/db/tables-with', { filter })
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('setTables', response.data);
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
                return API.post('/db/table-view', { id })
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('setTable', response.data);
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
        handleError({ commit }, error) {
            if (error.response) {
                commit('setError', `Error: ${error.response.data}`);
            } else if (error.request) {
                commit('setError', `No response from server. ${error.message}`);
            } else {
                commit('setError', `Error: ${error.message}`);
            }
        },
        async testSetup({ commit }) {
            let testTables = [
                { id: 123212, meta: { name: 'EKKO' }, preview: { headers: [{ text: 'Number', value: 'a' }], items: [{ a: '123' }] } },
                { id: 123213, meta: { name: 'EKPO' }, preview: { headers: [{ text: 'Number', value: 'a' }], items: [{ a: '123' }] } },
                { id: 321321, meta: { name: 'EKIV' }, preview: { headers: [{ text: 'Number', value: 'a' }], items: [{ a: '123' }] } },
            ];
            commit('setTables', testTables);
        }
    }
};
