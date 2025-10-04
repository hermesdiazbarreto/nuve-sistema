import axios from "axios";

// Usa variable de entorno para producción, o localhost para desarrollo
const BASE_URL = process.env.VUE_APP_API_URL || "http://localhost:8000/api";

export default axios.create({
    baseURL: BASE_URL,
    timeout: 50000,
    headers: {
        "content-type": "application/json"
    }
});
