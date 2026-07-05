import api from "./index";

export function getWorks(params) {
  return api.get("/works/", { params });
}

export function getWork(id) {
  return api.get(`/works/${id}/`);
}

export function createWork(data) {
  // 如果包含文件，用 FormData 提交
  if (data instanceof FormData) {
    return api.post("/works/", data, {
      headers: { "Content-Type": "multipart/form-data" },
    });
  }
  return api.post("/works/", data);
}

export function updateWork(id, data) {
  return api.put(`/works/${id}/`, data);
}

export function deleteWork(id) {
  return api.delete(`/works/${id}/`);
}

export function likeWork(id) {
  return api.post(`/works/${id}/like/`);
}

export function getComments(workId) {
  return api.get(`/works/${workId}/comments/`);
}

export function addComment(workId, data) {
  return api.post(`/works/${workId}/comments/`, data);
}
