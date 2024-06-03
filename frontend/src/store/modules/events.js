// store/modules/events.js

import API from '../../api';

export default {
    namespaced: true,
    state: {
        events: [],
        error: null,
    },
    mutations: {
        addEvent(state, event) {
            state.events.push(event);
        },
        removeEvent(state, event) {
            let i = state.events.findIndex(e => e.id === event.id);
            state.events.splice(i, 1);
        },
        saveEventInfo(state, event) {
            let i = state.events.findIndex(e => e.id === event.id);
            state.events[i] = event;
        },
        setEvents(state, events) {
            state.events = events;
        },
        setError(state, error) {
            state.error = error;
        }
    },
    getters: {
        eventNames(state) {
            return state.events.map(event => ({ id: event.id, name: event.name }));
        }
    },
    actions: {
        async fetchAll({ commit, dispatch }) {
            try {
                return API.get('/events/all')
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('setEvents', response.data);
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
        async addEvent({ commit, dispatch }, event) {
            try {
                return API.post('/events/new', event)
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            let event = response.data;
                            commit('addEvent', event);
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
        async updateEvent({ commit, dispatch }, event) {
            try {
                return API.post('/events/update', event)
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            let event = response.data;
                            commit('saveEventInfo', event);
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
        async removeEvent({ commit, dispatch }, event) {
            try {
                return API.post('/events/remove', event)
                    .then(response => {
                        if (response.status >= 200 && response.status < 300) {
                            commit('removeEvent', event);
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
        }
    },
};
