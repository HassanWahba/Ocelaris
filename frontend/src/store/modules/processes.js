// store/modules/process.js

import API from '../../api';

export default {
    namespaced: true,
    state: {
        processes: [],
        error: null,
    },
    mutations: {
        addProcess(state, process) {
            state.processes.push(process);
        },
        removeProcess(state, processID) {
            let i = state.processes.findIndex(process => process.id == processID);
            state.processes.splice(i, 1);
        },
        saveProcessInfo(state, process) {
            let index = state.processes.findIndex(p => p.id === process.id);
            if (index !== -1) {
                state.processes.splice(index, 1, object);
            } else {
                state.processes.push(object);
            }
        },
        setProcesses(state, processes) {
            state.processes = processes;
        },
        setError(state, error) {
            state.error = error;
        }
    },
    actions: {
        async fetchAll({ commit, dispatch }) {
            try {
                return API.get('/processes/all')
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('setProcesses', response.data);
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
        async addProcess({ commit, dispatch }, process) {
            try {
                return API.post('/processes/new', process)
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            let process = response.data;
                            commit('addProcess', process);
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
        async updateProcess({ commit, dispatch }, process) {
            try {
                return API.post('/processes/update', process)
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('saveProcessInfo', process);
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
        async removeProcess({ commit, dispatch }, process) {
            console.log(process);
            try {
                return API.post('/processes/remove', process)
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('removeProcess', process);
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
        async fetchViewInfo({ commit, dispatch }, id) {
            try {
                const response = await API.post('/processes/view-info', { id: id });
                if (response.status >= 200 && response.status < 300) {
                    commit('setMetaTableInfo', response.data);
                } else {
                    commit('setError', `Request failed with status code: ${response.status}`);
                }
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
