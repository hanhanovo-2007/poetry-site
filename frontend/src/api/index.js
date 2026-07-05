import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  timeout: 15000,
});

// 请求拦截器：自动设置 Content-Type（FormData 时不覆盖）
api.interceptors.request.use((config) => {
  if (config.data instanceof FormData) {
    delete config.headers["Content-Type"];
  } else {
    config.headers["Content-Type"] = "application/json";
  }
  return config;
});

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const msg = error.response?.data?.message || error.message || "网络错误";
    return Promise.reject(new Error(msg));
  }
);

export default api;
