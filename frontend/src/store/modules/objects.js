// store/modules/objects.js

import API from '../../api';

export default {
    namespaced: true,
    state: {
        objects: [],
        error: null,
    },
    mutations: {
        addObject(state, object) {
            state.objects.push(object);
        },
        removeObject(state, id) {
            let i = state.objects.findIndex(meta => meta.id == id);
            state.objects.splice(i, 1);
        },
        saveObjectInfo(state, object) {
            let index = state.objects.findIndex(o => o.id == object.id);
            if (index !== -1) {
                state.objects.splice(index, 1, object);
            } else {
                state.objects.push(object);
            }
        },
        setObjects(state, objects) {
            state.objects = objects;
        },
        setError(state, error) {
            state.error = error;
        }
    },
    getters: {
        objectNames(state) {
            return state.objects.map(object => ({ id: object.id, name: object.meta.name }));
        }
    },
    actions: {
        async fetchAll({ commit, dispatch }) {
            try {
                return API.get('/objects/all')
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('setObjects', response.data);
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
        async removeObject({ commit, dispatch }, id) {
            try {
                return API.post('/objects/remove', id)
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('removeObject', id);
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
        async addSQLObject({ commit }, object) {
            try {
                return API.post('/objects/sql/new', object)
                    .then(response => {
                        console.log(response);
                        if (response.status >= 200 && response.status < 300) {
                            let object = response.data;
                            commit('addObject', object);
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
        async updateSQLObject({ commit }, object) {
            try {
                return API.post('/objects/sql/update', object)
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            let object = response.data;
                            commit('saveObjectInfo', object);
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
