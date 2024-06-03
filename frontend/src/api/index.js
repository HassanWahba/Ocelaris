// src/api/index.js

import Axios from 'axios';

let ENDPOINT = '/api';
if (process.env.NODE_ENV === 'development') {
	ENDPOINT = 'http://127.0.0.1:5000' + ENDPOINT;
}

export default {
	get(path) {
		return Axios.get(ENDPOINT + path);
	},
	post(path, data, config) {
		return Axios.post(ENDPOINT + path, data, config);
	},
	delete(path, options) {
		return Axios.delete(ENDPOINT + path, options);
	}
};
