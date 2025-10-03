import axios from "axios";

const BASE_URL = "http://localhost:8000/api"; // Local


export default axios.create({
    baseURL: BASE_URL,
    timeout: 50000,
    headers: {
        "content-type": "application/json"
    }
});
