// store/modules/process.js

import API from '../../api';

export default {
    namespaced: true,
    state: {
        logs: [],
        error: null,
    },
    mutations: {
        addLog(state, log) {
            state.logs.push(log);
        },
        removeLog(state, id) {
            let i = state.logs.findIndex(meta => meta.id == id);
            state.logs.splice(i, 1);
        },
        setLogs(state, logs) {
            state.logs = logs;
        },
        setError(state, error) {
            state.error = error;
        }
    },
    getters: {
        changeLogNames(state) {
            let atts = log => log.meta.attributes ? log.meta.attributes.split(',').map(item => item.trim()) : [];
            return state.logs.map(log => ({ id: log.id, name: log.meta.name, columns: [log.meta.event_timestamp, log.meta.event_target, ...atts(log)] }));
        }
    },
    actions: {
        async fetchAll({ commit, dispatch }) {
            try {
                return API.get('/change-logs/all')
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('setLogs', response.data);
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
        async addLog({ commit, dispatch }, id) {
            try {
                return API.post('/change-logs/new', id)
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            let log = response.data;
                            commit('addLog', log);
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
        async updateLog({ commit, dispatch }, log) {
            try {
                return API.post('/change-logs/update', log)
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('removeLog', response.data);
                            commit('addLog', response.data);
                        } else {
                            dispatch('handleError', `Request failed with status code: ${response.status}`);
                        }
                        return response;
                    }).catch(error => {
                        dispatch('handleError', error);
                    })
            } catch (error) {
                dispatch('handleError', error);
            }
        },
        async removeLog({ commit, dispatch }, log) {
            try {
                return API.post('/change-logs/remove', log)
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('removeLog', response.data);
                        } else {
                            dispatch('handleError', `Request failed with status code: ${response.status}`);
                        }
                    })
                    .catch(error => {
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
