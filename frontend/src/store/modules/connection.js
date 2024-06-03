// store/modules/connection.js

import API from '../../api';

export default {
    namespaced: true,
    state: {
        status: 'disconnected',
        error: null,
        details: null,
        supported: null,
    },
    mutations: {
        setStatus(state, status) {
            state.status = status;
        },
        setError(state, error) {
            state.error = error;
        },
        setDetails(state, details) {
            state.details = details;
        },
        clearDetails(state) {
            state.details = null;
        },
        setSupported(state, supported) {
            state.supported = supported;
        },
    },
    getters: {
        status: state => state.status,
        error: state => state.error,
        details: state => state.details,
        supported: state => state.supported,
    },
    actions: {
        async validateConnection({ commit }) {
            return API.get('/db/validate').then(response => {
                response = response.data
                if (response.status == "error") {
                    commit('setError', `Error: ${response.message}`);
                    return false;
                }
                commit('setStatus', 'connected');
                commit('setDetails', response);
                return true;
            }).catch(error => {
                if (error.response) {
                    commit('setError', `Error: ${error.response.data}`);
                    commit('setStatus', 'disconnected');
                    commit('setDetails', null);
                } else if (error.request) {
                    commit('setError', `No response from server. ${error.message}`);
                    commit('setStatus', 'disconnected');
                    commit('setDetails', null);
                } else {
                    commit('setError', `Error: ${error.message}`);
                    commit('setStatus', 'disconnected');
                    commit('setDetails', null);
                }
                return false;
            });
        },
        async connect({ commit }, { hostname, port, sid, username, password, db_type, erp_type }) {
            return API.post('/db/connect', {
                hostname,
                port,
                sid,
                username,
                password,
                db_type,
                erp_type,
            }).then(response => {
                response = response.data
                if (response.status == "error") {
                    commit('setError', `Error: ${response.message}`);
                    this.$notify.error('Error Occurred While Connecting: ' + response.message)
                    return;
                }
                commit('setStatus', 'connected');
                commit('setDetails', response);
            }).catch(error => {
                if (error.response) {
                    commit('setError', `Error: ${error.response.data}`);
                    commit('setStatus', 'disconnected');
                    commit('setDetails', null);
                } else if (error.request) {
                    commit('setError', `No response from server. ${error.message}`);
                    commit('setStatus', 'disconnected');
                    commit('setDetails', null);
                } else {
                    commit('setError', `Error: ${error.message}`);
                    commit('setStatus', 'disconnected');
                    commit('setDetails', null);
                }
            });
        },
        async fetchSupportedDatabases({ commit }) {
            return API.get('/db/supported_databases').then(response => {
                response = response.data
                if (response.status == "error") {
                    commit('setError', `Error: ${response.message}`);
                    return;
                }
                commit('setSupported', response);
            }).catch(error => {
                if (error.response) {
                    commit('setError', `Error: ${error.response.data}`);
                } else if (error.request) {
                    commit('setError', `No response from server. ${error.message}`);
                } else {
                    commit('setError', `Error: ${error.message}`);
                }
            });
        },
        disconnect({ commit }) {
            // Add code to disconnect from the server
            commit('setStatus', 'disconnected');
            commit('clearDetails');
        },
    },
};
