import API from '../../api';

export default {
    namespaced: true,
    state: {
        error: null,
    },
    mutations: {
        setError(state, error) {
            state.error = error;
        }
    },
    actions: {
        async exportDBSnapshot({ dispatch }) {
            try {
                return API.get(`/processes/export-db-snapshot`, { responseType: 'blob' })
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            return response.data;
                        } else {
                            dispatch('handleError', `Request failed with status code: ${response.status}`);
                        }
                    }).catch(error => {
                        dispatch('handleError', error);
                    })
            } catch (e) {
                dispatch('handleError', e);
            }
        },
        async exportSQLiteOCEL({ dispatch }, process_id) {
            try {
                return API.post(`/processes/ocel-sql`, { id: process_id, format: 'sqlite' }, { responseType: 'blob' })
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            return response.data;
                        } else {
                            dispatch('handleError', `Request failed with status code: ${response.status}`);
                        }
                    }).catch(error => {
                        dispatch('handleError', error);
                    })
            } catch (e) {
                dispatch('handleError', e);
            }
        },
        handleError({ commit }, error) {
            commit('setError', error);
        }
    }
}
